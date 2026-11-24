import json,numpy as np
D=json.load(open("metrics.json"))
keys=["n","area","flat","noise","meancl","chk","inner_dark","edgeL","edge_dark","light","lr","var","sat"]
g={k:np.array([d[k] for d in D["gen3"]]) for k in keys}
print("GEN3   "+"  ".join(f"{k}:{np.percentile(g[k],10):.2f}/{np.median(g[k]):.2f}/{np.percentile(g[k],90):.2f}" for k in keys))
o={k:np.array([d[k] for d in D["ours"]]) for k in keys}
print("OURS   "+"  ".join(f"{k}:{np.percentile(o[k],10):.2f}/{np.median(o[k]):.2f}/{np.percentile(o[k],90):.2f}" for k in keys))
sk=["flat","noise","meancl","chk","var","edgeL","light","lr","n"]
for d in D["ours"]:
    z={}
    for k in sk:
        med=np.median(g[k]); lo,hi=np.percentile(g[k],5),np.percentile(g[k],95); s=(hi-lo)/3.3
        z[k]=(d[k]-med)/s
    d["z"]=z; d["score"]=float(np.sqrt(np.mean([v*v for v in z.values()])))
    d["out"]=[k for k in sk if not (np.percentile(g[k],5)<=d[k]<=np.percentile(g[k],95))]
D["ours"].sort(key=lambda d:d["score"])
for d in D["ours"]:
    print(f'{d["score"]:.2f} {d["date"]} {d["name"][:24]:24} n{d["n"]:2} flat{d["flat"]:.2f} noise{d["noise"]:.2f} cl{d["meancl"]:5.1f} chk{d["chk"]:.3f} var{d["var"]:.2f} edgeL{d["edgeL"]:5.1f} light{d["light"]:5.1f} area{d["area"]} out:{",".join(d["out"])}')
json.dump(D,open("scored.json","w"))
