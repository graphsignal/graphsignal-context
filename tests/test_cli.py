"""Tests for graphsignal_context CLI."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from graphsignal_context.cli import cli


runner = CliRunner()


def test_fetch_requires_login():
    with patch("graphsignal_context.cli.get_api_key", return_value=None):
        result = runner.invoke(cli, ["fetch", "--start", "2026-03-10T00:00:00Z", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code != 0
    assert "Not logged in" in result.output or "graphsignal-context login" in result.output


def test_fetch_success_outputs_context():
    with patch("graphsignal_context.cli.get_api_key", return_value="test-key"):
        with patch("graphsignal_context.cli.fetch_signal_context", return_value="context output"):
            result = runner.invoke(cli, ["fetch", "--start", "2026-03-10T00:00:00Z", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code == 0
    assert "context output" in result.output


def test_fetch_rejects_end_before_start():
    with patch("graphsignal_context.cli.get_api_key", return_value="key"):
        result = runner.invoke(
            cli,
            ["fetch", "--start", "2026-03-12T00:00:00Z", "--end", "2026-03-10T00:00:00Z"],
        )
    assert result.exit_code != 0
    assert "--start must be before --end" in result.output


def test_fetch_invalid_datetime():
    with patch("graphsignal_context.cli.get_api_key", return_value="key"):
        result = runner.invoke(cli, ["fetch", "--start", "not-a-date", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code != 0
    assert "Invalid datetime" in result.output or "Error" in result.output
