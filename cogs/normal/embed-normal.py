import discord
import random
from discord.ext import commands


# Cogs for Embed-Related command
def random_color():
    hex_chars = '0123456789abcdef'
    color = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
    return color


def hex_to_int(hex_color):
    return int(hex_color[1:], 16)


class Embed(commands.Cog, name="embed-normal"):
    def __init__(self, bot):
        self.bot = bot

    # Commands list
    @commands.command(
        name="embed",
        description="add embed"
    )
    async def embed(self, ctx, *args):
        title = None
        desc = None
        thumb = None
        image = None
        footer = None
        url = None
        color = None
        is_clean = False
        for i in range(len(args)-1):
            if args[i] == '-title':
                title = args[i+1]
            elif args[i] == '-desc':
                desc = args[i+1]
            elif args[i] == '-thumb':
                thumb = args[i+1]
            elif args[i] == '-image':
                image = args[i+1]
            elif args[i] == '-footer':
                footer = args[i+1]
            elif args[i] == '-url':
                url = args[i+1]
            elif args[i] == '-color':
                color = args[i+1]
            elif args[i] == '-clean':
                is_clean = True

        if color is None:
            color = random_color()

        author = ctx.message.author
        embed = discord.Embed(
            title=title,
            description=desc,
            url=url,
            color=discord.Color(hex_to_int(color))
        )
        if footer is not None:
            embed.set_footer(text=footer)
        if thumb is not None:
            embed.set_thumbnail(url=thumb)
        if image is not None:
            embed.set_image(url=image)
        if not is_clean:
            embed.set_author(name=author.display_name, icon_url=author.display_avatar)
        await ctx.send(embed=embed)

    # -----

    # Non-commands method

    # -----


# cog setup
def setup(bot):
    bot.add_cog(Embed(bot))
