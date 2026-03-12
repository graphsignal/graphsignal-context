"""graphsignal-debug: login and fetch."""

import sys
from typing import Optional

import click
import requests

from .config import get_api_key, set_api_key
from .api import iso_to_ns, fetch_debug_context


def main():
    cli()


@click.group()
def cli():
    """Graphsignal debug CLI."""
    pass


@cli.command()
def login():
    """Store Graphsignal API key in ~/.graphsignal/config.yml."""
    api_key = click.prompt("Graphsignal API key", hide_input=True)
    if not api_key or not api_key.strip():
        click.echo("API key cannot be empty.", err=True)
        sys.exit(1)
    set_api_key(api_key.strip())
    click.echo("API key saved to ~/.graphsignal/config.yml")


def _ensure_logged_in() -> str:
    api_key = get_api_key()
    if not api_key:
        click.echo(
            "Not logged in. Run: graphsignal-debug login",
            err=True,
        )
        sys.exit(1)
    return api_key


@cli.command()
@click.option(
    "--start",
    required=True,
    help="Start of time range (ISO 8601, e.g. 2026-03-10T00:00:00Z)",
)
@click.option(
    "--end",
    "end_",
    required=True,
    help="End of time range (ISO 8601, e.g. 2026-03-12T00:00:00Z)",
)
@click.option(
    "--tags",
    default=None,
    help="Filter by tags (semicolon-separated key:value pairs)",
)
def fetch(start: str, end_: str, tags: Optional[str]):
    """Fetch debug context for the given time range from api.graphsignal.com."""
    api_key = _ensure_logged_in()
    try:
        start_ns = iso_to_ns(start)
        end_ns = iso_to_ns(end_)
    except ValueError as e:
        click.echo(f"Invalid datetime: {e}", err=True)
        sys.exit(1)
    if start_ns >= end_ns:
        click.echo("--start must be before --end", err=True)
        sys.exit(1)
    try:
        context = fetch_debug_context(api_key, start_ns, end_ns, tags=tags)
    except requests.HTTPError as e:
        msg = e.response.text if e.response is not None else str(e)
        click.echo(f"API error {e.response.status_code if e.response else ''}: {msg}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    click.echo(context)
