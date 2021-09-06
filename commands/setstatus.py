import typing as t

import hikari
import lightbulb
from lightbulb import slash_commands

from __init__ import GUILD_ID


class SetStatus(slash_commands.SlashCommand):
    description = str = "Set the bot's status!"
    enabled_guilds: t.Optional[t.Iterable[int]] = (GUILD_ID,)
    options: list[hikari.CommandOption] = [
        hikari.CommandOption(
            name="status",
            description="The status you want the bot to have.",
            type=hikari.OptionType.STRING,
            is_required=True
        ),
    ]

    async def callback(self, ctx) -> None:
        await lightbulb.Bot.update_presence(
            self,
            activity=hikari.Activity(
                type=hikari.ActivityType.PLAYING,
                name=ctx.option_values.status
            )
        )
        await ctx.respond(f"yo my status is now: **{ctx.option_values.status}**")


def load(bot: lightbulb.Bot):
    bot.add_slash_command(SetStatus)


def unload(bot: lightbulb.Bot):
    bot.remove_slash_command("setstatus")
