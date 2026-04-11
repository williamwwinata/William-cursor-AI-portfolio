# William's Cursor AI Portfolio

A portfolio project built as part of the 100hires AI developer program. This repository documents the setup, tools, and process of configuring an AI-assisted development environment using Cursor IDE.

---

## Tools Installed

| Tool | Purpose |
|------|---------|
| [Cursor IDE](https://cursor.com) | AI-native code editor built on VS Code |
| Claude Code (Cursor Extension) | Anthropic's AI coding assistant, run via integrated terminal |
| Codex (Cursor Extension) | OpenAI-powered coding extension with sidebar interface |

---

## Languages & Technologies

- **Markdown** — documentation and README authoring
- **Git / GitHub** — version control and remote repository management
- **Bash / Terminal** — running CLI tools within Cursor's integrated terminal

---

## Setup Process

### 1. Installing Cursor IDE
- Visited [cursor.com](https://cursor.com), created an account, and downloaded the desktop application
- Logged in to the Cursor app using the newly created account
- Restarted the PC after installation to ensure a clean environment before proceeding

### 2. Finding the Extensions Panel
- Located the Extensions panel via **View > Extensions** in the Cursor menu bar
- Searched for and installed both **Claude Code** and **Codex** extensions

### 3. Setting Up Claude Code
- Claude Code was already installed on this machine as a CLI tool via a personal Anthropic subscription
- Claude Code authentication is **local** — credentials are stored on-device in `~/.claude/` after the initial OAuth login
- Because authentication persists locally, no additional login was required inside Cursor; opening Cursor's integrated terminal and running `claude` was sufficient to start a session immediately

### 4. Setting Up Codex
- The Codex extension did not have an immediately obvious entry point in the UI
- Watched a YouTube tutorial to understand how to launch it
- Used **Ctrl + Shift + P** to open the Command Palette and ran the **Open Codex Sidebar** command
- The extension prompted for account login, which was completed successfully

---

## Issues Encountered & How They Were Resolved

| Issue | Resolution |
|-------|-----------|
| Did not know where to find the Extensions panel in Cursor | Explored the menu bar and found it under **View > Extensions** |
| Unsure how to launch the Codex extension after installing it | Searched YouTube for a tutorial; learned to use **Ctrl + Shift + P** → **Open Codex Sidebar** |
| Needed to verify whether Claude Code required re-authentication inside Cursor | Confirmed that Claude Code stores auth locally on the device — no additional login needed |

---

## Key Takeaways

- Cursor's interface is familiar to anyone who has used VS Code, which reduces the learning curve significantly
- Claude Code's local authentication model means it works seamlessly across any terminal on the same machine without repeated logins
- When documentation or UI discoverability is lacking, targeted YouTube searches are an effective and fast way to unblock setup steps
- Restarting the PC after installations is a simple but effective step to avoid subtle environment issues
