import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from panel import *
os.chdir(RUN)
tr_idx = GRID[train_mask(GRID)]
def cov(df, name):
    t = pd.DataFrame({nm: df[in_slice(df.index, nm)].notna().mean() * 100 for nm in SLICES}).T.round(0)
    print(f"-- {name}: % non-null hourly rows by slice x coin"); print(t.to_string())
F, W = funding("phase0_03"); cov(F, "funding (last settled rate, stamp<=bar open)")
print("funding interval hours (non-8):", {c: int((W[c].dropna() != 8).sum()) for c in COINS})
print("funding: share exactly 0.0001 by slice:", {nm: round(float((F[in_slice(F.index,nm)] .round(6)==0.0001).stack().mean()),2) for nm in SLICES})
K = perp_hourly("phase0_03", "klines"); cov(K["close"], "perp klines close")
PR = perp_hourly("phase0_03", "premium"); cov(PR["close"], "perp premium index close")
print("premium index: zero volume share (expected: premium klines carry no trades):", float((PR["volume"]==0).stack().mean()))
M = metrics_hourly("phase0_03"); cov(M["sum_open_interest"], "metrics: open interest (hourly last snapshot)")
cov(M["count_long_short_ratio"], "metrics: long/short account ratio")
print("OI == 0 hours:", int((M["sum_open_interest"]==0).sum().sum()), " OI value/ (OI*spot close) check pending")
for k,v in M.items(): v.to_parquet(f"work/metrics_{k}.parquet")
S = spot("phase0_03")
CB = venue("coinbase", "coinbase") if False else venue("phase0_03", "coinbase"); cov(CB["close"], "coinbase close")
UB = venue("phase0_03", "upbit"); cov(UB["close"], "upbit KRW close")
print("\nknowability/alignment checks")
# perp kline close vs spot close: basis, and is perp stamp aligned (corr of returns same hour vs +-1)
for c in ["BTC","ETH"]:
    pr = np.log(K["close"][c]/K["close"][c].shift(1)); sr = np.log(S["close"][c]/S["close"][c].shift(1))
    m = train_mask(pr.index)
    print(c, "corr perp ret vs spot ret same hour", round(pr[m].corr(sr[m]),3), "lag+1", round(pr[m].corr(sr.shift(1)[m]),3), "lead", round(pr[m].corr(sr.shift(-1)[m]),3))
    cr = np.log(CB["close"][c]/CB["close"][c].shift(1)) if c in CB["close"] else None
    if cr is not None: print(c, "coinbase vs binance same hour", round(cr[m].corr(sr[m]),3))
bas = (K["close"]/S["close"]-1)*1e4
print("perp-spot close basis bp by slice (median):", {nm: round(float(bas[in_slice(bas.index,nm)].stack().median()),1) for nm in SLICES})
print("premium index close (bp) median by slice:", {nm: round(float(PR['close'][in_slice(PR['close'].index,nm)].stack().median()*1e4),1) for nm in SLICES})
print("OI value / (OI * spot close) ratio median BTC:", float((M['sum_open_interest_value']['BTC']/(M['sum_open_interest']['BTC']*S['close']['BTC'])).median()))
