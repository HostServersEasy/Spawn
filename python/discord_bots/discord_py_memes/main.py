import asyncio
import logging
import os

import requests
from discord import Embed, Intents
from discord.ext import commands, tasks

from config import get_config

SETTINGS = get_config()

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("discord_py_memes")


def _resolve_channel_config():
    """Resolve a channel lookup strategy from config."""
    channel_settings = SETTINGS.get("MEMES_CHANNEL", {})

    channel_id = channel_settings.get("id")
    if isinstance(channel_id, int) and channel_id > 0:
        return "id", channel_id

    channel_name = channel_settings.get("name")
    if isinstance(channel_name, str) and channel_name.strip():
        return "name", channel_name.strip()

    raise ValueError("MEMES_CHANNEL must have a valid positive id or a non-empty name.")


class MemeBot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        super().__init__(
            command_prefix="meme!",
            description=(
                "A Discord meme bot that posts memes on a timer and on-demand with meme!now."
            ),
            intents=intents,
        )

        lookup_mode, lookup_value = _resolve_channel_config()
        self.channel_lookup_mode = lookup_mode
        self.channel_lookup_value = lookup_value
        self.server_id = SETTINGS.get("SERVER")

    async def setup_hook(self):
        self.post_meme_loop.start()

    async def on_ready(self):
        LOGGER.info("Logged in as %s (%s)", self.user, self.user.id)

    async def _get_target_channel(self):
        guild = self.get_guild(self.server_id)
        if guild is None:
            try:
                guild = await self.fetch_guild(self.server_id)
            except Exception as exc:  # discord throws different API exceptions
                LOGGER.error("Unable to find guild %s: %s", self.server_id, exc)
                return None

        if self.channel_lookup_mode == "id":
            channel = guild.get_channel(self.channel_lookup_value)
            if channel is None:
                try:
                    channel = await self.fetch_channel(self.channel_lookup_value)
                except Exception as exc:
                    LOGGER.error(
                        "Unable to find configured channel id %s: %s",
                        self.channel_lookup_value,
                        exc,
                    )
                    return None
            return channel

        return next(
            (c for c in guild.text_channels if c.name == self.channel_lookup_value),
            None,
        )

    async def _request_meme(self):
        endpoint = SETTINGS["API"]["ENDPOINT"]

        def do_request():
            response = requests.get(endpoint, timeout=10)
            response.raise_for_status()
            return response.json()

        payload = await asyncio.to_thread(do_request)
        if "image" not in payload and "url" not in payload:
            raise ValueError("Meme API response must include an 'image' or 'url' field.")
        return payload

    async def _send_meme(self, channel):
        meme = await self._request_meme()
        image_url = meme.get("image") or meme.get("url")
        title = meme.get("title", "Random meme")
        post_url = meme.get("postLink") or meme.get("link")

        embed = Embed(title=title)
        embed.set_image(url=image_url)
        if post_url:
            embed.url = post_url
        if meme.get("subreddit"):
            embed.set_footer(text=f"r/{meme['subreddit']}")

        await channel.send(embed=embed)

    @tasks.loop(seconds=SETTINGS["INTERVAL"])
    async def post_meme_loop(self):
        channel = await self._get_target_channel()
        if channel is None:
            LOGGER.warning("Configured target channel was not found; skipping meme post.")
            return

        try:
            await self._send_meme(channel)
            LOGGER.info("Posted scheduled meme to #%s", channel.name)
        except Exception as exc:
            LOGGER.error("Failed to post scheduled meme: %s", exc)

    @post_meme_loop.before_loop
    async def before_post_meme_loop(self):
        await self.wait_until_ready()


bot = MemeBot()


@bot.command(name="now")
async def send_meme_now(ctx):
    """Send a meme instantly in the current channel."""
    try:
        await bot._send_meme(ctx.channel)
    except Exception as exc:
        await ctx.reply(f"I couldn't fetch a meme right now: {exc}")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN") or SETTINGS.get("TOKEN")
    if not token:
        raise ValueError("Set TOKEN in config.py or define DISCORD_TOKEN in the environment.")
    bot.run(token)
