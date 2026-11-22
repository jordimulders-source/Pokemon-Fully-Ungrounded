# vel r11 | r10B | model (natief, 4x) en diff-bewijs r11 t.o.v. r10B
import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
import numpy as np; from PIL import Image, ImageDraw
from bouw_r11 import ZONES, OY, OX
crop=(15,26,15+35,27+37); z=8
def op(c,bg,zz):
    b=Image.new('RGBA',c.size,bg+(255,)); b.alpha_composite(c); return b.convert('RGB').resize((c.width*zz,c.height*zz),Image.NEAREST)
r11=rgba(Image.open('sprite_r11/baltoy_r11.png')).crop(crop); r10=rgba(Image.open('sprite_r10/baltoy_r10B.png')).crop(crop)
mod=Image.open('gereedschap/natief.png').crop((12,10,91,86)).convert('RGBA')
W=r11.width*z; H=r11.height*z
vel=Image.new('RGB',(3*(W+30)+20,H+60+2*r11.height+20),(255,255,255)); d=ImageDraw.Draw(vel)
for i,(lab,c) in enumerate([('r11',r11),('r10B',r10)]):
    x=20+i*(W+30); d.text((x,10),lab,fill=(0,0,0)); vel.paste(op(c,(255,255,255),z),(x,30))
    vel.paste(op(c,(255,255,255),1),(x,H+40)); vel.paste(op(c,(255,255,255),2),(x+r11.width+6,H+40)); vel.paste(op(c,(48,48,56),2),(x+3*r11.width+16,H+40))
x=20+2*(W+30); d.text((x,10),'model (natief raster, 4x)',fill=(0,0,0)); vel.paste(mod.convert('RGB').resize((mod.width*4,mod.height*4),Image.NEAREST),(x,30))
vel.save('sprite_r11/vel.png')
# diff
a=np.array(Image.open('sprite_r11/baltoy_r11.png')); s=np.array(Image.open('sprite_r10/baltoy_r10B.png')); m=a!=s
toeg={(y+OY,x+OX):zn for zn,dd in ZONES.items() for y,r in dd.items() for x in r}
kl={'linkerarm':(30,120,255),'rechterarm':(0,170,90),'punt':(230,140,0),'keurderpunten':(200,0,200)}
arr=np.array(rgba(Image.open('sprite_r10/baltoy_r10B.png'))); per={}
for y,x in zip(*np.nonzero(m)):
    zn=toeg.get((y,x),'BUITEN'); per[zn]=per.get(zn,0)+1; arr[y,x]=kl.get(zn,(255,0,0))+(255,)
dv=op(Image.fromarray(arr,'RGBA').crop(crop),(255,255,255),z); ImageDraw.Draw(dv).text((6,4),'r11 vs r10B: blauw linkerarm, groen rechterarm, oranje punt, paars keurderpunten; rood = buiten zones (0)',fill=(0,0,0))
dv.save('sprite_r11/diff_bewijs.png')
# beschermd: hoofd+band (klassen y<=16), lijfvoor-/zijvlak patroon B (y20..28, x11..23 behalve keurderpunten), alles buiten de zones
hoofd=int(m[27:27+17,:].sum()); lijf=0
for y in range(20,29):
    for x in range(11,24):
        if m[y+OY,x+OX] and toeg.get((y+OY,x+OX)) not in ('keurderpunten','rechterarm'): lijf+=1
tekst=(f'gewijzigd t.o.v. r10B: {int(m.sum())} px; per zone: {per}\n'
       f'hoofd en band (klassen y 0..16): {hoofd} px gewijzigd\n'
       f'lijfvoor-/zijvlak patroon B (klassen y 20..28, x 11..23, zonder keurderpunten en de rechter armaanzet x23-24 rij 20-21): {lijf} px gewijzigd\n'
       f'buiten de zones: {per.get("BUITEN",0)} px; transparantie gelijk: {bool(((a==0)==(s==0)).all())}; zwarte omlijning gelijk: {bool(((a==10)==(s==10)).all())}\n'
       'keurderpunten (bewust, binnen opdracht 3): nekbalk y17-18 x11-14 (8 px), ribbe x20 rij 21 (1 px), zijvlak lijf rij 28 x21-22 (2 px; rij 28 hoort niet bij patroon B)\n')
open('sprite_r11/diff_bewijs.txt','w').write(tekst); print(tekst)
