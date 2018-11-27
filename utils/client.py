
import aiohttp
import io
import logging
import re
import json
import datetime as dt

from . import utils, nano, errors

log = logging.getLogger("talos.utils")


class TalosHTTPClient(aiohttp.ClientSession):
    """
        Extension of the aiohttp ClientSession to provide utility methods for getting certain sites and such,
        and automatically handling various tokens for those sites.
    """

    __slots__ = ("nano_tries", "last_guild_count", "__tokens")

    TALOS_URL = "https://talosbot.org/"
    BOTLIST_URL = "https://discordbots.org/"
    NANO_URL = "https://nanowrimo.org/"
    BTN_URL = "https://www.behindthename.com/"
    CAT_URL = "https://api.thecatapi.com/v1/"
    XKCD_URL = "https://xkcd.com/"
    SMBC_URL = "https://smbc-comics.com/"

    def __init__(self, *args, tokens=None, **kwargs):
        """
            Create a Talos HTTP Client object
        :param args: arguments to pass on
        :param kwargs: keyword args to use and pass on
        """
        self.__tokens = tokens if tokens else {}
        self.nano_tries = 0
        self.last_guild_count = 0

        super().__init__(*args, **kwargs)

    async def get_site(self, url, **kwargs):
        """
            Get the text of a given URL
        :param url: url to get text from
        :param kwargs: keyword args to pass to the GET call
        :return: text of the requested page
        """
        async with self.get(url, **kwargs) as response:
            return utils.to_dom(await response.text())

    async def server_post_commands(self, commands):
        headers = {
            "Token": self.__tokens["webserver"],
            "User": "Talos"
        }
        await self.post(self.TALOS_URL + "api/commands", json=commands, headers=headers)
        pass

    async def botlist_post_guilds(self, num):
        """
            Post a number of guilds to the discord bot list. Will only post if there's a botlist token available
            and the passed number is different from the last passed number
        :param num: Number of guilds to post
        """
        if num == self.last_guild_count or self.__tokens.get("botlist", "") == "":
            return
        log.info("Posting guilds to Discordbots")
        self.last_guild_count = num
        headers = {
            'Authorization': self.__tokens["botlist"]
        }
        data = {'server_count': num}
        api_url = self.BOTLIST_URL + 'api/bots/199965612691292160/stats'
        await self.post(api_url, json=data, headers=headers)

    async def btn_get_names(self, gender="", usage="", number=1, surname=False):
        """
            Get names from Behind The Name
        :param gender: gender to restrict names to. m or f
        :param usage: usage to restrict names to. eng for english, see documentation
        :param number: number of names to generate. Between 1 and 6.
        :param surname: whether to generate a random surname. Yes or No
        :return: List of names generated or None if failed
        """
        surname = "yes" if surname else "no"
        gender = "&gender="+gender if gender else gender
        usage = "&usage="+usage if usage else usage
        url = self.BTN_URL + f"api/random.php?key={self.__tokens['btn']}&randomsurname={surname}&number={number}"\
                             f"{gender}{usage}"
        async with self.get(url) as response:
            if response.status == 200:
                doc = utils.to_dom(await response.text())
                return [x.innertext for x in doc.get_by_tag("name")]
            else:
                log.warning(f"BTN returned {response.status}")
                return []

    async def nano_get_page(self, url):
        """
            Safely gets a page from the NaNoWriMo website. Tries to log on, but returns None if that fails three times
            or for whatever reason the page can't be resolved
        :param url: NaNo URL path to fetch from
        :return: text of the page or None
        """
        async with self.get(self.NANO_URL + url) as response:
            if response.status == 200:
                if not str(response.url).startswith(self.NANO_URL + re.sub(r"/.*", "", url)):
                    return None
                return utils.to_dom(await response.text())
            elif response.status == 403:
                response = await self.nano_login_client()
                if response == 200:
                    return await self.nano_get_page(url)
                else:
                    return None
            else:
                log.warning(f"Got unexpected response status {response.status}")
                return None

    async def nano_get_user(self, username):
        """
            Returns a given NaNo user profile, if it can be found.
        :param username: username of nano user to get profile of
        :return: text of the profile page for that user or None
        """
        user = nano.NanoUser(self, username)
        await user._initialize()
        return user

    async def nano_get_novel(self, username, title=None):
        """
            Returns the novel of a given NaNo user. This year's novel, if specific name not given.
        :param username: user to get novel of.
        :param title: novel to get for user. Most recent if not given.
        :return: NanoNovel object, or None.
        """
        user = nano.NanoUser(self, username)
        if title is None:
            return await user.current_novel
        else:
            for novel in await user.novels:
                if novel.title == title:
                    return novel
            raise errors.NotANovel(title)

    async def nano_login_client(self):
        """
            Login the client to the NaNo site.
        :return: status of login request.
        """
        self.nano_tries += 1
        login_page = await self.get_site(self.NANO_URL + "sign_in")
        auth_el = login_page.get_by_name("authenticity_token")
        auth_key = ""
        if auth_el:
            auth_key = auth_el.get_attribute("value")
        params = {
            "utf8": "✓",
            "authenticity_token": auth_key,
            "user_session[name]": self.__tokens["nano"][0],
            "user_session[password]": self.__tokens["nano"][1],
            "user_session[remember_me]": "0",
            "commit": "Sign+in"
        }
        async with self.post(self.NANO_URL + "sign_in", data=params) as response:
            doc = utils.to_dom(await response.text())
            status = response.status
            sign_in = list(filter(lambda x: x.get_attribute("href") == "/sign_in", doc.get_by_tag("a")))
            if sign_in:
                if self.nano_tries < 3:
                    return await self.nano_login_client()
                else:
                    status = 403
                    self.nano_tries = 0
            else:
                self.nano_tries = 0
            return status

    async def get_cat_pic(self):
        """
            Get a random cat picture from The Cat API
        :return: A discord.File with a picture of a cat.
        """
        async with self.get(self.CAT_URL + f"images/search?api_key={self.__tokens['cat']}&type=jpg,png") as response:
            data = json.loads(await response.text())[0]
        async with self.get(data["url"]) as response:
            data["filename"] = data["url"].split("/")[-1]
            data["img_data"] = io.BytesIO(await response.read())
        return data

    async def get_xkcd(self, xkcd):
        """
            Get the data from an XKCD comic and return it as a dict
        :param xkcd: XKCD to get, or None if current
        :return: Dict of JSON data
        """
        async with self.get(self.XKCD_URL + (f"{xkcd}/" if xkcd else "") + "info.0.json") as response:
            data = await response.text()
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return None
        async with self.get(data["img"]) as response:
            data["filename"] = data["img"].split("/")[-1]
            data["img_data"] = io.BytesIO(await response.read())
        return data

    async def get_smbc_list(self):
        """
            Get the list of current SMBC comics from the smbc archive
        :return: List of elements
        """
        async with self.get(self.SMBC_URL + "comic/archive/") as response:
            dom = utils.to_dom(await response.text())
            selector = dom.get_by_name("comic")
            return selector.child_nodes[1:]

    async def get_smbc(self, smbc):
        """
            Get the data for an SMBC from its ID
        :param smbc: SMBC to get, or None if current
        :return: Dict of JSON data
        """
        data = {}
        if isinstance(smbc, int):
            url = self.SMBC_URL + f"index.php?db=comics&id={smbc}"
        else:
            url = self.SMBC_URL + f"comic/{smbc}"
        async with self.get(url, headers={"user-agent": ""}) as response:
            dom = utils.to_dom(await response.text())
            data["title"] = "-".join(dom.get_by_tag("title")[0].innertext.split("-")[1:]).strip()
            comic = dom.get_by_id("cc-comic")
            if comic is None:
                return None
            data["img"] = comic.get_attribute("src")
            data["alt"] = comic.get_attribute("title")
            time = dom.get_by_class("cc-publishtime")[0]
            date = dt.datetime.strptime(time.innertext, "Posted %B %d, %Y at %I:%M %p")
            data["time"] = date
        async with self.get(data["img"]) as response:
            data["filename"] = data["img"].split("/")[-1]
            data["img_data"] = io.BytesIO(await response.read())
        return data
