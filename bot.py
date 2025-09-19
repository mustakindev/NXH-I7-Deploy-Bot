import discord
from discord import app_commands
from discord.ext import commands
import docker
import yaml
import os
import random
import asyncio
import requests
from typing import Optional, Literal

# Cute emojis for flair
EMOJIS = "🌸✨💎🎀⚡🖤🌐🌙⭐🐳🪐🎉🔮🧩🏆🚀🎶💫🌈"

# Load config
with open("config.yml", "r") as f:
    CONFIG = yaml.safe_load(f)

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Docker client
client = docker.from_env()

# Database functions
def load_db():
    if not os.path.exists("database.txt"):
        open("database.txt", "w").close()
    with open("database.txt", "r") as f:
        lines = f.read().strip().split("\n")
        db = {}
        for line in lines:
            if not line: continue
            parts = line.split("|")
            if len(parts) < 3: continue
            userid, container_id, ssh_cmd = parts
            db[userid] = {"container_id": container_id, "ssh_cmd": ssh_cmd}
        return db

def save_db(db):
    with open("database.txt", "w") as f:
        for userid, data in db.items():
            f.write(f"{userid}|{data['container_id']}|{data['ssh_cmd']}\n")

# Mock invite/boost tracker (replace with real logic)
async def get_user_invites(user_id: int) -> int:
    # Simulate invite count — replace with real tracking system
    return random.randint(0, 20)

async def get_user_boosts(guild: discord.Guild, user_id: int) -> int:
    member = guild.get_member(user_id)
    if not member: return 0
    return member.premium_since is not None and 1 or 0  # Simplified — track actual boosts

# Generate Tmate SSH session (mock)
def generate_tmate_session():
    # In real use: spawn container → run tmate → capture SSH
    # Here, we mock it
    return f"ssh {random.randint(1000,9999)}@n1.nxh.cloud -p 2222"

# Deploy VPS container (mock)
def deploy_vps_container(ram: str, cores: int, disk: str) -> str:
    # In real use: docker run with resource limits + tmate preinstalled
    # Here, mock container ID
    container_id = f"nxh-{random.randint(10000, 99999)}"
    return container_id

