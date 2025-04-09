import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
poop_counts = {}

BOT_OWNER_ID = 123456789012345678 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)

    if '💩' in message.content:
        poop_counts[user_id] = poop_counts.get(user_id, 0) + message.content.count('💩')
        await message.channel.send(f"<@{user_id}> 你這個月已經拉了  {poop_counts[user_id]}  次 💩！")

    if message.content.strip() == "？":
       await message.channel.send("", embed=discord.Embed().set_image(url="https://img12.pixhost.to/images/1542/585916625_d0ef2a7e-cafa-4635-b163-87e0101169c0.jpg"))
    if message.content.strip() == "?":
       await message.channel.send("", embed=discord.Embed().set_image(url="https://img12.pixhost.to/images/1542/585916625_d0ef2a7e-cafa-4635-b163-87e0101169c0.jpg"))
    await bot.process_commands(message)


@bot.tree.command(name="all", description="查看 💩 傳送次數排行榜")
async def all_command(interaction: discord.Interaction):
    if not poop_counts:
        await interaction.response.send_message("目前沒有任何統計數據！", ephemeral=True)
        return

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
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset", description="重置所有 💩 統計資料")
async def reset_command(interaction: discord.Interaction):
    poop_counts.clear()
    await interaction.response.send_message("所有 💩 統計已重置！")

@bot.tree.command(name="set", description="設定特定使用者的 💩 次數（僅限擁有者使用）")
@app_commands.describe(user="要設定的使用者", count="次數")
async def set_command(interaction: discord.Interaction, user: discord.User, count: int):
    if interaction.user.id != BOT_OWNER_ID:
        await interaction.response.send_message("你沒有權限使用這個指令！", ephemeral=True)
        return

    poop_counts[str(user.id)] = count
    await interaction.response.send_message(f"已將 <@{user.id}> 的 💩 次數設為 {count} 次！")
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
