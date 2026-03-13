# Graphsignal Debug Client

CLI for Graphsignal: login (store API key) and fetch debug context from api.graphsignal.com.

## Install

```bash
pip install graphsignal-debug
```

## Usage

### Login

Store your Graphsignal API key in `~/.graphsignal/config.yml`:

```bash
graphsignal-debug login
```

You will be prompted for your API key.

### Fetch

Fetch debug context for a time range. Requires being logged in.

```bash
graphsignal-debug fetch --start 2026-03-10T00:00:00Z --end 2026-03-12T00:00:00Z
```

Optional `--tags` filter (semicolon-separated key:value pairs). Tags must match exactly the tags sent to Graphsignal when the app was instrumented:

```bash
graphsignal-debug fetch --start 2026-03-10T00:00:00Z --end 2026-03-12T00:00:00Z --tags "env:prod"
```

The command calls `GET /api/v1/debug_context/` on `https://api.graphsignal.com` with `start_time_ns`, `end_time_ns`, and optional `tags`, and prints the response `context` field.
