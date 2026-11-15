# Ronde 6 van de steenjaguar-welp. Basis: r5 (silhouet, posities, spiralen). Elke wijziging is een benoemde zone;
# per zone wordt het aantal gewijzigde pixels t.o.v. r5 gelogd.
# Bronnen: model_welp_gekozen.png (orig = 99.3+16.9x, 191.5+16.9y; zie grid.py/punt.py), facetkaart facet.py/auto2.py.
import numpy as np
r5=np.load('welp_r5.npy'); auto2=np.load('auto2.npy'); H,W=r5.shape
edge=np.zeros((H,W),bool)   # buitenrand van r5 (blijft)
for y in range(H):
    for x in range(W):
        if r5[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or r5[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): edge[y,x]=True
np.save('edge.npy',edge)
CH='.KdSMLPQRgWCTGH'; IX={c:i for i,c in enumerate(CH)}
a=r5.copy(); log={}
def zone(naam,mask_or_fn):
    global a
    oud=a.copy(); mask_or_fn(); n=int((a!=oud).sum()); log[naam]=log.get(naam,0)+n
def rijen(x0,y0,rows):
    """schrijf tekstrijen (alleen tekens != ' ') vanaf (x0,y0)"""
    for j,r in enumerate(rows):
        for i,c in enumerate(r):
            if c!=' ': a[y0+j,x0+i]=IX[c]

# --- 1. Lijf rechts/onder (x>=20 r13-38, en r32-38 overal): facettonen van het model (auto2: helderheid -> S/M/L,
#        modusfilter, korrels<4 weg), patronen ongemoeid; structuurlijnen (lijnbruin) van het model blijven.
STRUCT={(27,34),(27,35),(27,36),(28,33),(28,37),(28,38),(28,39),(29,31),(29,40),(31,30),(31,41),(36,30),(36,41),
        (35,43),(36,43),(37,42),(38,42),(31,25),
        (29,32),(30,31),(32,30),(33,30),(34,30),(35,30)}   # haarlijn dij doorgetrokken (model: ononderbroken contour x~30)|{(y,19) for y in range(30,37)}|{(y,27) for y in range(31,40)}
def f1():
    for y in range(13,39):
        for x in range(W):
            if (x>=20 or y>=32) and not edge[y,x] and r5[y,x] in (2,3,4,5):
                a[y,x]=2 if (y,x) in STRUCT else auto2[y,x]
zone('lijf_facetten',f1)

# --- 2. Kop boven (r0-12): voorhoofdsband als lila golfband (haarspeld, 2 strengen + bruine binnenlijn) op de modelplek,
#        oren, oog (Gen 3-opbouw: bovenlid K, glans W, pupil K, lichte iris C/G, sclera g), verre oog (glans), snuitrug H.
def f2():
    rijen(0,0,[
    ".....dK.............ddK...",
    "....dMMdK.ddddK...ddLLMK..",
    "....dMMMMdRRRRRdddLLMMMK..",
    "....dSSMRRRPPRLLLLLKKSSMK.",
    "....dSRRRPRRRLLLLLKKSSSMK.",
    "....dSRRPRLLLLLLMMdSSSSMK.",
    "....dRRPRLLLLLLMMMMdSSSMK.",
    "...dLLRRQMMMMMMMMMMMSSSK..",
    "...ddLLLMdKKKKMMMMMMMMK...",
    "...KWMMMSKWKGgdMMMMLLdK...",
    "...KKMLLSKCKCgMMMLLLLdK...",
    "...dLHHLLMCCCMMMMLLLLMMK..",
    "...dHHLMLLLLLLMMMMMMSSdSK.",
    ])
zone('kop_boven',f2)

# --- 3. Snuit/neus/mond/tong/kaak (r13-22, x<20) + kaaklijn als rechte trap (12,21)->(22,14)
def f3():
    rijen(0,13,[
    "..dKKKKMLLLMMMMMMMSS",
    ".KSSSKMLLLMMMMMMMSSS",
    "..dMKMMMMMMdMSSSSSSS",
    "..KMKMMMMMKKdSSSSSSS",
    "...KKKKKKKdKSSSSSSSS",
    "....KWTTWddKSSSSSSSS",
    ".....TTTdddKSSSSSSSS",
    "....dTTTdWdSdSSSSSSS",
    "....TTTdMMMKdSSSSSSS",
    "....dTTKKKK.ddLLLLCR",
    ])
    for (y,x) in [(21,12),(20,12),(19,13),(19,14),(18,15),(18,16),(17,17),(17,18),(16,19),(16,20),(15,21),(14,22)]:
        a[y,x]=IX['d']
    for (y,x) in [(15,20),(17,16)]: a[y,x]=IX['S']
zone('snuit_mond_kaak',f3)

# --- 4. Opgeheven poot (r23-31, x<12): 3 tenen met 2 korte teenlijnen (model x~1.6 en ~4.3), lichte bovenkant,
#        donkere onderkant; borst/schouder (x12-19): lichte borst, schouderlijn (13,24)->(16,29), P-vlekjes weg (niet in model).
def f4():
    rijen(0,23,[
    "..ddLLHLK...ddLLLLPR",
    ".dLLLHHLMK.dMdLLLCPR",
    "dLdLdLHLMMddMMdLLCPR",
    "dLdLdLLMMMMMSSdSSSCR",
    "dMMMMMddSMMMSSSdSSCR",
    "KMMSSSSSSSSSSSSdSSSM",
    ".KKKKKKSSSSSSSSSdSSM",
    ".......KSSSSSSSSKKSd",
    "........KSSSSSSK..dd",
    ])
zone('poot_borst',f4)

# --- 5. Voeten (r39-43): lichte bovenkant met hooglicht, teenlijnen zoals het model (voor x17/x20, achter x35/x38)
def f5():
    rijen(15,39,[
    " dLLHHLLMMMSdSKSSSSSSSSSMMMKKKK",
    "dLLHHLLLMMKKKK.dLLHHLLLMMMK",
    "dLdLLLLMMK.....dMLLLdLLdMK",
    "dLdLLdMMMK.....KSMMMdMMdK",
    "KMdMMdMSK.......KKKKKKKK",
    ])
zone('voeten',f5)

np.save('welp_r6.npy',a)
if __name__=='__main__':
    print(log,'totaal diff r5:',int((a!=r5).sum()))
    print('    '+''.join(str(x%10) for x in range(W)))
    for y in range(H): print('%2d  '%y+''.join(CH[v] for v in a[y]))
