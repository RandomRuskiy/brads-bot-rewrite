import os
from importlib import import_module
from pathlib import Path
import logging

import hikari
import lightbulb


def create_bot() -> lightbulb.Bot:
    token = os.getenv("TOKEN")

    # Create the main bot instance with all intents.
    bot = lightbulb.command_handler.Bot(token=token,
                                        prefix="!",
                                        intents=hikari.Intents.ALL,
                                        logs="DEBUG"
                                        )

    # Gather all slash command files.
    commands = Path("./commands").glob("*.py")
    print(f'yo: {commands}')

    # Load each slash command extension into the bot.
    for c in commands:
        bot.load_extension(f"commands.{c.stem}")

    return bot


if __name__ == "__main__":
    if os.name != "nt":

        import uvloop

        uvloop.install()

    # Create and run the bot.
    create_bot().run()
