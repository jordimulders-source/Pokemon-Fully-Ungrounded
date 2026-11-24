# keuze.png (A | B | C op 8x + 1x/2x op licht en donker) en diff-bewijs t.o.v. r8
import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
import numpy as np; from PIL import Image, ImageDraw
r8=np.array(Image.open('sprite_r8/baltoy_r8.png'))
crop=(15+0,27-1,15+35,27+37); W,H=crop[2]-crop[0],crop[3]-crop[1]; z=8
L='ABC'; ims=[rgba(Image.open(f'sprite_r9/baltoy_r9{k}.png')).crop(crop) for k in L]
def op(c,bg,zz):
    b=Image.new('RGBA',c.size,bg+(255,)); b.alpha_composite(c); return b.convert('RGB').resize((c.width*zz,c.height*zz),Image.NEAREST)
kol=W*z+24; vel=Image.new('RGB',(24+3*kol, 40+H*z+20+H*2+30),(255,255,255)); d=ImageDraw.Draw(vel)
for i,(k,c) in enumerate(zip(L,ims)):
    x=24+i*kol; d.text((x,12),{'A':'A  handen: kero + staf, gordel','B':'B  getrapte gordel + banen','C':'C  chakana-paneel'}[k],fill=(0,0,0))
    vel.paste(op(c,(255,255,255),z),(x,36)); yy=36+H*z+16
    for j,bg in enumerate([(255,255,255),(48,48,56)]):
        bx=x+j*(3*W+20)
        vel.paste(op(c,bg,1),(bx,yy)); vel.paste(op(c,bg,2),(bx+W+4,yy))
vel.save('sprite_r9/keuze.png')
# diff-bewijs: per variant de gewijzigde pixels in rood over r8 (8x), plus bounding box en telling
reg=[]; kol=W*z+24; dv=Image.new('RGB',(24+3*kol,40+H*z),(255,255,255)); dd=ImageDraw.Draw(dv)
for i,k in enumerate(L):
    a=np.array(Image.open(f'sprite_r9/baltoy_r9{k}.png')); m=a!=r8; ys,xs=np.nonzero(m)
    reg.append(f'{k}: {m.sum()} pixels gewijzigd, png y {ys.min()}..{ys.max()}, x {xs.min()}..{xs.max()} (zone lijfvoorvlak y 47..55, x 27..34); buiten de zone: {int(m.sum()-m[47:56,27:35].sum())}; transparantie gelijk: {bool(((a==0)==(r8==0)).all())}')
    base=rgba(Image.open('sprite_r8/baltoy_r8.png')); arr=np.array(base); arr[m]=(230,30,30,255)
    c=Image.fromarray(arr,'RGBA').crop(crop); x=24+i*kol; dv.paste(op(c,(255,255,255),z),(x,36)); dd.text((x,12),f'{k}: gewijzigd t.o.v. r8 (rood) = {m.sum()} px',fill=(0,0,0))
    dd.rectangle((x+(27-crop[0])*z-1,36+(47-crop[1])*z-1,x+(35-crop[0])*z,36+(56-crop[1])*z),outline=(0,90,255),width=2)
dv.save('sprite_r9/diff_bewijs.png'); open('sprite_r9/diff_bewijs.txt','w').write('\n'.join(reg)+'\nblauw kader = zone lijfvoorvlak (klassen x 12..19, y 20..28). Gecontroleerd met gereedschap/vel_r9.py.\n'); print('\n'.join(reg))
