---
name: graphsignal-context
description: Fetch Graphsignal signal context via the graphsignal-context CLI. Use when the user needs signal context, time-range queries for signals/profiles/errors, signal guide content, or CLI access to the context APIs.
---

# graphsignal-context commands

Fetch signal context and signal guide content from [Graphsignal](https://graphsignal.com) (api.graphsignal.com).

## When to use

- User asks for Graphsignal signal context, signal output, or time-range data.
- User wants to inspect signals, profiles, or errors for a specific window.
- User needs to call the signal_context API from the command line or from agent workflows.

## Prerequisites

1. **Install** (from PyPI):
   ```bash
   pip install graphsignal-context
   ```

2. **Login** (once). API key is stored in `~/.graphsignal/config.yml`:
   ```bash
   graphsignal-context login
   ```
   Alternatively, set `GRAPHSIGNAL_API_KEY` in the environment; the CLI uses it if present.

If not logged in, `signals` and `guide` exit with: "Not logged in. Run: graphsignal-context login".

## Command

```bash
graphsignal-context signals --start <ISO8601> --end <ISO8601> [--tags "key:value;..."]
```

- **--start** (required): Start of time range, ISO 8601 with Z (UTC). Example: `2026-03-10T00:00:00Z`.
- **--end** (required): End of time range, same format. Must be after `--start`.
- **--tags** (optional): Filter by tags; semicolon-separated `key:value` pairs. Example: `env:prod;service:api`. Tags must be known exactly—they are the same tags sent to Graphsignal when the application was instrumented (e.g. from `graphsignal.configure()` or the SDK).

The CLI calls `GET https://api.graphsignal.com/api/v1/context/signals/` with `start_time_ns`, `end_time_ns`, and optional `tags`, and prints the response `context` field.

## Command

```bash
graphsignal-context guide
```

Fetch guide content about signals and print it to stdout.

The CLI calls `GET https://api.graphsignal.com/api/v1/context/guide/` and prints the returned text content.

## Examples

```bash
# Last two days (adjust dates to your window)
graphsignal-context signals --start 2026-03-10T00:00:00Z --end 2026-03-12T00:00:00Z

# With tag filter
graphsignal-context signals --start 2026-03-10T00:00:00Z --end 2026-03-12T00:00:00Z --tags "env:production"
```

## Agent workflow

1. If the user needs signal context for a time range, run `graphsignal-context signals` with the appropriate `--start` and `--end` (ISO 8601 UTC).
2. If the user needs general guide content about signals, run `graphsignal-context guide`.
3. If a command fails with "Not logged in", tell the user to run `graphsignal-context login` or set `GRAPHSIGNAL_API_KEY`.
4. Use the `signals` output JSON to answer questions about profiles, errors, traces, or metrics in that window.
5. The `signals` response includes `available_tags` — all metric tag keys with their most recent values. Use these to re-fetch context with `--tags` for a specific host, process, GPU device, etc. when you need more targeted optimization (e.g. `--tags "host.name:gpu-server-01"` or `--tags "device.index:0"`).
