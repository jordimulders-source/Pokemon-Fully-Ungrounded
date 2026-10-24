"""Exporteert anim_front.png (64x128, 2 frames), normal.pal, onderlaag.png, compare.png en zelfcheck/."""
import sys, os, shutil
sys.path.insert(0,'/home/user/projectgrounded/docs/concept/sprites/olinguito/herbouw_linoone/bron')
from render import load,to_img,zoom,pal
from PIL import Image, ImageDraw
D='/home/user/projectgrounded/docs/concept/sprites/olinguito/'
H=D+'herbouw_linoone/'
SHIFT=(4,3)   # Linoone-coordinaten -> gecentreerd in 64x64
f1=to_img(load(H+'bron/raster_f1.txt'),SHIFT); f2=to_img(load(H+'bron/raster_f2.txt'),SHIFT)
A=Image.new('P',(64,128),0); A.putpalette(f1.getpalette())
A.paste(f1,(0,0)); A.paste(f2,(0,64))
A.save(H+'anim_front.png',transparency=0)
shutil.copy(D+'ronde23/normal.pal',H+'normal.pal')
lin=Image.open(D+'referenties/galar_linoone_front.png')
r23=Image.open(D+'ronde23/anim_front.png').crop((0,0,64,64))
pooch=Image.open('/home/user/projectgrounded/graphics/pokemon/poochyena/anim_front.png').crop((0,0,64,64))
BG=(200,200,220)
def lab(img,t):
    d=ImageDraw.Draw(img); d.text((4,2),t,fill=(0,0,0))
# onderlaag: basis | overtekening (basis vaag + resultaat halfdoorzichtig, zelfde coordinaten) | resultaat
z=6
base=zoom(lin,z,BG)
ov=Image.new('RGBA',(64*z,64*z),(235,235,235,255))
g=lin.convert('RGBA'); g=zoom(lin,z,(235,235,235)); g=Image.blend(Image.new('RGBA',g.size,(235,235,235,255)),g,0.45)
ov.paste(g,(0,0))
res_lin=to_img(load(H+'bron/raster_f1.txt'))  # in Linoone-coordinaten
r=zoom(res_lin,z,BG).convert('RGBA'); px=r.load(); m=res_lin.load()
r2=Image.new('RGBA',r.size,(0,0,0,0)); p2=r2.load()
for y in range(64*z):
    for x in range(64*z):
        if m[x//z,y//z]!=0:
            c=px[x,y]; p2[x,y]=(c[0],c[1],c[2],150)
ov=Image.alpha_composite(ov,r2)
res=zoom(res_lin,z,BG)
O=Image.new('RGBA',(64*z*3+20,64*z),(255,255,255,255))
O.paste(base,(0,0)); O.paste(ov,(64*z+10,0)); O.paste(res,(2*64*z+20,0))
O=O.crop((0,15*z,O.size[0],56*z)); lab(O,'basis Galar-Linoone | overtekening (zelfde coordinaten) | resultaat')
O.save(H+'onderlaag.png')
# compare: resultaat | ronde 23 | Galar-Linoone, 1x en 3x (+ frame 2)
items=[(f1,'nieuw f1'),(f2,'nieuw f2'),(r23,'ronde 23'),(lin,'Galar-Linoone')]
W=Image.new('RGBA',(len(items)*196+10,64+20+192+10),(255,255,255,255))
for i,(im,t) in enumerate(items):
    W.paste(zoom(im,1,BG),(i*70+4,16)); W.paste(zoom(im,3,BG),(i*196+4,90))
    ImageDraw.Draw(W).text((i*196+4,80),t,fill=(0,0,0))
ImageDraw.Draw(W).text((4,2),'1x: nieuw f1, f2, ronde 23, Galar-Linoone',fill=(0,0,0))
W.save(H+'compare.png')
# zelfcheck: uitsneden 8x (frame 1, in Linoone-coordinaten)
os.makedirs(H+'zelfcheck',exist_ok=True)
crops={'kop':(0,19,25,40),'voorpoot_nabij':(1,33,23,53),'voorpoot_ver':(13,33,27,50),
       'achterpoot_ver':(19,33,34,48),'achterpoot_nabij':(28,28,43,50),'staart':(38,25,56,50)}
for n,b in crops.items():
    c=res_lin.crop(b); zz=zoom(c,8,BG); d=ImageDraw.Draw(zz)
    zz.save(H+'zelfcheck/%s_8x.png'%n)
W=Image.new('RGBA',(4*68,70),(255,255,255,255))
for i,im in enumerate((f1,lin,r23,pooch)): W.paste(zoom(im,1,BG),(i*68,3))
W.save(H+'zelfcheck/naast_1x.png')
W=Image.new('RGBA',(4*196,196),(255,255,255,255))
for i,im in enumerate((f1,lin,r23,pooch)): W.paste(zoom(im,3,BG),(i*196,2))
W.save(H+'zelfcheck/naast_3x.png')
print('ok', Image.open(H+'anim_front.png').info)
