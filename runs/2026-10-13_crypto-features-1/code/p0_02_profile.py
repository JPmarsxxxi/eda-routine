import sys; sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
from panel import *
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, r"C:\Users\User\backtest_engine\backtest_engine2")
from cellplot import setup, PAL; setup()
os.chdir(RUN)
P, NS, QV, SRC = prim("phase0_02")
S = spot("phase0_02")
r1 = back(P, NS, 1)
tr = train_mask(P.index)
print("== 1 DISTRIBUTIONS (1h log return, TRAIN)")
rows=[]
for c in COINS:
    x = r1[c][tr].dropna()
    rows.append(dict(coin=c, n=len(x), sd_bp=x.std()*1e4, skew=stats.skew(x), exkurt=stats.kurtosis(x), zero_pct=(x==0).mean()*100, q001_bp=x.quantile(.001)*1e4, q999_bp=x.quantile(.999)*1e4))
T1=pd.DataFrame(rows).round(2); print(T1.to_string(index=False))
T1.to_csv("work/p0_dist.csv", index=False)
fig,ax=plt.subplots(1,2,figsize=(11,4))
for i,c in enumerate(["BTC","DOGE","SOL"]):
    x=r1[c][tr].dropna()*1e4; ax[0].hist(x.clip(-300,300),bins=120,alpha=.5,label=c,color=PAL[i])
ax[0].set_title("1h returns, bp (clipped +-300)"); ax[0].legend()
for i,c in enumerate(COINS): ax[1].bar(i,T1.exkurt[i],color=PAL[i%8])
ax[1].set_xticks(range(10)); ax[1].set_xticklabels(COINS,rotation=45); ax[1].set_title("excess kurtosis of 1h returns")
fig.savefig("plots/00_distributions.png",bbox_inches="tight"); plt.close(fig)

print("\n== 2 MISSINGNESS: missing hours inside each coin's own span (primary) and binance spot")
rows=[]
for c in COINS:
    p=P[c][tr]; first=p.first_valid_index(); last=p.last_valid_index()
    span=p.loc[first:last]; miss=span.isna().sum()
    s=S["close"][c][tr].loc[first:last]
    # longest run of missing
    runs=(span.isna().astype(int).groupby((~span.isna()).cumsum()).sum()).max()
    rows.append(dict(coin=c, first=str(first)[:10], span_h=len(span), prim_missing_h=int(miss), longest_gap_h=int(runs), spot_missing_h=int(s.isna().sum())))
T2=pd.DataFrame(rows); print(T2.to_string(index=False))
print("\nFTMO Saturday holes: share of Saturday-hours missing in primary C3 (BTC):")
b=P["BTC"][in_slice(P.index,"C3")]; sat=b[b.index.dayofweek==5]
print(sat.isna().groupby(sat.index.hour).mean().round(2).to_dict())

print("\n== 3 AUTOCORRELATION (TRAIN): ACF of 1h returns, |returns|, log quote volume")
lags=[1,2,3,6,12,24,168]
rows=[]
for c in COINS:
    x=r1[c][tr]; a=x.abs(); v=np.log(S["quote_vol"][c].where(S["quote_vol"][c]>0))[tr]
    rows.append(dict(coin=c, **{f"ret_l{l}":x.autocorr(l) for l in lags[:4]}, **{f"abs_l{l}":a.autocorr(l) for l in (1,24,168)}, **{f"vol_l{l}":v.autocorr(l) for l in (1,24,168)}))
T3=pd.DataFrame(rows).round(3); print(T3.to_string(index=False)); print("2/sqrt(n)=", round(2/np.sqrt(tr.sum()),4))
print("per-fold lag-1 ACF of 1h returns (BTC, ETH, DOGE):")
for nm in SLICES:
    m=in_slice(P.index,nm); print(nm, {c: round(r1[c][m].autocorr(1),3) for c in ["BTC","ETH","DOGE"]})

print("\n== 4 CROSS-COLUMN: correlation of 1h returns across coins (TRAIN, pairwise); impostor checks")
C=r1[tr].corr().round(2); print(C.to_string())
# primary vs binance close return twin
print("\nprimary return vs Binance close return, corr by slice (BTC/ETH) and share of bars where prim price == binance close:")
for nm in SLICES:
    m=in_slice(P.index,nm)
    out={}
    for c in ["BTC","ETH","DOGE"]:
        bc=back(S["close"],NS*False,1)[c][m]; out[c]=(round(r1[c][m].corr(bc),4), round(((P[c][m]-S["close"][c][m]).abs()<1e-9).sum()/max(P[c][m].notna().sum(),1),3))
    print(nm,out)
