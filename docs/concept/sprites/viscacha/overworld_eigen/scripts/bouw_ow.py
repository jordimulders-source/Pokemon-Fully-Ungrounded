"""Bouwt de overworldsprite van de viscacha uit de bronrasters in ../bron/.
 voor.half / achter.half: linkerhelft (x0-15), gespiegeld met spiegel.py (symmetrisch, licht linksboven)
 opzij.blk: volledig raster (naar links)
 Elk aanzicht wordt daarna gecentreerd (midden x15-16, onderkant y29); het loopframe schuift mee.
 Loopframes (1, 3, 5) = stilframe + de pootwissels hieronder (voeten, plus een oor als klein gebaar).
Uitvoer in ../af/: overworld.png (192x32, P, index 0 transparant), overworld_normal.pal, overworld_8x.png, loop.gif.
Gebruik (repo-root): python3 docs/concept/sprites/viscacha/overworld_eigen/scripts/bouw_ow.py"""
import sys,os,numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H)
from ow_pal import PAL,rgba; import spiegel,blk
B=H+'/../bron/'; A=H+'/../af/'
def zet(a,y,x0,s):
    for i,c in enumerate(s):
        if c==' ': continue
        a[y,x0+i]=0 if c=='.' else int(c,16)
f0=spiegel.maak(B+'voor.half')
f2=spiegel.maak(B+'achter.half')
f4=blk.lees(B+'opzij.blk')
# loopframes, in de coordinaten van de bronrasters (voor het centreren)
f1=f0.copy(); zet(f1,28,11,'2222'); zet(f1,29,11,'....')          # linkervoorpoot 1 px op
zet(f1,8,11,'..'); zet(f1,9,11,'11')                                 # gebaar: linkeroor 1 px omlaag
f3=f2.copy(); zet(f3,26,9,'65'); zet(f3,27,8,'2222'); zet(f3,28,8,'....')   # linkerachtervoet 1 px op
zet(f3,8,11,'..'); zet(f3,9,11,'11')                                 # gebaar: linkeroor 1 px omlaag
f5=f4.copy(); zet(f5,27,9,'2222.2'); zet(f5,28,9,'.....')            # voorpoot 1 px op, tenen achtervoet 1 px terug
def centreer(a,b):
    ys,xs=np.nonzero(a); dx=int(np.floor(15.5-(xs.min()+xs.max())/2+0.5)); dy=29-ys.max()
    return [np.roll(np.roll(m,dy,0),dx,1) for m in (a,b)]
f0,f1=centreer(f0,f1); f2,f3=centreer(f2,f3); f4,f5=centreer(f4,f5)
F=[f0,f1,f2,f3,f4,f5]
sheet=np.concatenate(F,axis=1).astype(np.uint8)
im=Image.fromarray(sheet,'P'); im.putpalette([c for p in PAL for c in p]); im.info['transparency']=0
os.makedirs(A,exist_ok=True); im.save(A+'overworld.png',transparency=0)
open(A+'overworld_normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in PAL))
BG=(152,208,160)
big=rgba(sheet,bg=BG).resize((192*8,32*8),Image.NEAREST)
from PIL import ImageDraw
d=ImageDraw.Draw(big)
for k in range(1,6): d.line([(k*256,0),(k*256,256)],fill=(90,120,90),width=2)
big.save(A+'overworld_8x.png')
# loop.gif: per aanzicht stil/lopen 4x, 100 ms
fr=[]
for k in (0,2,4):
    for _ in range(4):
        for j in (k,k+1):
            row=np.concatenate([F[j]],axis=1)
            fr.append(rgba(row,bg=BG).resize((128,128),Image.NEAREST).convert('P',palette=Image.ADAPTIVE))
fr[0].save(A+'loop.gif',save_all=True,append_images=fr[1:],duration=100,loop=0)
for i,f in enumerate(F): open(H+'/../werk/frame%d.txt'%i,'w').write(__import__('ow_pal').totext(f)+'\n')
print('ok')
