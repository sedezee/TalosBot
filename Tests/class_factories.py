"""
    Functions and classes for building various discord.py classes
"""

import datetime as dt
import asyncio
import discord
import discord.ext.commands as commands
import discord.ext.commands.view as dview


class FakeState:

    def __init__(self):
        self._users = {}
        self.user = discord.ClientUser(state=self, data=make_user_dict("State", "0000", None, make_id()))
        self._private_channels_by_user = {}
        self.shard_count = None

    def store_user(self, data):
        # this way is 300% faster than `dict.setdefault`.
        user_id = int(data['id'])
        try:
            return self._users[user_id]
        except KeyError:
            self._users[user_id] = user = discord.User(state=self, data=data)
            return user

    def _get_private_channel_by_user(self, user_id):
        return self._private_channels_by_user.get(user_id)


class FakeContext(commands.Context):

    def __init__(self, **attrs):
        self.callback = attrs.get('callback', None)
        super().__init__(**attrs)

    def set_callback(self, callback):
        self.callback = callback

    async def send(self, content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None):
        value = self.callback(content, tts=tts, embed=embed, file=file, files=files, delete_after=delete_after, nonce=nonce)
        if asyncio.iscoroutine(value) or asyncio.isfuture(value):
            return await value
        else:
            return value


generated_ids = 0


def make_id():
    global generated_ids
    # timestamp
    discord_epoch = str(bin(int(dt.datetime.now().timestamp() * 1000) - 1420070400000))[2:]
    discord_epoch = "0" * (42 - len(discord_epoch)) + discord_epoch
    # internal worker id
    worker = "00001"
    # internal process id
    process = "00000"
    # determine how many ids have been generated so far
    generated = str(bin(generated_ids)[2:])
    generated_ids += 1
    generated = "0" * (12 - len(generated)) + generated
    # and now finally return the ID
    return int(discord_epoch + worker + process + generated, 2)


def make_user_dict(username, discriminator, avatar, id_num):
    return {
        'username': username,
        'discriminator': discriminator,
        'avatar': avatar,
        'id': id_num
    }


def make_role_dict(name, id_num):
    return {
        'id': id_num,
        'name': name
    }


def make_member_dict(username, discriminator, nick, roles, avatar, id_num):
    return {
        'user': make_user_dict(username, discriminator, avatar, id_num),
        'nick': nick,
        'roles': roles,
        'id': id_num
    }


test_state = FakeState()


def make_guild(name, members=None, channels=None, roles=None, id_num=-1):
    if id_num == -1:
        id_num = make_id()
    if roles is None:
        roles = [make_role_dict("@everyone", id_num)]
    if channels is None:
        channels = []
    if members is None:
        members = []
    else:
        map(lambda x: make_member_dict(x.name, x.discriminator, x.nick, x.roles, x.avatar, x.id), members)
    member_count = len(members) if len(members) != 0 else 1
    return discord.Guild(
        state=test_state,
        data={
            'name': name,
            'roles': roles,
            'channels': channels,
            'members': members,
            'member_count': member_count,
            'id': id_num
        }
    )


def make_text_channel(name, guild, position=-1, id_num=-1):
    if id_num == -1:
        id_num = make_id()
    if position == -1:
        position = len(guild.channels) + 1
    channel = discord.TextChannel(
        state=test_state,
        guild=guild,
        data={
            'id': id_num,
            'name': name,
            'position': position
        }
    )
    guild._add_channel(channel)
    return channel


def make_user(username, discriminator, avatar=None, id_num=-1):
    if id_num == -1:
        id_num = make_id()
    return discord.User(
        state=test_state,
        data=make_user_dict(username, discriminator, avatar, id_num)
    )


def make_member(username, discriminator, guild, nick=None, roles=None, avatar=None, id_num=-1):
    if id_num == -1:
        id_num = make_id()
    if roles is None:
        roles = []
    if nick is None:
        nick = username
    member = discord.Member(
        state=test_state,
        guild=guild,
        data=make_member_dict(username, discriminator, nick, roles, avatar, id_num)
    )
    guild._add_member(member)
    return member


def make_message(content, author, channel, pinned=False, id_num=-1):
    if id_num == -1:
        id_num = make_id()
    author = make_member_dict(author.name, author.discriminator, author.nick, author.roles, author.avatar, author.id)
    return discord.Message(
        state=test_state,
        channel=channel,
        data={
            'content': content,
            'author': author,
            'pinned': pinned,
            'id': id_num
        }
    )


async def make_context(callback, message, bot):
    view = dview.StringView(message.content)
    ctx = FakeContext(callback=callback, prefix=None, view=view, bot=bot, message=message)

    if bot._skip_check(message.author.id, test_state.user.id):
        return ctx

    prefix = bot.DEFAULT_PREFIX
    invoked_prefix = prefix

    if isinstance(prefix, str):
        if not view.skip_string(prefix):
            return ctx
    else:
        invoked_prefix = discord.utils.find(view.skip_string, prefix)
        if invoked_prefix is None:
            return ctx

    invoker = view.get_word()
    ctx.invoked_with = invoker
    ctx.prefix = invoked_prefix
    ctx.command = bot.all_commands.get(invoker)
    return ctx


def main():
    print(make_id())

    d_user = make_user("Test", "0001")

    d_guild = make_guild("Test_Guild")

    d_channel = make_text_channel("Channel 1", d_guild)

    d_member = make_member("Test", "0001", d_guild)

    print(d_member)


if __name__ == "__main__":
    main()