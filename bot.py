import discord
import wavelink
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents, command_prefix=commands.when_mentioned)

    async def setup_hook(self) -> None:
        await self.load_extension("cogs.channels")
        await self.load_extension("cogs.lofi")
        await self.load_extension("jishaku")

        # await self.tree.sync()

        nodes = [
            wavelink.Node(uri=host, password=password, secure=True)
            for host, password in {
                "lavalink.ordinaryender.my.eu.org": "ordinarylavalink"
            }.items()
        ]
        await wavelink.NodePool.connect(client=self, nodes=nodes)


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    Bot().run(os.environ["TOKEN"])
