import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

poop_counts = {}  # 用來記錄每個使用者傳了多少次

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)

    if '💩' in message.content:  # 💩 emoji unicode
        poop_counts[user_id] = poop_counts.get(user_id, 0) + message.content.count('💩')
        await message.channel.send(f"<@{user_id}> 你這個月已經拉了  {poop_counts[user_id]}  次 💩！")

    await bot.process_commands(message)

@bot.command()
async def all(ctx):
    if not poop_counts:
        await ctx.send("目前沒有任何統計數據！")
        return

    # 按次數排序（由多到少）
    sorted_counts = sorted(poop_counts.items(), key=lambda x: x[1], reverse=True)

    embed = discord.Embed(
        title="💩 傳送次數排行榜",
        color=discord.Color.orange()
    )

    rank_emojis = ["🥇", "🥈", "🥉"]

    description_lines = []
    for idx, (user_id, count) in enumerate(sorted_counts, start=1):
        user_mention = f"<@{user_id}>"
        emoji = rank_emojis[idx - 1] if idx <= 3 else f"#{idx}"
        description_lines.append(f"{emoji} {user_mention}：{count} 次")

    embed.description = "\n".join(description_lines)
    await ctx.send(embed=embed)


@bot.command()
async def reset(ctx):
    poop_counts.clear()
    await ctx.send("所有 💩 統計已重置！")

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
