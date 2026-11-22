# Meet de paletkleuren in het Gemini-model: mediaan per tintgroep, omlijning (l<0.15) niet meegeteld.
# Schrijft per kleur ook een modelplek (de pixel die het dichtst bij de mediaan ligt) naar palet_gemeten.json.
import numpy as np, colorsys, json
from PIL import Image
def laad(f): return np.asarray(Image.open('../model/'+f).convert('RGB')).astype(int)
r1=laad('r1_nat100.png'); r2=laad('r2_nat100.png')
def hls(p):
    h,l,s=colorsys.rgb_to_hls(*(p/255)); return h*360,l,s
def groep(a,cond,naam,bron):
    pts=[(x,y) for y in range(99) for x in range(99) if a[y,x].min()<=225 and cond(*hls(a[y,x]))]
    v=np.array([a[y,x] for x,y in pts]); med=np.median(v,0).round().astype(int)
    i=np.argmin(((v-med)**2).sum(1)); x,y=pts[i]
    return naam,{'rgb':[int(c) for c in med],'n':len(pts),'bron':bron,'plek':[x,y],'plekkleur':[int(c) for c in a[y,x]]}
rood=lambda h:(h<22 or h>=345)
G=dict([
 groep(r1,lambda h,l,s:l<0.15,'k','r1 omlijning (alleen als lijnkleur)'),
 groep(r1,lambda h,l,s:rood(h) and 0.30<=l<0.42 and s>0.3,'r','r1 donkerste lijfschaduw/selout rood'),
 groep(r1,lambda h,l,s:rood(h) and 0.42<=l<0.50 and s>0.3,'H','r1 lijfschaduw'),
 groep(r1,lambda h,l,s:h<14 and 0.50<=l<0.62 and s>0.5,'G','r1 zalmrood lijf'),
 groep(r1,lambda h,l,s:14<=h<24 and 0.50<=l<0.64 and s>0.5,'m','r1 oranje tussentint lijf'),
 groep(r1,lambda h,l,s:24<=h<34 and 0.58<=l<0.70 and s>0.6,'F','r1 licht oranje lijf'),
 groep(r1,lambda h,l,s:34<=h<55 and 0.28<=l<0.42,'E','r1 donker mosterd (selout/lijn geel)'),
 groep(r1,lambda h,l,s:34<=h<55 and 0.48<=l<0.58,'D','r1 mosterd schaduw'),
 groep(r1,lambda h,l,s:34<=h<55 and 0.58<=l<0.68,'C','r1 mosterd midden'),
 groep(r1,lambda h,l,s:34<=h<55 and 0.68<=l<0.80,'B','r1 mosterd licht'),
 groep(r2,lambda h,l,s:45<=h<60 and l>=0.62 and s>0.8,'A','r2 kuifgeel (lichtste geel)'),
 groep(r1,lambda h,l,s:(h>=340 or h<12) and l>=0.68 and s<0.75,'p','r1 roze licht'),
 groep(r1,lambda h,l,s:h>=340 and 0.55<=l<0.68,'q','r1 roze midden'),
 groep(r1,lambda h,l,s:h>=340 and 0.35<=l<0.48,'s','r1 roze schaduw'),
])
for k,v in G.items(): print(k,v)
json.dump(G,open('palet_gemeten.json','w'),indent=1)
