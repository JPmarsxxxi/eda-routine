# HOLDOUT RULES (rules and dates only: no results)

Extracted from backtest_engine2\_SEALED_HOLDOUT.md. That file ALSO contains the results of earlier hunts and
records of past breaches, so the routine must NOT read it: reading earlier results contaminates exploration.

## Sealed: no measurement, plot, fit, sweep or diagnostic may touch these ranges

| series | sealed from |
|---|---|
| Binance BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT | 2024-08-01 onward |
| FTMO BTCUSD | 2026-05-01 onward |
| FTMO US500.cash (and, until decided otherwise, any US equity index: US500/US100/US30/US2000, ES/NQ/YM) | 2025-10-06 onward (added 2026-10-07) |

## Splits used for BTC (calendar, UTC)

TRAIN <= 2023-03-19. VAL 2023-03-25 to 2023-11-30. TEST 2023-12-06 to 2024-07-31 (NEVER supplied to the routine).
The same calendar cut is applied to every crypto asset, because coins are highly correlated.

## Splits used for FTMO US500.cash (calendar dates, declared 2026-10-06 from coverage counts only)

TRAIN 2021-10-01 to 2024-12-31. VAL 2025-01-06 to 2025-09-30. TEST 2025-10-06 to 2026-10-05 (NEVER supplied to the routine;
sealed above). Embargoes 2025-01-01..05 and 2025-10-01..05. Copy supplied to the routine: `data\ftmo_us500_clean\` (CUT.json).
US equity indices move together, so the seal covers the other US index CFDs and futures over the same range.

## Rules

1. Nothing touches the sealed range or TEST. Not "just to look".
2. A held-out window is for CHECKING only, never for searching. Each check runs a pre-registered spec, frozen with its pass
   condition before the window is opened, and nothing is tuned on what it showed. Any number of frozen specs may be checked,
   each once (eda-routine v3.3: VAL; TEST only after a VAL pass).
3. Opening TEST is the user's decision, not the routine's.
4. Anything already measured on a held-out window is spent: it cannot be reused as evidence.
