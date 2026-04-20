# Graphsignal Context Client

CLI for Graphsignal: login (store API key) and fetch signal context from api.graphsignal.com. You can also install a skill so your AI coding agent (Cursor, Claude Code, Codex, etc.) can run the CLI and use the returned context to help optimize inference, profiles, or errors.

## Install

```bash
pip install graphsignal-context
```

Or install as an isolated CLI tool with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install graphsignal-context
```

## Usage

### Login

Store your Graphsignal API key in `~/.graphsignal/config.yml`:

```bash
graphsignal-context login
```

You will be prompted for your API key.

### Fetch

Fetch signal context for a time range. Requires being logged in.

```bash
graphsignal-context fetch --start 2026-03-10T00:00:00Z --end 2026-03-12T00:00:00Z
```

Optional `--tags` filter (semicolon-separated key:value pairs). Tags must match exactly the tags sent to Graphsignal when the app was instrumented:

```bash
graphsignal-context fetch --start 2026-03-10T00:00:00Z --end 2026-03-12T00:00:00Z --tags "env:prod"
```

The command calls `GET /api/v1/signal_context/` on `https://api.graphsignal.com` with `start_time_ns`, `end_time_ns`, and optional `tags`, and prints the response context.

---

## AI agent integration

Install the Graphsignal skill so your AI coding agent can run `graphsignal-context fetch` for a time range and use the returned context (profiles, errors, traces) to help you optimize.

**Claude Code** — Clone the repo into Claude's personal skills directory:

```bash
git clone https://github.com/graphsignal/graphsignal-context ~/.claude/skills/graphsignal-context
```

**Other agents (Cursor, Codex, Gemini)** — Use the [skills.sh](https://skills.sh) registry:

```bash
npx skills add graphsignal/graphsignal-context
```

Install the CLI first (`pip install graphsignal-context` or `uv tool install graphsignal-context`), then run `graphsignal-context login` with your API key.

### Supported agents

- **Cursor** — Use the skill when working in Cursor with agent/composer.
- **Claude Code** — Use with Claude Code (e.g. via Claude CLI or supported IDEs).
- **Codex** — Use with Codex agent workflows.
- **Gemini CLI** — Use with Gemini from the command line.

### Example prompts

Once the skill is installed, you can ask the agent to:

- **Find the root cause of a latency spike** — e.g. "Fetch Graphsignal data for the last 2 hours and find the root cause of the latency spike" or "What's causing the slowdown? Use Graphsignal signal context from 10am to noon today."
- **Explain errors or failures** — e.g. "Get signal context for the last 24 hours and summarize any errors or failures" or "Why did inference fail around 3pm? Pull Graphsignal data for that window."
- **Inspect profiles and bottlenecks** — e.g. "Fetch Graphsignal context for yesterday and identify the main performance bottlenecks" or "Which operations are taking the most time? Use Graphsignal data from the last 6 hours."

The agent will call `graphsignal-context fetch --start <ISO> --end <ISO>` (and optional `--tags` when you specify deployment or service tags), then analyze the returned context to answer your question.
