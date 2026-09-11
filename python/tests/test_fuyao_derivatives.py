from __future__ import annotations

import pytest

from toolkit.fuyao.scripts import fuyao_client


@pytest.mark.parametrize(
    "function_name,args,kwargs,path",
    [
        ("futures_varieties", (), {}, "/api/futures/varieties/list"),
        ("futures_contract_detail", ("RB2610.SHF",), {}, "/api/futures/contracts/detail"),
        ("futures_variety_positions", ("2026-09-10",), {}, "/api/futures/positions/variety-daily"),
        (
            "futures_company_variety_positions",
            ("2026-09-10", "RB,HC"),
            {},
            "/api/futures/positions/company-variety-daily",
        ),
        (
            "futures_contract_positions",
            ("RB2610.SHF", "RB", "2026-09-10"),
            {},
            "/api/futures/positions/contract-daily",
        ),
        (
            "futures_contract_position_history",
            ("RB2610.SHF", "RB", "永安期货", "2026-09-01"),
            {},
            "/api/futures/positions/contract-historical",
        ),
        ("futures_position_companies", (), {}, "/api/futures/positions/company-list"),
        (
            "futures_warehouse_receipts",
            ("RB2610.SHF", "2026-09-01", "2026-09-10"),
            {},
            "/api/futures/warehouse-receipts/historical",
        ),
        ("futures_latest_basis", (), {}, "/api/futures/basis/main-continuous-latest"),
        ("futures_basis_history", ("RB2610.SHF",), {}, "/api/futures/basis/historical"),
        (
            "futures_trading_schedule",
            ("RB2610.SHF", "2026-09-01", "2026-09-10"),
            {},
            "/api/futures/calendar/trading-schedule",
        ),
        ("futures_intraday", ("RB2610.SHF",), {}, "/api/futures/prices/intraday"),
        ("futures_daily", ("RB2610.SHF",), {}, "/api/futures/prices/daily"),
        ("options_varieties", (), {}, "/api/options/varieties/list"),
        ("options_contract_detail", ("MO2610-C-6500.CFX",), {}, "/api/options/contracts/detail"),
        ("options_intraday", ("MO2610-C-6500.CFX",), {}, "/api/options/prices/intraday"),
        ("options_daily", ("MO2610-C-6500.CFX",), {}, "/api/options/prices/daily"),
    ],
)
def test_derivative_functions_map_to_public_paths(monkeypatch, function_name, args, kwargs, path):
    calls = []
    monkeypatch.setattr(fuyao_client, "_get", lambda endpoint, params: calls.append((endpoint, params)) or {})
    getattr(fuyao_client, function_name)(*args, **kwargs)
    assert calls[0][0] == path


def test_derivative_validation_happens_before_http(monkeypatch):
    monkeypatch.setattr(fuyao_client, "_get", lambda *_args, **_kwargs: pytest.fail("HTTP must not be called"))
    with pytest.raises(ValueError, match="start_date"):
        fuyao_client.futures_warehouse_receipts("RB2610.SHF", "2026-09-11", "2026-09-10")
    with pytest.raises(ValueError, match="session"):
        fuyao_client.options_intraday("MO2610-C-6500.CFX", session="overnight")
