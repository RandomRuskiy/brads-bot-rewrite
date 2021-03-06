import datetime as dt
import typing as t

import hikari
import lightbulb
from lightbulb import slash_commands

from __init__ import GUILD_ID


class Userinfo(slash_commands.SlashCommand):
    description: str = "Get info on a server member."
    enabled_guilds: t.Optional[t.Iterable[int]] = (GUILD_ID,)
    options: list[hikari.CommandOption] = [
        hikari.CommandOption(
            name="target",
            description="The member to get information about.",
            type=hikari.OptionType.USER,
            is_required=True,
        ),
    ]

    async def callback(self, ctx) -> None:
        # Convert the return value to a Member object.
        target = ctx.guild.get_member(int(ctx.option_values.target))
        if not target:
            await ctx.respond("That user is not in the server.")
            return

        created_at = int(target.created_at.timestamp())
        joined_at = int(target.joined_at.timestamp())
        roles = (await target.fetch_roles())[1:]  # All but @everyone.

        # Function calls can be chained when creating embeds.
        embed = (
            hikari.Embed(
                title="User information",
                description=f"ID: {target.id}",
                colour=hikari.Colour(0x563275),
                # Doing it like this is important.
                timestamp=dt.datetime.now().astimezone(),
            )
            .set_author(name="Information")
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            .set_thumbnail(target.avatar_url)
            # These are just a number of example fields.
            .add_field(name="Discriminator", value=target.discriminator, inline=True)
            .add_field(name="Bot?", value=target.is_bot, inline=True)
            .add_field(name="No. of roles", value=len(roles), inline=True)
            .add_field(
                name="Created on",
                value=f"<t:{created_at}:d> (<t:{created_at}:R>)",
                inline=False,
            )
            .add_field(
                name="Joined on",
                value=f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
                inline=False,
            )
            .add_field(name="Roles", value=" | ".join(r.mention for r in roles))
        )

        # To send a message, use ctx.respond. Using kwargs, you can make the
        # bot reply to a message (when not send from a slash command
        # invocation), allow mentions, make the message ephemeral, etc.
        await ctx.respond(embed)


def load(bot: lightbulb.Bot):
    bot.add_slash_command(Userinfo)


def unload(bot: lightbulb.Bot):
    bot.remove_slash_command("userinfo")
