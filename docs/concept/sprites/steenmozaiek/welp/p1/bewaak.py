# Bewaakt p1-varianten t.o.v. r11 (bevroren): silhouet-diff 0, lijnen (1,2) ongewijzigd, palet gelijk en <=16,
# wijzigingen alleen binnen de patroonzones (materiaalkaart van de variant + oude lijfpatroonpixels van r11).
# Meldt ook per zone het aantal gewijzigde pixels en of de patroontint het facet (bruin eronder) volgt.
import sys, importlib, numpy as np
from PIL import Image
from p1 import r11, B, KEEP
PATR=[6,7,8,11]
def check(var):
    mod=importlib.import_module('var'+var); mat=mod.mat
    im=Image.open('welp_p1_%s.png'%var); a=np.array(im)
    ok=True
    sil=int(((a>0)!=(r11>0)).sum()); print('variant',var,'| silhouet-diff:',sil); ok&=sil==0
    lijn=int(((np.isin(r11,[1,2]))&(a!=r11)).sum()); print('  lijnpixels (1,2) gewijzigd:',lijn); ok&=lijn==0
    pal_ok=im.getpalette()[:48]==Image.open('../r11/welp_r11.png').getpalette()[:48]; n=len(set(a.ravel()))
    print('  palet gelijk aan r11:',pal_ok,'| indexen in gebruik incl. transparant:',n); ok&=pal_ok and n<=16
    zone=np.zeros(a.shape,bool)
    for (x,y) in mat: zone[y,x]=True
    keep=np.zeros(a.shape,bool)
    for (y0,y1,x0,x1) in KEEP: keep[y0:y1,x0:x1]=True
    zone|=np.isin(r11,PATR)&~keep
    d=(a!=r11)
    buiten=int((d&~zone).sum()); print('  diff buiten patroonzones:',buiten); ok&=buiten==0
    print('  diff binnen zones:',int((d&zone).sum()),'px | kop/staartband (KEEP) gewijzigd:',int((d&keep).sum()))
    # facet: tint per basisniveau
    lv={5:'licht',14:'licht',4:'mid',3:'donker',2:'diepst'}
    T={}
    for (x,y),m in mat.items():
        if m in 'CL' and a[y,x] in (6,7,8,9,11,14) and B[y,x] in lv:
            T.setdefault((m,lv[B[y,x]]),{}).setdefault(int(a[y,x]),0); T[(m,lv[B[y,x]])][int(a[y,x])]+=1
    nm={6:'lila-d',7:'lila-m',8:'lila-l',9:'creme-d',11:'creme-l',14:'creme-rand(e)'}
    for k in sorted(T): print('   ',k[0],k[1].ljust(6),{nm[i]:v for i,v in sorted(T[k].items())})
    return ok
if __name__=='__main__':
    alles=all(check(v) for v in (sys.argv[1:] or ['A','B','C']))
    print('ALLES OK' if alles else 'FOUT'); sys.exit(0 if alles else 1)
