# Kene ronde 9: de loop komt uit de 3D-projectie (silhouet/kene_dik_64.npy). Omlijning blijft staan.
# Met de hand: hapjes gevuld en dunne stukken langs dezelfde loop verdikt tot >= 3 px (lijst EXTRA), niets herschikt.
# Kleur vlak: lichtkant f (idx 15, maanzilver), lijfschaduw m (idx 6); 1 px basis b tussen patroon en vachthooglicht l.
import os, numpy as np
H=os.path.dirname(os.path.abspath(__file__))
K=np.load(os.path.join(H,'../../../silhouet/kene_dik_64.npy'))
g=[['.']*64 for _ in range(64)]
for line in open(os.path.join(H,'raster.txt')):
    line=line.split('#')[0].strip()
    if not line: continue
    y,x,st=line.split()
    for i,ch in enumerate(st): g[int(y)][int(x)+i]=ch
def blok(x0,x1,y0,y1): return {(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)}
EXTRA=set()
EXTRA|=blok(19,21,29,30)|{(22,28),(22,29),(23,29)}      # voorste punt van de rugband: 1 px -> 3x3, hapje dicht
EXTRA|=blok(38,38,34,38)                                # band 2 omlaag: 2 px breed -> 3 (naar binnen, langs dezelfde lijn)
EXTRA|=blok(43,44,35,36)|blok(44,45,37,40)|{(44,34)}     # band 3 langs het achterlijf: 1-2 px -> 3 (naar binnen)
EXTRA|={(33,28),(34,29),(40,32),(41,34)}                 # bovenkant band 2 en de splitsing band 2/3: 1-2 px -> 3
EXTRA|={(43,37),(46,35),(46,40),(44,41),(45,41),(46,41),(42,41)}   # band 3 en voet band 2: dunne stukken dichtgezet
EXTRA|={(33,29),(41,35),(42,35),(45,34)}   # laatste dunne plekken (bovenkant band 2, splitsing, band 3 boven)
RUIS={(32,26)}                                          # los projectiepuntje tegen de omlijning
P=({(x,y) for y in range(64) for x in range(64) if K[y,x]}|EXTRA)-RUIS
P={(x,y) for (x,y) in P if g[y][x] not in '.kd' and 17<=x<=49 and 24<=y<=50}
out={}
for (x,y) in P: out.setdefault(y,{})[x]='m' if g[y][x]=='s' else 'f'
for (x,y) in P:
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            X,Y=x+dx,y+dy
            if (X,Y) not in P and g[Y][X]=='l' and 17<=X<=49 and 24<=Y<=50 and not (X<=24 and Y>=36): out.setdefault(Y,{})[X]='b'
lines=['# ---- ronde 9: kene volgens de 3D-projectie (f licht / m schaduw, 1 px basis langs het hooglicht) ----']
for y in sorted(out):
    xs=sorted(out[y]); run=[xs[0]]
    for x in xs[1:]+[None]:
        if x is not None and x==run[-1]+1: run.append(x); continue
        lines.append('%d %d %s'%(y,run[0],''.join(out[y][i] for i in run)))
        if x is not None: run=[x]
print('\n'.join(lines))
buiten=[p for p in P if not K[p[1],p[0]]]
print('# kene-pixels: %d, waarvan buiten de projectie (verdikking): %d'%(len(P),len(buiten)))
open(os.path.join(H,'kene_pixels.txt'),'w').write('\n'.join('%d %d'%p for p in sorted(P)))
