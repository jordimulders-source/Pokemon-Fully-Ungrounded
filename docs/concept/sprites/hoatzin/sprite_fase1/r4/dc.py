# Kuiken r4: Dragonfly Cave-eindkeuring op r3 (alleen belijning + tinten; silhouet gelijk, behalve gaatje (32,45) dicht).
# DC-gids r. 85-125/445-460: outline base in eigen donkere tint aan de lichtkant (linksboven), zwart (outline shadow) aan de
# schaduwkant en waar delen tegen elkaar liggen; binnenlijnen in eigen donkere tint. Werkwijze als fase 2 r5 (sprite/r5/dc.py).
import numpy as np, os
from PIL import Image
HIER=os.path.dirname(os.path.abspath(__file__)); R3=HIER+'/../r3/'
# palet: hue shift (schaduw koeler/blauwer, licht warmer); dons blijft zwartig; geel alleen in het dons; 12 = selout grijs
PAL=[(152,208,160),(16,16,20),
 (34,37,46),(53,56,64),(78,80,84),(98,102,114),     # 2-5 dons (2 = ook selout dons), 5 = koele schaduw (ook grijs)
 (82,78,46),(122,114,66),                            # 6-7 geel (ongewijzigd)
 (124,126,134),(154,154,154),(182,181,176),          # 8-10 grijs: midden, licht (neutraal), hooglicht warm
 (228,228,228),(66,68,80)]                           # 11 (ongebruikt), 12 selout grijs (koel donker)
DONS={2,3,4,6,7}; GRIJS={8,9,10}
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy,dx)!=(0,0)]; N4=((-1,0),(1,0),(0,-1),(0,1))
def tr(a,y,x): return y<0 or x<0 or y>=64 or x>=64 or a[y,x]==0
def groep(a,y,x):
    c=[a[y+dy,x+dx] for dy,dx in N8 if not tr(a,y+dy,x+dx)]
    d=sum(v in DONS for v in c); g=sum(v in GRIJS for v in c)
    if d==0 and g==0: return 'G' if any(v==5 for v in c) and y>=36 else ('D' if any(v==5 for v in c) else None)
    return 'D' if d>=g else 'G'
SEL={'D':2,'G':12}
# binnenlijnen (r3-coördinaten, gecontroleerd op buren): zwart -> eigen tint
BINNEN={(28,33):2,(27,34):2,(23,36):2,(39,37):2,(40,37):2,(24,39):2,(24,40):2,(24,41):2,   # dons-lijnen / vleugel over lijf
        (35,39):12,(35,40):12,(35,41):12,(35,42):12,(35,43):12,(35,44):12,                 # lichtkant van de dij tegen het lijf
        (37,40):12,(17,41):12}                                                             # losse zwarte stip in dij / linkervleugel
def bewerk(a):
    a=a.copy(); tel={}
    def t(k): tel[k]=tel.get(k,0)+1
    if a[45,32]==0: a[45,32]=1; t('gaatje dicht')
    o=a.copy()
    for (x,y),v in BINNEN.items():
        assert a[y,x]==1,(x,y); o[y,x]=v; t('binnenlijn')
    for y in range(64):
        for x in range(64):
            if a[y,x]!=1 or not any(tr(a,y+dy,x+dx) for dy,dx in N4): continue
            if (tr(a,y-1,x) and tr(a,y+1,x)) or (tr(a,y,x-1) and tr(a,y,x+1)): continue   # dunne delen/haren: zwart (leesbaar)
            ny=sum(dy for dy,dx in N8 if tr(a,y+dy,x+dx)); nx=sum(dx for dy,dx in N8 if tr(a,y+dy,x+dx))
            if not (nx+ny<0): continue          # strikt: normaal naar links/boven/linksboven
            g=groep(a,y,x)
            if g: o[y,x]=SEL[g]; t('selout '+g)
    # rand eenduidig: geen zwart/selout om en om (randpixel die van al zijn randburen verschilt volgt ze)
    rand=lambda b,y,x: b[y,x] in (1,2,12) and any(tr(b,y+dy,x+dx) for dy,dx in N4)
    for _ in range(2):
        for y in range(64):
            for x in range(64):
                if not rand(o,y,x) or (y,x)==(45,32): continue
                nb=[o[y+dy,x+dx] for dy,dx in N8 if 0<=y+dy<64 and 0<=x+dx<64 and rand(o,y+dy,x+dx)]
                if len(nb)>=2 and len(set(nb))==1 and nb[0]!=o[y,x] and ((nb[0]==1)!=(o[y,x]==1)):
                    o[y,x]=nb[0]; t('rand eenduidig')
    return o,tel
def save(c,fn):
    im=Image.fromarray(c,'P'); im.putpalette(sum(PAL,())+(0,)*(768-3*len(PAL))); im.save(fn,transparency=0)
if __name__=='__main__':
    for src,dst in (('kuiken_r3.png','kuiken_r4.png'),('kuiken_r3_haarB.png','kuiken_r4_haarB.png')):
        a=np.array(Image.open(R3+src)); o,tel=bewerk(a); save(o,HIER+'/'+dst)
        al=(a>0)!=(o>0); print(dst,tel,'gewijzigd',int((o!=a).sum()),'alpha-diff',int(al.sum()),[tuple(p[::-1]) for p in np.argwhere(al)])
        print('  zwart % voor',round((a==1).sum()/(a>0).sum()*100,1),'na',round((o==1).sum()/(o>0).sum()*100,1),'kleuren',len(set(o.flat)-{0}))
        ch='.KdDmMyYgGlWs'
        for y in range(20,64): print('  %2d '%y+''.join((ch[o[y,x]].upper() if o[y,x]!=a[y,x] and o[y,x]!=1 else ch[o[y,x]]) if o[y,x]!=a[y,x] or True else '' for x in range(12,52)))
