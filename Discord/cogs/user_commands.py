"""
    User Commands cog for Talos
    Holds all user specific commands, those things that alter a user's permissions, roles,
    Talos' knowledge of them, so on.

    Author: CraftSpider
"""
import discord
import discord.ext.commands as commands
import discord.errors as errors
import logging
import asyncio
import utils
import re

log = logging.getLogger("talos.user")


def space_replace(match):
    print(match.group(1))
    if match.group(1):
        return "\\"*int(len(match.group(0)) / 2) + " "
    else:
        return " "


class UserCommands(utils.TalosCog):
    """These commands can be used by anyone, as long as Talos is awake.\n"""\
        """The effects will apply to the person using the command."""

    @commands.command(aliases=["color"], signature="colour <hex-code>", description="Set your role colour")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True)
    async def colour(self, ctx, colour):
        """Changes the User's colour, if Talos has role permissions."""\
            """ Input must be a hexadecimal colour or the word 'clear' to remove all Talos colours."""
        # If we want to remove Talos Colour
        if colour == "clear":
            for role in ctx.author.roles:
                if role.name.startswith("<TALOS COLOR>") or role.name.startswith("LOPEZ COLOR:"):
                    await ctx.author.remove_roles(role)
                    if not len(role.members):
                        await role.delete()
            await ctx.send("Talos colour removed")
            return

        if not colour.startswith("#") or len(colour) is not 7 and len(colour) is not 4:
            await ctx.send("That isn't a valid hexadecimal colour!")
            return

        for role in ctx.author.roles:
            if role.name.startswith("<TALOS COLOR>") or role.name.startswith("LOPEZ COLOR:"):
                await ctx.author.remove_roles(role)
                if not len(role.members):
                    await role.delete()

        # Convert to hexadecimal number
        discord_colour = None
        try:
            if len(colour) == 7:
                discord_colour = discord.Colour(int(colour[1:], 16))
            elif len(colour) == 4:
                colour = colour[1:]
                result = ""
                for item in colour:
                    result += item*2
                discord_colour = discord.Colour(int(result, 16))
                colour = "#{}".format(result)
        except ValueError:
            await ctx.send("That isn't a valid hexadecimal colour!")
            return

        # Find and add or create and add the role.
        colour_role = discord.utils.find(lambda x: x.name.startswith("<TALOS COLOR>") and x.colour == discord_colour,
                                         ctx.guild.roles)
        if colour_role is not None:
            await ctx.author.add_roles(colour_role)
        else:
            colour_role = await ctx.guild.create_role(name="<TALOS COLOR>", colour=discord_colour)
            try:
                await asyncio.sleep(.1)
                try:
                    await colour_role.edit(position=(ctx.guild.me.top_role.position - 1))
                except errors.HTTPException:
                    pass
            except discord.errors.InvalidArgument as e:
                log.error(e.__cause__)
                log.error(e.args)
            await ctx.author.add_roles(colour_role)

        await ctx.send("{0.name}'s colour changed to {1}!".format(ctx.message.author, colour))

    @commands.command(description="Display current guild perms")
    @commands.guild_only()
    async def my_perms(self, ctx):
        """Has Talos display your current effective guild permissions. This is channel independent, channel-specific"""\
            """ perms aren't taken into account."""
        out = "```Guild Permissions:\n"
        out += ', '.join(map(lambda x: x[0], filter(lambda y: y[1] is True, ctx.author.guild_permissions)))
        out += "```"
        await ctx.send(out)

    @commands.command(description="User registration command")
    async def register(self, ctx):
        """Registers you as a user with Talos. This creates a profile and options for you, and allows Talos to """\
            """save info."""
        if not self.database.get_user(ctx.author.id):
            self.database.register_user(ctx.author.id)
            await ctx.send("Registered new user!")
        else:
            await ctx.send("You're already a registered user.")

    @commands.command(description="User deletion command")
    async def deregister(self, ctx):
        """Deregisters you from Talos. All collected data is wiped, no account info will be saved until """\
            """you re-register."""
        if self.database.get_user(ctx.author.id):
            self.database.deregister_user(ctx.author.id)
            await ctx.send("Deregistered user")
        else:
            raise utils.NotRegistered(ctx.author)

    @commands.command(description="Display a user profile")
    async def profile(self, ctx, user: discord.User=None):
        """Displays you or another user's profile, if it exists. Defaults to your own profile, but accepts the name """\
            """of a user to display instead."""
        if user is None:
            user = ctx.author
        profile = self.database.get_user(user.id)
        if not profile:
            raise utils.NotRegistered(user)
        favorite_command = profile.get_favorite_command()
        if self.bot.should_embed(ctx):
            with utils.PaginatedEmbed() as embed:
                embed.title = profile.cur_title
                embed.description = profile.description if profile.description else "User has not set a description"
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                value = "Total Invoked Commands: {0}\nFavorite Command: `{1[0]}`, invoked {1[1]} times.".format(
                    profile.total_commands, favorite_command
                )
                embed.add_field(name="Command Stats", value=value)
            for page in embed:
                await ctx.send(embed=page)
        else:
            out = "```md\n"
            out += "{}\n".format(user.name)
            out += "{}\n".format(profile.description if profile.description else "User has not set a description")
            out += "# Command Stats:\n"
            out += "-  Total Invoked: {}\n".format(profile.total_commands)
            out += "-  Favorite Command: {0[0]}, invoked {0[1]} times.".format(favorite_command)
            out += "```"
            await ctx.send(out)

    @commands.group(description="For checking or setting your own profile")
    async def user(self, ctx):
        """Options will show current user options, stats will display what Talos has saved about you, description """\
            """will set your user description, set will set user options, and remove will clear user options."""
        if not self.database.get_user(ctx.author.id):
            raise utils.NotRegistered(ctx.author)
        elif ctx.invoked_subcommand is None:
            await ctx.send("Valid options are 'options', 'stats', 'title', 'description', 'set', and 'remove'")
            return

    @user.command(name="title", description="List or set your title(s)")
    async def _title(self, ctx, title=""):
        """If given no arguments will list your available titles, if given a title will make that your title if you
        own that title."""
        if title:
            pass
            result = self.database.set_title(ctx.author.id, title)
            if result:
                await ctx.send("Title successfully set to `{}`".format(title))
            else:
                await ctx.send("You do not have that title")
        else:
            profile = self.database.get_user(ctx.author.id)
            titles = profile.titles
            if len(titles) == 0:
                await ctx.send("No available titles")
                return
            out = "```"
            for title in titles:
                out += title[0] + "\n"
            out += "```"
            await ctx.send(out)

    @user.command(name="options", description="List your current user options")
    async def _options(self, ctx):
        """Currently available user options:
        rich_embeds: whether Talos will embed messages for you if guild options allow it
        prefix: what prefix Talos will use in PMs with you"""
        out = "```"
        options = self.database.get_user_options(ctx.author.id)
        for item in options.__slots__[2:]:
            out += "{}: {}\n".format(item, getattr(options, item))
        out += "```"
        if out == "``````":
            await ctx.send("No options available.")
            return
        await ctx.send(out)

    @user.command(name="stats", description="List your current user stats")
    async def _stats(self, ctx):
        """Will show just about everything Talos knows about you."""
        profile = self.database.get_user(ctx.author.id)
        if profile is None:
            await ctx.send("No profile found, please register.")
            return
        out = "```"
        out += "Desc: {}\n".format(profile.description)
        out += "Total Invoked: {}\n".format(profile.total_commands)
        out += "Command Stats:\n"
        for command in profile.invoked_data:
            out += "    {}: {}\n".format(command[0], command[1])
        out += "```"
        await ctx.send(out)

    @user.command(name="description", description="Set your user description")
    async def _description(self, ctx, *, text):
        """Change what the user description on your profile is. Max size of 2048 characters."""
        self.database.set_description(ctx.author.id, text)
        await ctx.send("Description set.")

    @user.command(name="set", description="Set your user options")
    async def _set(self, ctx, option, value):
        """Set user options for your account. See `^help user options` for available options."""
        try:
            option_type = self.database.get_column_type("user_options", option)
        except ValueError:
            await ctx.send("Eh eh eh, letters and numbers only.")
            return
        if option_type == "tinyint":
            if value.upper() == "ALLOW" or value.upper() == "TRUE":
                value = True
            elif value.upper() == "FORBID" or value.upper() == "FALSE":
                value = False
            else:
                await ctx.send("Sorry, that option only accepts true or false values.")
                return
        if option_type == "varchar":
            value = re.sub(r"(?<!\\)\\((?:\\\\)*)s", space_replace, value)
            value = re.sub(r"\\\\", r"\\", value)
        if option_type is not None:
            self.database.set_user_option(ctx.author.id, option, value)
            await ctx.send("Option {} set to `{}` for {}".format(option, value, ctx.author.display_name))
        else:
            await ctx.send("I don't recognize that option.")

    @user.command(name="remove", description="Set a user option to default")
    async def _remove(self, ctx, option):
        """Reset a user option to default. See `^help user options` for available options."""
        try:
            data_type = self.database.get_column_type("user_options", option)
        except ValueError:
            await ctx.send("Eh eh eh, letters and numbers only.")
            return
        if data_type is not None:
            self.database.remove_user_option(ctx.author.id, option)
            await ctx.send("Option {} set to default for {}".format(option, ctx.author.display_name))
        else:
            await ctx.send("I don't recognize that option.")

    
def setup(bot):
    bot.add_cog(UserCommands(bot))