# Slash command: /createvps
class VPSPlanDropdown(discord.ui.Select):
    def __init__(self, user, guild):
        self.user = user
        self.guild = guild
        options = [
            discord.SelectOption(label="🌸 Starter (6 INV)", description="8GB RAM, 5 CORE, 10GB DISK", emoji="🌸"),
            discord.SelectOption(label="✨ PlansNamePLS (10 INV)", description="14GB RAM, 6 CORE, 30GB DISK", emoji="✨"),
            discord.SelectOption(label="💎 Premium (15 INV)", description="16GB RAM, 7 CORE, 50GB DISK", emoji="💎"),
            discord.SelectOption(label="🎀 1 BOOST", description="12GB RAM, 5 CORE, 30GB DISK", emoji="🎀"),
            discord.SelectOption(label="⚡ 2 BOOSTS", description="16GB RAM, 6 CORE, 40GB DISK", emoji="⚡"),
        ]
        super().__init__(placeholder="Select your VPS plan...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        plan_name = self.values[0]
        db = load_db()

        # Check if user already has VPS
        if str(self.user.id) in db:
            await interaction.response.send_message("🚫 You already have a VPS! Use `/manage` to control it.", ephemeral=True)
            return

        # Parse plan
        invites_needed = 0
        boosts_needed = 0
        ram = cores = disk = None

        if "Starter" in plan_name:
            invites_needed = 6
            ram, cores, disk = "8GB", 5, "10GB"
        elif "PlansNamePLS" in plan_name:
            invites_needed = 10
            ram, cores, disk = "14GB", 6, "30GB"
        elif "Premium" in plan_name:
            invites_needed = 15
            ram, cores, disk = "16GB", 7, "50GB"
        elif "1 BOOST" in plan_name:
            boosts_needed = 1
            ram, cores, disk = "12GB", 5, "30GB"
        elif "2 BOOSTS" in plan_name:
            boosts_needed = 2
            ram, cores, disk = "16GB", 6, "40GB"

        # Check invites/boosts
        invites = await get_user_invites(self.user.id)
        boosts = await get_user_boosts(self.guild, self.user.id)

        if invites_needed > 0 and invites < invites_needed:
            await interaction.response.send_message(f"🌸 You need {invites_needed} invites! You have {invites}.", ephemeral=True)
            return
        if boosts_needed > 0 and boosts < boosts_needed:
            await interaction.response.send_message(f"🎀 You need {boosts_needed} server boosts! You have {boosts}.", ephemeral=True)
            return

        # Deploy VPS
        container_id = deploy_vps_container(ram, cores, disk)
        ssh_cmd = generate_tmate_session()

        # Save to DB
        db[str(self.user.id)] = {"container_id": container_id, "ssh_cmd": ssh_cmd}
        save_db(db)

        # DM user
        try:
            embed = discord.Embed(
                title="🪄 Your VPS is Ready!",
                description=f"```{ssh_cmd}```",
                color=0x9d5dfa
            )
            embed.add_field(name="📦 Plan", value=plan_name, inline=False)
            embed.add_field(name="🧠 RAM", value=ram, inline=True)
            embed.add_field(name="⚙️ Cores", value=cores, inline=True)
            embed.add_field(name="💾 Disk", value=disk, inline=True)
            embed.set_footer(text="Use /manage to control your VPS anytime 💫")
            embed.set_thumbnail(url="https://i.imgur.com/MbGZQdY.png")  # Replace with cute cloud icon

            await self.user.send(embed=embed)
            await interaction.response.send_message("✅ VPS deployed! Check your DMs for SSH access 🌈", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ I can't DM you! Please enable DMs from server members.", ephemeral=True)

class VPSPlanView(discord.ui.View):
    def __init__(self, user, guild):
        super().__init__(timeout=180)
        self.add_item(VPSPlanDropdown(user, guild))

@bot.tree.command(name="createvps", description="Create your own VPS with invites or boosts!")
async def createvps(interaction: discord.Interaction):
    view = VPSPlanView(interaction.user, interaction.guild)
    embed = discord.Embed(
        title="☁️ Create Your VPS",
        description="Select a plan below to deploy your cloud instance!",
        color=0x7289da
    )
    embed.set_thumbnail(url="https://i.imgur.com/0QzJZ7P.png")  # Cute cloud
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# /plans
@bot.tree.command(name="plans", description="View all available VPS plans")
async def plans(interaction: discord.Interaction):
    embed = discord.Embed(title="💎 VPS Plans", color=0x9b59b6)
    embed.add_field(
        name="🌸 Invite Plans",
        value=(
            "```"
            "Starter → 6 INV = 8GB RAM, 5 CORE, 10GB DISK\n"
            "PlansNamePLS → 10 INV = 14GB RAM, 6 CORE, 30GB DISK\n"
            "Premium → 15 INV = 16GB RAM, 7 CORE, 50GB DISK"
            "```"
        ),
        inline=False
    )
    embed.add_field(
        name="🎀 Boost Plans",
        value=(
            "```"
            "1 BOOST = 12GB RAM, 5 CORE, 30GB DISK\n"
            "2 BOOSTS = 16GB RAM, 6 CORE, 40GB DISK"
            "```"
        ),
        inline=False
    )
    embed.set_footer(text="Use /createvps to get started! 🚀")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /manage
class ManageVPSView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=300)
        self.user_id = str(user_id)

    @discord.ui.button(label="Start", emoji="🟢", style=discord.ButtonStyle.green)
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🟢 Starting VPS... (mock)", ephemeral=True)

    @discord.ui.button(label="Stop", emoji="🔴", style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔴 Stopping VPS... (mock)", ephemeral=True)

    @discord.ui.button(label="Reinstall", emoji="♻️", style=discord.ButtonStyle.gray)
    async def reinstall_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("♻️ Reinstalling OS... (mock)", ephemeral=True)

    @discord.ui.button(label="Re-SSH", emoji="🔑", style=discord.ButtonStyle.blurple)
    async def ressh_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        db = load_db()
        if self.user_id not in db:
            await interaction.response.send_message("❌ No VPS found.", ephemeral=True)
            return
        new_ssh = generate_tmate_session()
        db[self.user_id]["ssh_cmd"] = new_ssh
        save_db(db)
        await interaction.response.send_message(f"🔑 New SSH: ```{new_ssh}```", ephemeral=True)

@bot.tree.command(name="manage", description="Manage your VPS")
async def manage(interaction: discord.Interaction):
    db = load_db()
    if str(interaction.user.id) not in db:
        await interaction.response.send_message("❌ You don't have a VPS yet! Use `/createvps`.", ephemeral=True)
        return

    view = ManageVPSView(interaction.user.id)
    embed = discord.Embed(
        title="🎛️ VPS Control Panel",
        description="Use the buttons below to manage your cloud instance!",
        color=0x3498db
    )
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

# /stop-all
@bot.tree.command(name="stop-all", description="Stop all your VPS instances")
async def stop_all(interaction: discord.Interaction):
    # Mock — in real use, iterate containers
    await interaction.response.send_message("🔴 All your VPS stopped! (mock)", ephemeral=True)

# /list
@bot.tree.command(name="list", description="List all your VPS with specs")
async def list_vps(interaction: discord.Interaction):
    db = load_db()
    if str(interaction.user.id) not in db:
        await interaction.response.send_message("❌ You have no VPS deployed.", ephemeral=True)
        return

    data = db[str(interaction.user.id)]
    embed = discord.Embed(title="📋 Your VPS", color=0x2ecc71)
    embed.add_field(name="🆔 Container ID", value=data["container_id"], inline=False)
    embed.add_field(name="🔑 SSH Command", value=f"```{data['ssh_cmd']}```", inline=False)
    embed.set_footer(text="Use /manage for more actions 💫")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /regen-ssh
@bot.tree.command(name="regen-ssh", description="Regenerate your SSH session")
async def regen_ssh(interaction: discord.Interaction):
    db = load_db()
    user_id = str(interaction.user.id)
    if user_id not in db:
        await interaction.response.send_message("❌ No VPS found.", ephemeral=True)
        return

    new_ssh = generate_tmate_session()
    db[user_id]["ssh_cmd"] = new_ssh
    save_db(db)
    await interaction.response.send_message(f"🔑 New SSH: ```{new_ssh}```", ephemeral=True)

# Simple control commands
@bot.tree.command(name="start", description="Start your VPS")
async def start_vps(interaction: discord.Interaction):
    await interaction.response.send_message("🟢 Starting VPS... (mock)", ephemeral=True)

@bot.tree.command(name="stop", description="Stop your VPS")
async def stop_vps(interaction: discord.Interaction):
    await interaction.response.send_message("🔴 Stopping VPS... (mock)", ephemeral=True)

@bot.tree.command(name="restart", description="Restart your VPS")
async def restart_vps(interaction: discord.Interaction):
    await interaction.response.send_message("🔄 Restarting VPS... (mock)", ephemeral=True)

@bot.tree.command(name="remove", description="Delete your VPS")
async def remove_vps(interaction: discord.Interaction):
    db = load_db()
    user_id = str(interaction.user.id)
    if user_id not in db:
        await interaction.response.send_message("❌ No VPS to delete.", ephemeral=True)
        return

    # In real use: stop & remove container
    del db[user_id]
    save_db(db)
    await interaction.response.send_message("🗑️ VPS deleted successfully!", ephemeral=True)

# /help
@bot.tree.command(name="help", description="Show all commands")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="📚 NxH-i7 Help", color=0xe91e63)
    embed.add_field(
        name="🧑‍💻 User Commands",
        value="`/createvps` `/plans` `/manage` `/stop-all` `/list` `/regen-ssh` `/start` `/stop` `/restart` `/remove` `/help` `/botinfo`",
        inline=False
    )
    if str(interaction.user.id) in CONFIG["admin_ids"]:
        embed.add_field(
            name="👑 Admin Commands",
            value="`/deploy` `/suspend` `/delvps` `/killvps` `/remove-everything` `/editplans` `/sendvps` `/track-invite` `/botstatus` `/admin-help`",
            inline=False
        )
    embed.set_footer(text="Made with 💖 by Mustakin | NxH-i7 Hosting")
    await interaction.response.send_message(embed=embed, ephemeral=True)

# /botinfo
@bot.tree.command(name="botinfo", description="Show bot info")
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🪐 NxH-i7 Hosting",
        description="**Made by Mustakin**\n\n🌸 Premium Discord VPS Hosting with Tmate + Docker\n🚀 Fast, Cute, Reliable Clouds",
        color=0x9b59b6
    )
    embed.set_thumbnail(url="https://i.imgur.com/5HjYKQp.png")  # Cute bot icon
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ========== ADMIN COMMANDS ==========