cb=pd.concat([np.log(S["quote_vol"][c]) for c in COINS],axis=1)
print("\ncorr(|ret|, log quote vol) pooled: ", round(pd.concat([r1[c][tr].abs() for c in COINS]).corr(pd.concat([np.log(S['quote_vol'][c].where(S['quote_vol'][c]>0))[tr] for c in COINS])),3))
print("taker identity: buy_vol/vol mean by coin:", (S["buy_vol"]/S["vol"])[tr].mean().round(3).to_dict())

print("\n== 5 REGIME: by slice - EW-market 1h vol (bp), mean pairwise corr, median trades/hour (BTC), median quote vol (BTC, M$)")
ew=r1[tr].mean(axis=1)
for nm in SLICES:
    m=in_slice(P.index,nm); sub=r1[m]
    cm=sub.corr().values; avgc=(cm.sum()-np.trace(cm)*0)/1  # placeholder
    n=cm.shape[0]; off=np.nanmean(cm[np.triu_indices(n,1)])
    print(f"{nm}: ew_vol {r1[m].mean(axis=1).std()*1e4:.1f}  mean_pair_corr {off:.2f}  BTC trades/h {S['n']['BTC'][m].median():.0f}  BTC qvol/h {S['quote_vol']['BTC'][m].median()/1e6:.1f}M  cs_dispersion {r1[m].std(axis=1).mean()*1e4:.1f}bp")

print("\n== 6 INTRADAY/WEEKLY shape (TRAIN, pooled over coins): mean |1h return| bp by UTC hour; quote-vol index; by weekday")
ab=pd.concat([r1[c][tr].abs() for c in COINS],axis=1).mean(axis=1)
byh=ab.groupby(ab.index.hour).mean()*1e4; byd=ab.groupby(ab.index.dayofweek).mean()*1e4
qv=(S["quote_vol"]/S["quote_vol"].rolling(24*30,min_periods=24*10).mean())[tr].mean(axis=1)
print("abs-ret by hour:", byh.round(1).to_dict()); print("by dow(0=Mon):", byd.round(1).to_dict())
print("volume index by hour:", qv.groupby(qv.index.hour).mean().round(2).to_dict())
fig,ax=plt.subplots(1,2,figsize=(11,4)); ax[0].bar(range(24),byh.values,color=PAL[0]); ax[0].set_title("mean |1h ret| bp by UTC hour"); ax[1].bar(range(7),byd.values,color=PAL[1]); ax[1].set_title("mean |1h ret| bp by weekday (0=Mon)")
fig.savefig("plots/00_intraday.png",bbox_inches="tight"); plt.close(fig)

print("\n== 7 WHAT A ROW IS: stamp check (open-stamped, price = bar END): corr of primary 1h return with Binance (close_t/close_t-1) vs (close_t+1/close_t) and open-stamp: bar t open == close t-1?")
for c in ["BTC","ETH"]:
    o=S["open"][c][tr]; cl=S["close"][c].shift(1)[tr]
    print(c,"open_t == close_{t-1} share:", round(((o-cl).abs()<1e-9).mean(),3))
    x=r1[c][tr]; bc=np.log(S["close"][c]/S["close"][c].shift(1))[tr]
    print(c,"corr(prim ret_t, binance close ret_t):",round(x.corr(bc),4)," vs binance close ret_{t+1}:",round(x.corr(bc.shift(-1)),4)," vs ret_{t-1}:",round(x.corr(bc.shift(1)),4))
fig,ax=plt.subplots(figsize=(8,4))
ew=(r1[tr]).mean(axis=1).rolling(24*30).std()*1e4*np.sqrt(24)
ax.plot(ew.index,ew.values,color=PAL[0]); ax.set_title("30d rolling daily-equivalent EW-market vol (bp/day)")
for nm,(a,b_) in SLICES.items(): ax.axvline(pd.Timestamp(a),color="#9b9a94",lw=.7)
fig.savefig("plots/00_regime.png",bbox_inches="tight"); plt.close(fig)
