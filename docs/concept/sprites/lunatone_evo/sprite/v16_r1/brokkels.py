# Brokkels terug (Jordi 23 nov: "en de brokkels mogen terug"): gaten uit de r5-rand overnemen.
# r5 en v16-sprite bol op bol uitgelijnd (gepaste cirkels: middelpunt + straal, gelijkvormigheid),
# per gat een gebied (gat + 2 px wand + bijbehorende losse plaat, als rechthoek) pixel voor pixel uit r5 gekopieerd
# (zelfde palet). Gaten over gezicht/neus: weglaten.
import sys, numpy as np; from PIL import Image; from scipy import ndimage; import tool
VAR=sys.argv[1] if len(sys.argv)>1 else 'A'
r5=np.array(Image.open('../r5/sprite.png')).astype(int)
g=np.load('groot.npy'); out=g.copy()
c5=np.load('c5.npy'); cg=np.load('cg.npy'); s=cg[2]/c5[2]
J,I=np.mgrid[0:64,0:64]
d5=np.hypot(I+.5-c5[0],J+.5-c5[1])
gap=(d5<c5[2]-0.7)&(r5==0)
lab,n=ndimage.label(gap)
lab2,n2=ndimage.label(r5>0)
sizes=np.bincount(lab2.ravel())
GATEN={'hap rechtsboven':[2,1,3],'hap linksonder (onder de neus)':[4],'opening rechtsonder + losse plaat':[5]}
if VAR=='B': GATEN.pop('opening rechtsonder + losse plaat')
gezicht=np.zeros((64,64),bool)
# gezicht/neus in v16-coords (groot): oog x26-37,y21-36; neus x2-24,y24-33
gezicht[21:37,26:38]=True; gezicht[24:34,2:25]=True
rap=[]
for nm,ks in GATEN.items():
    m=np.isin(lab,ks)
    near=ndimage.binary_dilation(m,iterations=2)
    # losse stukken die het gat raken (de plaat)
    for k in set(lab2[ndimage.binary_dilation(m,iterations=2)])-{0}:
        if sizes[k]<200: m=m|(lab2==k)
    main5=lab2==np.argmax(np.where(np.arange(len(sizes))==0,0,sizes))
    # wig: hoekbereik van het gat (+ plaat), vanaf 2 px binnen het diepste gatpunt tot ver buiten de bol
    gm=np.isin(lab,ks)
    A5=np.arctan2(J+.5-c5[1],I+.5-c5[0])
    ang=A5[gm]; ref=np.angle(np.exp(1j*ang).mean()); da=np.angle(np.exp(1j*(A5-ref)))
    span=np.abs(np.angle(np.exp(1j*(ang-ref)))).max()
    rin=d5[gm].min()-2
    reg=(np.abs(da)<=span+0.06)&(d5>=rin)&(d5<=c5[2]+8)
    reg|=ndimage.binary_dilation(m,iterations=1)&(main5|m|(r5==0))
    ys,xs=np.where(reg); box=(xs.min(),xs.max(),ys.min(),ys.max())
    lg,ng=ndimage.label(out>0); sg=np.bincount(lg.ravel()); sg[0]=0; mainG=lg==np.argmax(sg)
    puinzone=ndimage.binary_dilation((out>0)&~mainG,structure=np.ones((3,3)))
    tx0=ty0=99; tx1=ty1=-1; ch=0; hit_face=False; todo=[]
    for y in range(64):
      for x in range(64):
        sx=int(np.floor(c5[0]+(x+.5-cg[0])/s)); sy=int(np.floor(c5[1]+(y+.5-cg[1])/s))
        if not(0<=sx<64 and 0<=sy<64) or not reg[sy,sx]: continue
        v=r5[sy,sx]
        if v==0 and out[y,x]>0 and not mainG[y,x]: continue   # eigen v16-puin niet wissen
        if v>0 and out[y,x]>0 and not mainG[y,x]: continue    # eigen v16-puin niet overschrijven
        plaat=(v>0) and not main5[sy,sx]
        if plaat and not m[sy,sx]: v=0   # ander r5-puin telt niet mee
        dg=np.hypot(x+.5-cg[0],y+.5-cg[1])
        if v>0 and not plaat and dg>cg[2]+0.3 and not mainG[y,x]: continue  # geen r5-lijf buiten de v16-bol
        if v>0 and puinzone[y,x]: continue   # 1 px afstand tot eigen v16-puin
        todo.append((y,x,v)); hit_face|=gezicht[y,x]
        tx0=min(tx0,x);tx1=max(tx1,x);ty0=min(ty0,y);ty1=max(ty1,y)
    if hit_face: rap.append(f'{nm}: valt over gezicht/neus -> weggelaten'); continue
    for y,x,v in todo:
        if out[y,x]!=v: out[y,x]=v; ch+=1
    rap.append(f'{nm}: r5-gebied x{box[0]}-{box[1]} y{box[2]}-{box[3]} -> v16 x{tx0}-{tx1} y{ty0}-{ty1}; {ch} px uit r5 overgenomen')
# losse snippers (< 4 px) die door het knippen ontstaan: weg; rand van de geknipte zone: zwart (schaduwkant rechts)
lab3,n3=ndimage.label(out>0); sz=np.bincount(lab3.ravel()); snip=0
for k in range(1,n3+1):
    if sz[k]<4 and not (g[lab3==k]>0).all(): out[lab3==k]=0; snip+=sz[k]
zone=(out!=g)
zoneN=ndimage.binary_dilation(zone,iterations=1)
fig=out>0; rim=fig&~ndimage.binary_erosion(fig,structure=[[0,1,0],[1,1,1],[0,1,0]])
lijn=0
for y,x in zip(*np.where(rim&zoneN&(out>=2))):
    if x>=cg[0]-2: out[y,x]=1; lijn+=1
rap.append(f'snippers weg: {snip} px; randpixels in de knipzone naar zwart: {lijn}')
np.save(f'brok_{VAR}.npy',out)
open(f'brokkels_{VAR}.txt','w').write(f'schaal r5->v16 {s:.3f}; r5 c=({c5[0]:.1f},{c5[1]:.1f}) R={c5[2]:.1f}; v16 c=({cg[0]:.1f},{cg[1]:.1f}) R={cg[2]:.1f}\n'+'\n'.join(rap)+'\n')
print(open(f'brokkels_{VAR}.txt').read())
tool.grid(out,f'brok_{VAR}_grid.png',sc=12)
