import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
poop_counts = {}

# 你的 Discord 使用者 ID（只有你能使用 /set 指令）
BOT_OWNER_ID = 739297622204088360

# 你的伺服器 ID（立即同步 slash 指令）
GUILD_ID = 1357348274159354136
GUILD_OBJECT = discord.Object(id=GUILD_ID)

# ====== 事件：Bot 啟動 ======
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

    try:
        # 只註冊到特定伺服器（避免重複）
        bot.tree.clear_commands()  # 清除原本所有註冊（避免殘留）
        await bot.tree.sync(guild=GUILD_OBJECT)
        print("✅ Slash 指令已同步到你的伺服器（不含全域）！")
    except Exception as e:
        print(f"❌ 同步失敗: {e}")

# ====== 事件：收到訊息時的處理 ======
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)

    # 💩 統計
    if '💩' in message.content:
        poop_counts[user_id] = poop_counts.get(user_id, 0) + message.content.count('💩')
        await message.channel.send(f"<@{user_id}> 你這個月已經拉了 {poop_counts[user_id]} 次 💩！")

    # 問號圖片回應
    if "？" in message.content or "?" in message.content:
        embed = discord.Embed(title="你問號了嗎？")
        embed.set_image(url="https://img12.pixhost.to/images/1542/585916625_d0ef2a7e-cafa-4635-b163-87e0101169c0.jpg")
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# ====== Slash 指令：排行榜 ======
@bot.tree.command(name="all", description="查看 💩 傳送次數排行榜", guild=GUILD_OBJECT)
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

# ====== Slash 指令：重置統計 ======
@bot.tree.command(name="reset", description="重置所有 💩 統計資料", guild=GUILD_OBJECT)
async def reset_command(interaction: discord.Interaction):
    poop_counts.clear()
    await interaction.response.send_message("所有 💩 統計已重置！")

# ====== Slash 指令：顯示使用者 ID ======
@bot.tree.command(name="whoami", description="顯示你的 Discord 使用者 ID（除錯用）", guild=GUILD_OBJECT)
async def whoami_command(interaction: discord.Interaction):
    await interaction.response.send_message(f"你的使用者 ID 是：`{interaction.user.id}`", ephemeral=True)

# ====== Slash 指令：設定使用者次數（限本人） ======
@bot.tree.command(name="set", description="設定使用者的 💩 次數（僅限擁有者）", guild=GUILD_OBJECT)
@app_commands.describe(user="要設定的使用者", count="次數")
async def set_command(interaction: discord.Interaction, user: discord.User, count: int):
    if interaction.user.id != BOT_OWNER_ID:
        await interaction.response.send_message("你沒有權限使用這個指令！", ephemeral=True)
        return

    poop_counts[str(user.id)] = count
    await interaction.response.send_message(f"✅ 已將 <@{user.id}> 的 💩 次數設為 {count} 次！")

# 啟動 Bot（從 .env 載入 token）
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
