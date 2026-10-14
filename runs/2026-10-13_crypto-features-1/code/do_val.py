import sys
sys.path.insert(0, r"C:\Users\User\eda-routine\runs\2026-10-13_crypto-features-1\code")
import confirm as cf
nn, fid = int(sys.argv[1]), sys.argv[2]
cf.begin_val(nn, fid)
cf.run_val(nn, fid)
cf.write_val_result(nn, fid)
cf.kit.write_beliefs()
print("posterior", cf.kit.posterior(cf.kc.hyp_of(f"F{cf._resolve(fid)[1]}")))
