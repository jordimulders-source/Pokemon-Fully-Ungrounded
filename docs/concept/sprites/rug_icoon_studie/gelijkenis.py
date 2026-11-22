"""Gelijkenis per kenmerk: verhoudingen in de kop van het icoon tegen de front (wiskundig, geen oordeel op het oog).
Herkenningspunten in de front staan per soort vast (FRONT); in het icoon worden ze gezocht (pal2-indexen).
python3 gelijkenis.py icon.png [soort]   -> per verhouding front, icoon, verschil in icoonpixels"""
import sys,numpy as np
from PIL import Image
from scipy import ndimage as nd
FRONT={'viscacha':dict(snuit=(8.5,34.0),oog=(16.0,30.0),wangpluk=(7.5,30.5),kraag=(22.5,32.0),kopboven=25.5,kin=38.5,
                       oor_ver=(12.0,15.0),oor_nabij=(25.0,16.0))}
def zoek(a):
    m=a>0; geel=np.isin(a,[8,9]); lab,n=nd.label(geel)
    cl=[(np.argwhere(lab==k)) for k in range(1,n+1)]
    cl=[c for c in cl if len(c)>=2]
    wit=np.argwhere(a==3)
    # oog = witte pixel met donker ernaast, in de bovenste helft
    oog=None
    for y,x in wit:
        nb=a[max(0,y-1):y+2,max(0,x-1):x+2]
        if (nb==15).sum()>=2 and y<20: oog=(x+.5,y+.5); break
    cen=[(c[:,1].mean()+.5,c[:,0].mean()+.5) for c in cl]
    # kraag = gele cluster rechts van het oog en dichtstbij; wangpluk = links van het oog
    groot=[(len(c),cc) for c,cc in zip(cl,cen) if cc[0]>oog[0] and abs(cc[1]-oog[1])<=3 and cc[0]<oog[0]+8]
    kraag=max(groot)[1]
    wang=min([c for c in cen if c[0]<oog[0]],key=lambda c:abs(c[0]-oog[0]))
    # snuit = meest linkse niet-grijze pixel binnen 3 rijen onder het oog (snorharen 14/1 overgeslagen)
    best=None
    for y in range(int(oog[1]),int(oog[1])+4):
        xs=[x for x in range(32) if a[y,x]>0 and a[y,x] not in (1,14,8,9)]
        if xs and (best is None or xs[0]<best[0]): best=(xs[0]+.5,y+.5)
    # kopboven = laagste rij tussen de oren (kolom tussen oorbases) ; kin = eerste rij onder het oog met grijze/donkere onderrand bij de snuit
    kol=int(round((oog[0]+kraag[0])/2)); col=np.nonzero(m[:,kol])[0]
    # bovenste kopkolom tussen de oren: eerste rij na de oorgleuf
    rows=[y for y in range(int(oog[1])) if m[y,kol]]
    kopb=min(rows)+.5 if rows else oog[1]-3
    kin=None
    for y in range(int(oog[1])+1,32):
        if a[y,int(best[0])+1] in (14,15) or a[y,int(best[0])+1]==0: kin=y+.5; break
    return dict(snuit=best,oog=oog,wangpluk=wang,kraag=kraag,kopboven=kopb,kin=kin)
a=np.array(Image.open(sys.argv[1]))[:32]; F=FRONT[sys.argv[2] if len(sys.argv)>2 else 'viscacha']; I=zoek(a)
def rel(P):
    s,o,k=P['snuit'],P['oog'],P['kraag']
    return {'oog horizontaal (snuit=0, kraag=1)':(o[0]-s[0])/(k[0]-s[0]),
            'oog verticaal (kopboven=0, kin=1)':(o[1]-P['kopboven'])/(P['kin']-P['kopboven']),
            'wangpluk horizontaal':(P['wangpluk'][0]-s[0])/(k[0]-s[0]),
            'kraag hoogte t.o.v. oog (in kophoogtes)':(k[1]-o[1])/(P['kin']-P['kopboven'])}
rf,ri=rel(F),rel(I)
schaal_x=I['kraag'][0]-I['snuit'][0]; schaal_y=I['kin']-I['kopboven']
print('gevonden in icoon:',{k:(tuple(round(v,1) for v in w) if isinstance(w,tuple) else w) for k,w in I.items()})
for k in rf:
    d=ri[k]-rf[k]; px=d*(schaal_y if ('verticaal' in k or 'hoogte' in k) else schaal_x)
    print(f'{k:42s} front {rf[k]:.2f}  icoon {ri[k]:.2f}  verschil {px:+.1f} px', '' if abs(px)<0.75 else '<-- aanpassen')
