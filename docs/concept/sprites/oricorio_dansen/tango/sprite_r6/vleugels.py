# r6 punt 1: vleugelomtrek schoon. Alleen binnen de vleugelzones. Silhouet uit de modeldekking (2x2 natieve cellen, >= 0,5),
# daarna Gen 3-lijnregels: uitsteeksels (>=3 lege 4-buren) weg, inhammen van 1 px (>=3 dekkende 4-buren) dicht, lijn = randpixels (1 px, 8-verbonden),
# oude randlijn die binnen komt te liggen -> vlaktint, selout aan de lichtkant. Tellingen in log_vleugels.json.
import numpy as np, json
from collections import Counter
o=np.load('tango_r5.npy').copy(); r5=o.copy(); D=np.load('dekking.npy'); L=np.load('model_L.npy'); H,W=o.shape
_,O,D0,D1,D2,D3,D4=range(7); DONK=(D0,D1,D2,D3,D4)
def zone(y,x): return (y<=28 and x>=47) or (19<=y<=28 and x>=38) or (26<=y<=40 and x<=21)
Z=np.array([[zone(y,x) for x in range(W)] for y in range(H)])
log={}
def tel(k,n=1): log[k]=log.get(k,0)+n
def nb(y,x): return [(y+a,x+b) for a,b in((-1,0),(1,0),(0,-1),(0,1))]
def op(m,y,x): return 0<=y<H and 0<=x<W and m[y,x]
m=o>0
# 1. silhouet uit de modeldekking
for y in range(H):
    for x in range(W):
        if not Z[y,x]: continue
        v=D[y,x]>0.5 or (D[y,x]==0.5 and m[y,x])
        if v!=m[y,x]: m[y,x]=v; tel('1_dekking_'+('erbij' if v else 'eraf'))
# 1b. gelijkspel (dekking precies 0,5) dat de trap onregelmatig maakt: (33,4) weg -> starts linkervleugel 10,8,5,1 (stappen 2,3,4)
for y,x in ((33,4),):
    if m[y,x]: m[y,x]=False; tel('1b_gelijkspel_trap')
# 2. uitsteeksels weg / inhammen dicht (2 rondes)
for it in range(2):
    for y in range(H):
        for x in range(W):
            if not Z[y,x]: continue
            n=sum(op(m,a,b) for a,b in nb(y,x))
            if m[y,x] and n<=1: m[y,x]=False; tel('2_uitsteeksel_weg')
            elif not m[y,x] and n>=3: m[y,x]=True; tel('2_inham_dicht')
# 3. klassen: nieuw -> meest voorkomende vlakbuur, weg -> transparant
oud_rand=np.array([[r5[y,x]>0 and any(not op(r5>0,a,b) for a,b in nb(y,x)) for x in range(W)] for y in range(H)])
for y in range(H):
    for x in range(W):
        if not Z[y,x]: continue
        if not m[y,x]: o[y,x]=0
        elif r5[y,x]==0:
            c=Counter(r5[a,b] for a,b in nb(y,x) if op(r5>0,a,b) and r5[a,b] in DONK); o[y,x]=c.most_common(1)[0][0] if c else D4
# 4. lijn: randpixels in de zone -> zwart; oude randlijn (zwart/selout) die nu binnen ligt -> vlaktint
for y in range(H):
    for x in range(W):
        if not Z[y,x] or not m[y,x]: continue
        rand=any(not op(m,a,b) for a,b in nb(y,x))
        if rand and o[y,x]!=O: o[y,x]=O; tel('4_randlijn')
        elif not rand and oud_rand[y,x] and o[y,x] in (O,D4) and r5[y,x]!=0:
            c=Counter(o[a,b] for a,b in nb(y,x) if o[a,b] in DONK and not oud_rand[a,b])
            if c:
                v=c.most_common(1)[0][0]
                if v!=o[y,x]: o[y,x]=v; tel('4_oude_rand_naar_vlak')
# 5. selout aan de lichtkant (leeg boven of links, niet onder/rechts). Het model heeft langs de voorrand van de vleugels een lichte band
#    (L 50-72, gemeten): selout D3 waar de modelrand licht is (L>=45), anders D4; de vlakpixel erachter D2 als het model daar licht is (L>=45).
for y in range(H):
    for x in range(W):
        if not Z[y,x] or o[y,x]!=O: continue
        up=not op(m,y-1,x); lf=not op(m,y,x-1); dn=not op(m,y+1,x); rt=not op(m,y,x+1)
        if not(up or lf) or dn or rt: continue
        o[y,x]=D3 if L[y,x]>=45 else D4; tel('5_selout_'+('D3' if L[y,x]>=45 else 'D4'))
        for a,b in [p for p,ok in (((y+1,x),up),((y,x+1),lf)) if ok]:
            if op(m,a,b) and Z[a,b] and o[a,b] in (D3,D4) and not any(not op(m,p,q) for p,q in nb(a,b)) and L[a,b]>=45:
                o[a,b]=D2; tel('5_lichte_voorrand_D2_op_model')
# 6. dubbele lijn: zwarte binnenclusters (<3 px) die tegen de randlijn liggen -> vlaktint; 7. lichte spikkels (D0-D2, <3 px) in de vleugels -> vlaktint
def comps(mask):
    seen=np.zeros(mask.shape,bool); out=[]
    for y in range(H):
        for x in range(W):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)]; seen[y,x]=True; pts=[]
                while st:
                    a,b=st.pop(); pts.append((a,b))
                    for p,q in nb(a,b):
                        if 0<=p<H and 0<=q<W and mask[p,q] and not seen[p,q]: seen[p,q]=True; st.append((p,q))
                out.append(pts)
    return out
rand=np.array([[m[y,x] and any(not op(m,a,b) for a,b in nb(y,x)) for x in range(W)] for y in range(H)])
binnenO=(o==O)&~rand&Z
for pts in comps(binnenO):
    if len(pts)>=3: continue
    if not any(rand[p,q] for a,b in pts for p,q in nb(a,b) if 0<=p<H and 0<=q<W): continue
    for a,b in pts:
        c=Counter(o[p,q] for p,q in nb(a,b) if o[p,q] in (D1,D2,D3,D4) and not rand[p,q]); o[a,b]=c.most_common(1)[0][0] if c else D4; tel('6_dubbele_lijn_weg')
for k in (D0,D1,D2):
    for pts in comps((o==k)&Z):
        if len(pts)>=3: continue
        c=Counter(o[p,q] for a,b in pts for p,q in nb(a,b) if 0<=p<H and 0<=q<W and o[p,q] in DONK and o[p,q]!=k)
        if c:
            for a,b in pts: o[a,b]=c.most_common(1)[0][0]; tel('7_spikkel_weg')
np.save('na_vleugels.npy',o)
sil=int(((o>0)!=(r5>0)).sum()); log['silhouet_px_veranderd']=sil; log['px_veranderd_totaal']=int((o!=r5).sum())
json.dump(log,open('log_vleugels.json','w'),indent=0); print(log)
