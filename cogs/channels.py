from __future__ import annotations

from typing import TYPE_CHECKING

import discord
import wavelink
from discord.ext import commands

if TYPE_CHECKING:
    from bot import Bot


class Channels(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        if member == self.bot.user:
            return

        if (
            after.channel is None
            and before.channel == before.channel.guild.voice_client.channel
            and len(before.channel.members) <= 0
        ):
            await before.channel.guild.voice_client.disconnect()

            if view := getattr(before.channel.guild.voice_client, "view", None):
                view.stop()

    @commands.hybrid_group()
    async def channel(self, ctx: commands.Context[Bot]) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @channel.command(description="Make me join you")
    @commands.guild_only()
    async def join(self, ctx: commands.Context[Bot]) -> None:
        if ctx.voice_client:
            await ctx.send(f"I'm already in {ctx.voice_client.channel.mention}")
            return

        if ctx.author.voice is None:
            await ctx.send("Join a voice channel first.")
            return

        await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.send("I'm with you now.")

    @channel.command(description="Make me leave you")
    @commands.guild_only()
    async def leave(self, ctx: commands.Context[Bot]) -> None:
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel.")
            return

        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("You need to be in my voice channel to make me leave.")
            return

        await ctx.voice_client.disconnect()
        await ctx.send("I left you now.")


async def setup(bot: Bot) -> None:
    await bot.add_cog(Channels(bot))
