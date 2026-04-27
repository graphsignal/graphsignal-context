"""Tests for graphsignal_context CLI."""

from unittest.mock import patch

from click.testing import CliRunner

from graphsignal_context.cli import cli


runner = CliRunner()


def test_signals_requires_login():
    with patch("graphsignal_context.cli.get_api_key", return_value=None):
        result = runner.invoke(cli, ["signals", "--start", "2026-03-10T00:00:00Z", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code != 0
    assert "Not logged in" in result.output or "graphsignal-context login" in result.output


def test_signals_success_outputs_context():
    with patch("graphsignal_context.cli.get_api_key", return_value="test-key"):
        with patch("graphsignal_context.cli.get_api_base", return_value="http://signal-api:8080"):
            with patch("graphsignal_context.cli.fetch_signal_context", return_value="context output"):
                result = runner.invoke(cli, ["signals", "--start", "2026-03-10T00:00:00Z", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code == 0
    assert "context output" in result.output


def test_signals_passes_api_base():
    with patch("graphsignal_context.cli.get_api_key", return_value="test-key"):
        with patch("graphsignal_context.cli.get_api_base", return_value="http://signal-api:8080"):
            with patch("graphsignal_context.cli.fetch_signal_context", return_value="context output") as mocked_fetch:
                result = runner.invoke(cli, ["signals", "--start", "2026-03-10T00:00:00Z", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code == 0
    mocked_fetch.assert_called_once()
    assert mocked_fetch.call_args.kwargs["api_base"] == "http://signal-api:8080"


def test_signals_rejects_end_before_start():
    with patch("graphsignal_context.cli.get_api_key", return_value="key"):
        with patch("graphsignal_context.cli.get_api_base", return_value="https://api.graphsignal.com"):
            result = runner.invoke(
                cli,
                ["signals", "--start", "2026-03-12T00:00:00Z", "--end", "2026-03-10T00:00:00Z"],
            )
    assert result.exit_code != 0
    assert "--start must be before --end" in result.output


def test_signals_invalid_datetime():
    with patch("graphsignal_context.cli.get_api_key", return_value="key"):
        with patch("graphsignal_context.cli.get_api_base", return_value="https://api.graphsignal.com"):
            result = runner.invoke(cli, ["signals", "--start", "not-a-date", "--end", "2026-03-12T00:00:00Z"])
    assert result.exit_code != 0
    assert "Invalid datetime" in result.output or "Error" in result.output


def test_guide_requires_login():
    with patch("graphsignal_context.cli.get_api_key", return_value=None):
        result = runner.invoke(cli, ["guide"])
    assert result.exit_code != 0
    assert "Not logged in" in result.output or "graphsignal-context login" in result.output


def test_guide_success_outputs_text():
    with patch("graphsignal_context.cli.get_api_key", return_value="test-key"):
        with patch("graphsignal_context.cli.get_api_base", return_value="http://signal-api:8080"):
            with patch("graphsignal_context.cli.fetch_signal_guide", return_value="# Signals\n\nSignal docs"):
                result = runner.invoke(cli, ["guide"])
    assert result.exit_code == 0
    assert "# Signals" in result.output


def test_guide_passes_api_base():
    with patch("graphsignal_context.cli.get_api_key", return_value="test-key"):
        with patch("graphsignal_context.cli.get_api_base", return_value="http://signal-api:8080"):
            with patch("graphsignal_context.cli.fetch_signal_guide", return_value="# Signals\n\nSignal docs") as mocked_fetch:
                result = runner.invoke(cli, ["guide"])
    assert result.exit_code == 0
    mocked_fetch.assert_called_once()
    assert mocked_fetch.call_args.kwargs["api_base"] == "http://signal-api:8080"
