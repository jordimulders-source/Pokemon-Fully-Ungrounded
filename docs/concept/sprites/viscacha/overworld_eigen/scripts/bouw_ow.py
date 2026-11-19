"""Bouwt de overworldsprite van de viscacha uit de bronrasters in ../bron/.
 voor.half / achter.half: linkerhelft (x0-15), gespiegeld met spiegel.py (symmetrisch, licht linksboven)
 opzij.blk: volledig raster (naar links), 1 px naar rechts geschoven zodat het midden op x15-16 ligt
 Loopframes (1, 3, 5) = stilframe + de pootwissels hieronder (alleen voeten, plus 1 gebaar bij achter).
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
f4=np.roll(blk.lees(B+'opzij.blk'),1,axis=1)
# voor-lopen: linkervoorpoot 1 px opgetrokken
f1=f0.copy(); zet(f1,27,10,'26652'); zet(f1,28,10,'22222'); zet(f1,29,10,'.....')
zet(f1,8,11,'..'); zet(f1,9,11,'11')   # gebaar: linkeroor zakt 1 px
# achter-lopen: linkerachtervoet 1 px op, rechterachtervoet blijft staan
f3=f2.copy(); zet(f3,27,9,'65'); zet(f3,28,8,'2222'); zet(f3,29,8,'....')
zet(f3,10,11,'..'); zet(f3,11,11,'11')   # gebaar: linkeroor zakt 1 px
# opzij-lopen (raster al 1 px geschoven, dus x+1): voorpoot 1 px naar achteren
f5=f4.copy()
zet(f5,27,12,'.2652'); zet(f5,28,11,'.26652'); zet(f5,29,11,'.22222')
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
