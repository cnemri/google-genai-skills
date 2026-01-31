# 🌌 Google GenAI Skills

> **A curated collection of agentic skills for Google AI frameworks and models.**
> Designed to work seamlessly with **Gemini CLI**, **Antigravity**, **Claude Code**, and more.

**Author:** [Chouaieb Nemri](https://github.com/cnemri)

---

## 🚀 About

This repository provides a set of high-performance agentic skills that allow your AI assistants to interact deeply with Google's AI ecosystem. Whether you are using the Gemini CLI, Antigravity IDE, or Claude Code, these skills empower your agent with the knowledge and tools to master Google's GenAI SDKs, models, and protocols.

## 📦 Available Skills

| Skill Name | Description | Status |
| :--- | :--- | :--- |
| [`google-adk-python`](./skills/google-adk-python) | Google Agent Development Kit python SKD. | ✅ Implemented |
| [`google-genai-sdk-python`](./skills/google-genai-sdk-python) | Use the right patterns for the Google GenAI Python SDK. | ✅ Implemented |
| [`veo-build`](./skills/veo-build) | Google DeepMind Veo Skills (Build). | ✅ Implemented |
| [`nano-banana-build`](./skills/nano-banana-build) | Gemini Image Nano Banana Skills (Build) | ✅ Implemented |
| [`speech-build`](./skills/speech-build) | Gemini and Chirp TTS Skills (Build). | ✅ Implemented |
| [`veo-use`](./skills/veo-use) | Google DeepMind Veo Skills (Use). | ✅ Implemented |
| [`nano-banana-use`](./skills/nano-banana-use) | Gemini Image Nano Banana Skills (Use) | ✅ Implemented |
| [`speech-use`](./skills/speech-use) | Gemini and Chirp TTS Skills (Use). | ✅ Implemented |
| [`deep-research`](./skills/deep-research) | Gemini Deep Research Agent (Interactions API). | ✅ Implemented |

## 🛠️ Installation

You can install skills individually or clone the entire repository.

### Install Specific Skill (Recommended)

To install a specific skill (e.g., `google-adk-python`) directly into your agent's environment:

```bash
npx skills add cnemri/google-genai-skills --skill google-adk-python
```

### Manual Installation

To use these skills by cloning the repository:

```bash
git clone https://github.com/cnemri/google-genai-skills.git ~/.gemini/skills/google-genai-skills
```

(Or follow the specific instructions for your agent environment).

## 📚 Documentation & Installation Guides

For detailed instructions on how to install and manage skills for your specific agent provider, please refer to the official documentation:

| Provider | Documentation |
| :--- | :--- |
| **Gemini CLI** | [geminicli.com/docs/cli/skills](https://geminicli.com/docs/cli/skills/) |
| **Antigravity** | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) |
| **Claude Code** | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| **OpenAI Codex** | [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills) |
| **GitHub Copilot** | [docs.github.com/copilot/agents](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| **VS Code Copilot** | [code.visualstudio.com/copilot/skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) |

---

## 🤝 Compatibility

These skills follow the universal **SKILL.md** format and are compatible with:

- 🔵 **Gemini CLI**
- 🔴 **Antigravity**
- 🟣 **Claude Code**
- 🟠 **Cursor**

---

## ⚖️ License

MIT