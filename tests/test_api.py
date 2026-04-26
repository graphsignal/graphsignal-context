"""Tests for graphsignal_context.api."""

import pytest
from unittest.mock import patch, Mock

from graphsignal_context.api import iso_to_ns, fetch_signal_context, fetch_signal_guide


class TestIsoToNs:
    def test_iso_utc_z_suffix(self):
        # 2026-03-10 00:00:00 UTC = 1773100800 seconds since epoch
        ns = iso_to_ns("2026-03-10T00:00:00Z")
        assert ns == 1773100800 * 1_000_000_000

    def test_iso_with_offset(self):
        ns = iso_to_ns("2026-03-10T00:00:00+00:00")
        assert ns == 1773100800 * 1_000_000_000

    def test_iso_strips_whitespace(self):
        ns = iso_to_ns("  2026-03-10T00:00:00Z  ")
        assert ns == 1773100800 * 1_000_000_000

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            iso_to_ns("not-a-date")


class TestFetchSignalContext:
    @patch("graphsignal_context.api.requests.get")
    def test_returns_context_field(self, mocked_get):
        mocked_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"context": "signal context body"}),
            raise_for_status=Mock(),
        )
        result = fetch_signal_context("key1", 0, 1000)
        assert result == "signal context body"
        mocked_get.assert_called_once()
        call_kw = mocked_get.call_args[1]
        assert call_kw["headers"]["X-API-KEY"] == "key1"
        assert call_kw["params"]["start_time_ns"] == 0
        assert call_kw["params"]["end_time_ns"] == 1000

    @patch("graphsignal_context.api.requests.get")
    def test_passes_tags_when_provided(self, mocked_get):
        mocked_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value={"context": ""}),
            raise_for_status=Mock(),
        )
        fetch_signal_context("key1", 0, 1000, tags="env:prod")
        call_kw = mocked_get.call_args[1]
        assert call_kw["params"]["tags"] == "env:prod"

    @patch("graphsignal_context.api.requests.get")
    def test_returns_empty_string_when_no_context_key(self, mocked_get):
        mocked_get.return_value = Mock(
            status_code=200,
            json=Mock(return_value={}),
            raise_for_status=Mock(),
        )
        result = fetch_signal_context("key1", 0, 1000)
        assert result == ""

    @patch("graphsignal_context.api.requests.get")
    def test_raises_on_http_error(self, mocked_get):
        import requests
        resp = Mock(status_code=401, text="Unauthorized")
        resp.raise_for_status.side_effect = requests.HTTPError(response=resp)
        mocked_get.return_value = resp
        with pytest.raises(requests.HTTPError):
            fetch_signal_context("badkey", 0, 1000)


class TestFetchSignalGuide:
    @patch("graphsignal_context.api.requests.get")
    def test_returns_plain_text(self, mocked_get):
        mocked_get.return_value = Mock(
            status_code=200,
            text="# Signals\n\nSignal docs",
            raise_for_status=Mock(),
        )
        result = fetch_signal_guide("key1")
        assert result == "# Signals\n\nSignal docs"
        mocked_get.assert_called_once()
        call_kw = mocked_get.call_args[1]
        assert call_kw["headers"]["X-API-KEY"] == "key1"

    @patch("graphsignal_context.api.requests.get")
    def test_raises_on_http_error(self, mocked_get):
        import requests
        resp = Mock(status_code=401, text="Unauthorized")
        resp.raise_for_status.side_effect = requests.HTTPError(response=resp)
        mocked_get.return_value = resp
        with pytest.raises(requests.HTTPError):
            fetch_signal_guide("badkey")
