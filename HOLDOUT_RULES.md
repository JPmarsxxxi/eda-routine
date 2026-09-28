# HOLDOUT RULES (rules and dates only: no results)

Extracted from backtest_engine2\_SEALED_HOLDOUT.md. That file ALSO contains the results of earlier hunts and
records of past breaches, so the routine must NOT read it: reading earlier results contaminates exploration.

## Sealed: no measurement, plot, fit, sweep or diagnostic may touch these ranges

| series | sealed from |
|---|---|
| Binance BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT | 2024-08-01 onward |
| FTMO BTCUSD | 2026-05-01 onward |

## Splits used for BTC (calendar, UTC)

TRAIN <= 2023-03-19. VAL 2023-03-25 to 2023-11-30. TEST 2023-12-06 to 2024-07-31 (NEVER supplied to the routine).
The same calendar cut is applied to every crypto asset, because coins are highly correlated.

## Rules

1. Nothing touches the sealed range or TEST. Not "just to look".
2. A held-out window is opened ONCE, for a pre-registered test whose pass condition was written before the run.
3. Opening a held-out window is the user's decision, not the routine's.
4. Anything already measured on a held-out window is spent: it cannot be reused as evidence.
