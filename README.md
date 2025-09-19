
# 🌸 NxH-i7 — Premium Discord VPS Hosting Bot

> **“Hosting the future, one cloud at a time.”**  
> ✨ Cute • Powerful • Dockerized • Slash Commands • Tmate SSH • Invite/Boost Plans

---

## 🚀 Overview

**NxH-i7** is a premium-quality Discord bot that lets users deploy their own Linux VPS using server invites or boosts — all managed via sleek slash commands and adorable embeds. Built with `discord.py`, Docker, and Tmate, it’s perfect for communities offering cloud rewards or premium hosting perks.

Perfect for:
- Discord server monetization via invites/boosts
- Cloud labs for developers & students
- Hosting Minecraft, bots, websites, or tunnels
- Admins who want full control + cute UI 😍

---

## 🧩 Features

### 🧑‍💻 User Experience
- `/createvps` → Dropdown menu with kawaii plans 🌸✨💎🎀⚡
- `/manage` → Start, Stop, Reinstall, Re-SSH with buttons
- `/plans` → Clean embed showing invite & boost tiers
- `/list` → View your deployed VPS specs
- `/regen-ssh` → Fresh Tmate SSH session anytime
- `/help` + `/botinfo` → Cute, categorized help panels

### 👑 Admin Powers
- `/deploy` → Custom RAM/CORE/DISK VPS for any user
- `/suspend`, `/delvps`, `/killvps` → Full VPS lifecycle control
- `/remove-everything` → Nuclear reset (⚠️ use carefully!)
- `/sendvps` → DM user their SSH credentials
- `/track-invite` → Check user invites & boosts
- `/botstatus` → Dynamically change bot presence
- `/admin-help` → Quick reference for admin commands

### 🐳 Tech Stack
- **Python 3.11+** with `discord.py 2.3+`
- **Docker** integration (mocked container deployment)
- **Tmate SSH** mock (easy to replace with real implementation)
- **YAML config** for easy customization
- **Flat-file DB** (`database.txt`) — no SQL needed!
- **Docker-ready** — one-command deploy

---

## ⚙️ Installation

### 1. Clone or Download

```bash
git clone https://github.com/mustakindev/NXH-I7-Deploy-Bot.git
cd NXH-I7-Deploy-Bot
```

### 2. Configure `config.yml`

```yaml
token: "YOUR_DISCORD_BOT_TOKEN_HERE"
admin_ids:
  - "1128161197766746213"  # Your Discord ID
plans:
  invites:
    - name: "Starter"
      invites: 6
      ram: "8GB"
      cores: 5
      disk: "10GB"
    # ... customize plans as needed
  boosts:
    - name: "Boost-1"
      boosts: 1
      ram: "12GB"
      cores: 5
      disk: "30GB"
    # ...
```

> 💡 Get your bot token from [Discord Developer Portal](https://discord.com/developers/applications)

### 3. Build & Run with Docker

```bash
docker build -t nxh-i7 .
docker run -d \
  --name nxh-i7-bot \
  --restart unless-stopped \
  nxh-i7
```

> 🐳 For real VPS deployment, mount Docker socket:  
> `-v /var/run/docker.sock:/var/run/docker.sock`

---

## 📜 Commands Quick Reference

| Command | Description |
|--------|-------------|
| `/createvps` | Deploy VPS via invite/boost plan |
| `/plans` | View all available plans |
| `/manage` | Control panel for your VPS |
| `/list` | Show your VPS details |
| `/start` `/stop` `/restart` | Basic VPS controls |
| `/remove` | Delete your VPS |
| `/regen-ssh` | Get new SSH session |
| `/help` | User + Admin command list |
| `/botinfo` | Branding & credits |

> 👑 *Admin-only commands require your ID in `config.yml`*

---

## 🎀 Cute Design Elements

We believe hosting should be fun! That’s why NxH-i7 uses:

- 🌸✨💎🎀⚡ **Premium emojis** in every embed
- 🎨 **Color-coordinated embeds** (pastel purples, blues, pinks)
- 🖤 **Minimalist yet expressive UI**
- 🚀 **Startup animation log** for that premium feel
- 💫 **DM-delivered SSH** with cute formatting

---

## 🔮 Future Roadmap

- [ ] Real Tmate SSH session generation
- [ ] Web dashboard for VPS management
- [ ] Billing & PayPal/Stripe integration
- [ ] Resource usage graphs (RAM/CPU/DISK)
- [ ] Auto-backup & snapshot system
- [ ] Multi-node support 🌐
- [ ] Kubernetes mode (for advanced users)

---

## 🛠️ Need Help?

- 💬 Join our [Support Server]() *(coming soon)*
- 🐞 Report bugs or request features on [GitHub Issues]()
- 💌 DM `Mustakin` on Discord for collabs

---

## 🧑‍💻 Made By

**Mustakin**  
> Creator of NxH-i7 — turning Discord into a cloud playground 🪄  
> Portfolio: [yourlink.com]() | Discord: `Mustakin#0001`

---

## 📄 License

MIT License — Use, modify, redistribute freely.  
Just keep the credits cute 😉🌸

---

## 🌈 Sample Bot Presence

```
Watching → NxH-i7 is best hosting
Playing → with VPS Clouds
```

---

## 💖 Thank You

Thanks for choosing **NxH-i7** — where performance meets kawaii.  
Deploy your cloud. Share the magic. Be the host. 🚀🪐

---

> ✨ *“Not all clouds are in the sky — some are in your Discord server.”*

---

✅ **Ready to host the future?**  
```bash
docker run -d nxh-i7
```

---

Let me know if you want:
- GitHub repo template
- Logo/banner assets
- Web dashboard mockup
- Real Tmate + Docker implementation guide

💖 Happy Hosting with NxH-i7!