def is_admin():
    async def predicate(interaction: discord.Interaction):
        return str(interaction.user.id) in CONFIG["admin_ids"]
    return app_commands.check(predicate)

@bot.tree.command(name="deploy", description="Deploy VPS with custom specs (Admin Only)")
@is_admin()
async def deploy_admin(
    interaction: discord.Interaction,
    user: discord.User,
    ram: str,
    cores: int,
    disk: str
):
    if cores > 200 or int(ram.replace("GB","")) > 200 or int(disk.replace("GB","")) > 200:
        await interaction.response.send_message("❌ Max limit is 200 per resource.", ephemeral=True)
        return

    container_id = deploy_vps_container(ram, cores, disk)
    ssh_cmd = generate_tmate_session()

    db = load_db()
    db[str(user.id)] = {"container_id": container_id, "ssh_cmd": ssh_cmd}
    save_db(db)

    try:
        embed = discord.Embed(title="👑 Admin Deployed VPS", color=0xe74c3c)
        embed.add_field(name="🧠 RAM", value=ram, inline=True)
        embed.add_field(name="⚙️ Cores", value=cores, inline=True)
        embed.add_field(name="💾 Disk", value=disk, inline=True)
        embed.add_field(name="🔑 SSH", value=f"```{ssh_cmd}```", inline=False)
        await user.send(embed=embed)
        await interaction.response.send_message(f"✅ Deployed VPS for {user.mention}!", ephemeral=True)
    except:
        await interaction.response.send_message(f"⚠️ Deployed, but couldn't DM {user.mention}.", ephemeral=True)

