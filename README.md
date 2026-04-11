# William's Cursor AI Portfolio

A portfolio project built as part of the 100hires AI-Native application process. This repository documents my setup, tools, and process of configuring an AI-assisted development environment using Cursor IDE.

---

## Tools Installed

- **[Cursor IDE](https://cursor.com)** — AI-native code editor built on VS Code
- **Claude Code** (Cursor Extension) — Anthropic's AI coding assistant, which I run via the integrated terminal
- **Codex** (Cursor Extension) — OpenAI-powered coding extension with a sidebar interface

---

## Languages and Technologies Used

- **Markdown** — for documentation and README authoring
- **Git / GitHub** — for version control and remote repository management
- **Bash / Terminal** — for running CLI tools within Cursor's integrated terminal

---

## Setup Process

### 1. Installing Cursor IDE
- I visited [cursor.com](https://cursor.com), created an account, and downloaded the desktop application
- I logged in to the Cursor app using my newly created account
- I restarted my PC after installation to ensure a clean environment before proceeding

### 2. Installing Extensions
- I located the Extensions panel via **View > Extensions** in the Cursor menu bar
- I searched for and installed both the **Claude Code** and **Codex** extensions

### 3. Setting Up Claude Code
- I already had Claude Code installed on my machine as a CLI tool via my personal Anthropic subscription
- Claude Code authentication is **local** — credentials are stored on-device in `~/.claude/` after the initial OAuth login
- Because my authentication was already stored locally, I did not need to log in again inside Cursor; I simply opened Cursor's integrated terminal and ran `claude` to start a session immediately

### 4. Setting Up Codex
- The Codex extension did not have an immediately obvious entry point in the UI
- I watched a YouTube tutorial to understand how to launch it
- I used **Ctrl + Shift + P** to open the Command Palette and ran the **Open Codex Sidebar** command
- The extension prompted me to log in, which I completed successfully

### 5. Creating the GitHub Repository and Cloning Locally
- I created a new public repository on GitHub using my existing GitHub account
- I cloned the repository to my local machine to start working with it inside Cursor

### 6. Writing the README and Pushing to GitHub
- With Claude Code running in my Cursor terminal, I used it to write this README documenting my full setup process — I specifically told Claude to write it in first person so it accurately reflects my own experience
- I had Claude Code handle the `git commit` and `git push` to upload the changes to my GitHub repository

---

## Issues Encountered and How They Were Resolved

- **Did not know where to find the Extensions panel in Cursor** — I explored the menu bar and found it under **View > Extensions**
- **Unsure how to launch the Codex extension after installing it** — I searched YouTube for a tutorial and learned to use **Ctrl + Shift + P** then **Open Codex Sidebar**
- **Needed to verify whether Claude Code required re-authentication inside Cursor** — I confirmed that Claude Code stores auth locally on the device, so no additional login was needed

---

## Key Takeaways

- Cursor's interface felt familiar since I have used VS Code before, which made the learning curve much easier
- Claude Code's local authentication model means it works seamlessly across any terminal on the same machine without repeated logins
- When documentation or UI discoverability is lacking, a targeted YouTube search is a fast and effective way to get unblocked
- Restarting my PC after installations was a simple but effective step to avoid potential environment issues
- AI tools like Claude Code can handle not just coding tasks but also documentation and Git operations, which streamlines the entire development workflow

---

## Personal Note

This entire project was built using Claude Code inside Cursor. To me, this task is ultimately about demonstrating problem-solving ability and clarity of thinking. My view is that as long as a person has a clear understanding of the problem and the steps needed to address it, AI becomes a powerful multiplier that accelerates the workflow without replacing the judgment behind it. That is exactly why I chose to leverage Claude Code here: so I could stay focused on the what and the why, while letting AI handle the execution. This approach is also backed by a level of technical literacy that I believe is one of the most essential skills an individual can have in this era.
