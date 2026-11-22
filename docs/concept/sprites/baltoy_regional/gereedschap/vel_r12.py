# vel r12 | r11 | r10B en diff-bewijs r12 t.o.v. r11
import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
import numpy as np; from PIL import Image, ImageDraw
crop=(15,26,15+35,27+37); z=8
def op(c,bg,zz):
    b=Image.new('RGBA',c.size,bg+(255,)); b.alpha_composite(c); return b.convert('RGB').resize((c.width*zz,c.height*zz),Image.NEAREST)
L=[('r12','sprite_r12/baltoy_r12.png'),('r11','sprite_r11/baltoy_r11.png'),('r10B','sprite_r10/baltoy_r10B.png')]
cs=[rgba(Image.open(p)).crop(crop) for _,p in L]; w,h=cs[0].size
vel=Image.new('RGB',(3*(w*z+30)+20,h*z+60+2*h+20),(255,255,255)); d=ImageDraw.Draw(vel)
for i,((lab,_),c) in enumerate(zip(L,cs)):
    x=20+i*(w*z+30); d.text((x,10),lab,fill=(0,0,0)); vel.paste(op(c,(255,255,255),z),(x,30))
    vel.paste(op(c,(255,255,255),1),(x,h*z+40)); vel.paste(op(c,(255,255,255),2),(x+w+6,h*z+40)); vel.paste(op(c,(48,48,56),2),(x+3*w+16,h*z+40))
vel.save('sprite_r12/vel.png')
a=np.array(Image.open('sprite_r12/baltoy_r12.png')); s=np.array(Image.open('sprite_r11/baltoy_r11.png')); m=a!=s
arr=np.array(rgba(Image.open('sprite_r11/baltoy_r11.png'))); arr[m]=(230,30,30,255)
dv=op(Image.fromarray(arr,'RGBA').crop(crop),(255,255,255),z); ImageDraw.Draw(dv).text((6,4),'r12 vs r11: rood = gewijzigd',fill=(0,0,0)); dv.save('sprite_r12/diff_bewijs.png')
ys,xs=np.nonzero(m); pts=sorted((int(y)-27,int(x)-15) for y,x in zip(ys,xs))
st=[p for p in pts if p[0]>=30]; mo=[p for p in pts if p[0]<30]
t=(f'r12 t.o.v. r11: {int(m.sum())} px gewijzigd\nstekel (klassen y30..34, x15..19): {len(st)} px {st}\nmond (klassen y15): {len(mo)} px {mo}\n'
   f'overig: {int(m.sum())-len(st)-len(mo)} px; transparantie gelijk: {bool(((a==0)==(s==0)).all())}; zwart gelijk: {bool(((a==10)==(s==10)).all())}\n')
open('sprite_r12/diff_bewijs.txt','w').write(t); print(t)
