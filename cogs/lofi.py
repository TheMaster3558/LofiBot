from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Self

import discord
import wavelink
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Bot

STREAMS = {
    "relax_and_study": "lofi hip hop radio 📚 - beats to relax/study to",
    "chill_and_game": "synthwave radio 🌌 - beats to chill/game to",
    "sleep_and_chill": "lofi hip hop radio 💤 - beats to sleep/chill to",
}


class Controls(discord.ui.View):
    def __init__(self, player: wavelink.Player) -> None:
        self.player = player
        player.view = self
        super().__init__(timeout=None)

    async def edit_volume_button(self, interaction: discord.Interaction[Bot]) -> None:
        self.volume.label = f"{self.player.volume // 4}%"
        await interaction.message.edit(view=self)

    @discord.ui.button(emoji="🔉")
    async def decrease_volume(
        self, interaction: discord.Interaction[Bot], button: discord.ui.Button[Self]
    ) -> None:
        await interaction.response.defer()
        await self.player.set_volume(self.player.volume - 20)
        if self.player.volume <= 0:
            button.disabled = True
        else:
            button.disabled = False
        await self.edit_volume_button(interaction)

    @discord.ui.button(label="50%")
    async def volume(
        self, interaction: discord.Interaction[Bot], button: discord.ui.Button[Self]
    ) -> None:
        pass

    @discord.ui.button(emoji="🔊")
    async def increase_volume(
        self, interaction: discord.Interaction[Bot], button: discord.ui.Button[Self]
    ) -> None:
        await interaction.response.defer()
        await self.player.set_volume(self.player.volume + 20)
        if self.player.volume >= 400:
            button.disabled = True
        else:
            button.disabled = False
        await self.edit_volume_button(interaction)


async def play(ctx: commands.Context[Bot], query: str) -> None:
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            await ctx.send("Join a voice channel first.")
            return
    else:
        if (
            ctx.author.voice is not None
            and ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("Join my channel.")
            return

    await ctx.voice_client.set_volume(200)

    tracks = await wavelink.YouTubeTrack.search(query)
    await ctx.voice_client.play(tracks[0])

    embed = discord.Embed(title=f"Playing {tracks[0].title}").set_image(
        url=tracks[0].thumbnail
    )
    await ctx.send(embed=embed, view=Controls(ctx.voice_client))


class Lofi(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        description="lofi hip hop radio 📚 - beats to relax/study to"
    )
    async def relax_and_study(self, ctx: commands.Context[Bot]) -> None:
        await play(ctx, "https://www.youtube.com/watch?v=jfKfPfyJRdk")

    @commands.hybrid_command(description="synthwave radio 🌌 - beats to chill/game to")
    async def chill_and_game(self, ctx: commands.Context[Bot]) -> None:
        await play(ctx, "https://www.youtube.com/watch?v=4xDzrJKXOOY")

    @commands.hybrid_command(
        description="lofi hip hop radio 💤 - beats to sleep/chill to"
    )
    async def sleep_and_chill(self, ctx: commands.Context[Bot]) -> None:
        await play(ctx, "https://www.youtube.com/watch?v=rUxyKA_-grg")


async def setup(bot: Bot) -> None:
    await bot.add_cog(Lofi(bot))
