# Capykart eindkeuring_dc variant b (op verzoek coördinator, 24 nov): bovenop bouw.py
# 1 binnenlijnen = donkerste eigen tint (taps), zwart alleen waar ze op de zwarte buitenlijn aansluiten of in de diepe spleet onder kin/nek;
# 2 tanden weer wit (240,240,232) zoals r17b; 3 kop: één compacte bolling op het voorhoofd + smalle op de snuitrug, rest midden, sikkel rechts/onder; B4 minder geel.
import sys; _argv=sys.argv[:]; sys.argv=['x']
exec(open('eindkeuring_dc/bouw.py').read().replace("if __name__=='__main__'","if False"))
sys.argv=_argv
PAL[CR]=(240,240,232)          # tanden wit (r17b); creme had geen andere rol meer
PAL[B4]=(236,166,108)          # lichtste vachttint minder geel (was 238,174,104; hue 31 -> 27)
logb=[]
# ---------- 3: kop opnieuw ----------
kop=(d==1)&~ring
oud=n.copy()
bol=np.zeros((64,64),bool)
for y in range(64):
    for x in range(64):
        if kop[y,x] and ((x-27)/4.6)**2+((y-16.4)/2.0)**2<=1: bol[y,x]=True   # voorhoofd, linksboven op de kop
for x in range(16,25):                                                          # snuitrug: eerste vulpixel onder de bovenlijn
    ys=[y for y in range(10,30) if kop[y,x] and (x,y) not in BESCHERMD]
    if ys:
        bol[ys[0],x]=True
        if 18<=x<=22 and ys[0]+1<30 and kop[ys[0]+1,x]: bol[ys[0]+1,x]=True
lv=np.where(kop,1,-1)
lv[kop&(niveau==0)]=0
lv[bol]=2
# schaduw: alleen stukken die aan de rand/nek raken (sikkel), losse donkere stukjes -> midden
lab,k=nd.label(lv==0,structure=np.ones((3,3)))
rand_=nd.binary_dilation(~kop&(d!=14),structure=np.ones((3,3)))
for i in range(1,k+1):
    c=lab==i
    if not (c&rand_).any() or c.sum()<3: lv[c]=1
r=RAMP[1]
for y,x in zip(*np.where(kop)):
    t=r[lv[y,x]]
    if detail[y,x] and lv[y,x]>0 and not bol[y,x]: t=r[lv[y,x]-1]   # vachtlijnen uit het model blijven één stap
    n[y,x]=t
logb.append('kop: %d px andere tint; bolling %d px'%(int((n!=oud).sum()),int(bol.sum())))
# vlekjes in de kop
for _ in range(3):
    for t in (B2,B3,B4):
        lab,k=nd.label((n==t)&kop,structure=np.ones((3,3)))
        for i in range(1,k+1):
            c=lab==i
            if c.sum()>=3: continue
            b=[n[yy,xx] for y,x in zip(*np.where(c)) for yy in range(y-1,y+2) for xx in range(x-1,x+2) if kop[yy,xx] and not c[yy,xx]]
            if b: n[c]=max(set(b),key=b.count)
# ---------- 1: binnenlijnen ----------
OOG_ENZ={p for p in BESCHERMD}
TOREN_SEL={13:GD,10:B2,11:B0,12:BD}
tel={'eigen':0,'zwart_aansluiting':0,'zwart_spleet':0}
binnen=zwart&~ring
for y,x in zip(*np.where(binnen)):
    if (x,y) in OOG_ENZ: continue
    aan=any(0<=y+dy<64 and 0<=x+dx<64 and ring[y+dy,x+dx] and n[y+dy,x+dx]==K for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)])
    if aan: n[y,x]=K; tel['zwart_aansluiting']+=1; continue
    if 22<=x<=47 and 29<=y<=42 and ML[y,x]<50 and not any(d[yy,xx] in (9,10,11,12,13) for yy in range(y-1,y+2) for xx in range(x-1,x+2)):
        n[y,x]=K; tel['zwart_spleet']+=1; continue
    buren=[d[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if (yy,xx)!=(y,x) and d[yy,xx]>0]
    if 9 in buren: t=HD                                   # hoepel ligt voor: zijn donkerste tint
    elif y>0 and d[y-1,x] in TOREN_SEL: t=TOREN_SEL[d[y-1,x]]   # onderrand van het blok erboven
    elif any(b in TOREN_SEL for b in buren): t=TOREN_SEL[max(set([b for b in buren if b in TOREN_SEL]),key=[b for b in buren if b in TOREN_SEL].count)]
    else: t=B0
    n[y,x]=t; tel['eigen']+=1
logb.append('binnenlijnen (r17-zwart, niet buitenrand, niet oog/neus/mond): %s'%tel)
assert ((n==0)==(o==0)).all()
for (x,y) in BESCHERMD:
    assert n[y,x]==oud[y,x], ('gezicht gewijzigd',x,y)
if __name__=='__main__':
    opslaan(n,'eindkeuring_dc/capykart_b.png'); np.save('eindkeuring_dc/_n_b.npy',n)
    rgb(n,(255,255,255)).resize((512,512),Image.NEAREST).save('eindkeuring_dc/capykart_b_8x.png')
    print('silhouet-diff',int(((n==0)!=(o==0)).sum()),'kleuren',len(set(n.ravel())))
    for l in logb: print(l)