@bot.tree.command(name="suspend", description="Suspend user VPS (Admin Only)")
@is_admin()
async def suspend(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"⏸️ Suspended VPS for {user.mention} (mock).", ephemeral=True)

@bot.tree.command(name="delvps", description="Delete user VPS (Admin Only)")
@is_admin()
async def delvps(interaction: discord.Interaction, user: discord.User):
    db = load_db()
    user_id = str(user.id)
    if user_id not in db:
        await interaction.response.send_message("❌ User has no VPS.", ephemeral=True)
        return
    del db[user_id]
    save_db(db)
    await interaction.response.send_message(f"🗑️ Deleted VPS for {user.mention}.", ephemeral=True)

@bot.tree.command(name="killvps", description="Kill ALL VPS instantly (Admin Only)")
@is_admin()
async def killvps(interaction: discord.Interaction):
    # In real use: stop & remove all containers
    open("database.txt", "w").close()  # Wipe DB
    await interaction.response.send_message("☠️ All VPS terminated. Database wiped.", ephemeral=True)

@bot.tree.command(name="remove-everything", description="Nuclear reset — delete all VPS + DB (Admin Only)")
@is_admin()
async def remove_everything(interaction: discord.Interaction):
    # In real use: docker system prune -af
    open("database.txt", "w").close()
    await interaction.response.send_message("☢️ NODE RESET COMPLETE. All data destroyed.", ephemeral=True)

@bot.tree.command(name="editplans", description="Edit invite/boost plans (Admin Only)")
@is_admin()
async def editplans(interaction: discord.Interaction):
    await interaction.response.send_message("🛠️ Plan editor not implemented yet. Edit config.yml manually.", ephemeral=True)

@bot.tree.command(name="sendvps", description="Send VPS info to user (Admin Only)")
@is_admin()
async def sendvps(interaction: discord.Interaction, user: discord.User):
    db = load_db()
    if str(user.id) not in db:
        await interaction.response.send_message("❌ User has no VPS.", ephemeral=True)
        return

    data = db[str(user.id)]
    embed = discord.Embed(title="📬 Your VPS Info (Sent by Admin)", color=0xf1c40f)
    embed.add_field(name="🆔 Container", value=data["container_id"], inline=False)
    embed.add_field(name="🔑 SSH", value=f"```{data['ssh_cmd']}```", inline=False)
    try:
        await user.send(embed=embed)
        await interaction.response.send_message(f"✅ VPS info sent to {user.mention}.", ephemeral=True)
    except:
        await interaction.response.send_message(f"❌ Failed to DM {user.mention}.", ephemeral=True)

@bot.tree.command(name="track-invite", description="Check user’s invites/boosts (Admin Only)")
@is_admin()
async def track_invite(interaction: discord.Interaction, user: discord.User):
    invites = await get_user_invites(user.id)
    boosts = await get_user_boosts(interaction.guild, user.id)
    await interaction.response.send_message(f"📊 {user.mention} → Invites: {invites}, Boosts: {boosts}", ephemeral=True)

@bot.tree.command(name="botstatus", description="Change bot presence (Admin Only)")
@is_admin()
async def botstatus(
    interaction: discord.Interaction,
    activity_type: Literal["watching", "playing"],
    text: str
):
    if activity_type == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))
    else:
        await bot.change_presence(activity=discord.Game(name=text))
    await interaction.response.send_message(f"✅ Status updated to: `{activity_type} {text}`", ephemeral=True)

@bot.tree.command(name="admin-help", description="Show admin commands (Admin Only)")
@is_admin()
async def admin_help(interaction: discord.Interaction):
    embed = discord.Embed(title="👑 Admin Commands", color=0xe74c3c)
    embed.description = """
    `/deploy` → Custom VPS deploy
    `/suspend` → Suspend user VPS
    `/delvps` → Delete user VPS
    `/killvps` → Kill all VPS
    `/remove-everything` → Nuclear reset
    `/editplans` → Edit plans (WIP)
    `/sendvps` → DM user VPS info
    `/track-invite` → Check invites/boosts
    `/botstatus` → Change presence
    """
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Error handler for admin check
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("🔒 You don't have permission to use this command.", ephemeral=True)
    else:
        raise error

# On ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="NxH-i7 is best hosting"
        )
    )
    print(f"\n🌸 NxH-i7 VPS Bot is Online 🌸")
    print(f"🚀 Hosting the future, one cloud at a time! 🚀\n")

# Run bot
bot.run(CONFIG["token"])
