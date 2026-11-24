# keuze.png: r15 | model (zelfde stuk, natief raster op 2x van de sprite = zelfde schaal) | r13, ingezoomd 10x; eronder volledig 1x/2x
import sys; sys.path.insert(0,'gereedschap'); from r4lib import rgba
from PIL import Image, ImageDraw
def op(c,bg,zz):
    b=Image.new('RGBA',c.size,bg+(255,)); b.alpha_composite(c); return b.convert('RGB').resize((c.width*zz,c.height*zz),Image.NEAREST)
z=10; sc=(24,50,42,64)          # sprite-uitsnede png x24..41, y50..63
nat=Image.open('gereedschap/natief.png').convert('RGBA')
nc=(2*sc[0]-15,2*sc[1]-41,2*sc[2]-15,2*sc[3]-41)   # zelfde stuk in het model (x55<->35, y71<->56)
W=(sc[2]-sc[0])*z; H=(sc[3]-sc[1])*z
r15=rgba(Image.open('sprite_r15/baltoy_r15.png')); r13=rgba(Image.open('sprite_r13/baltoy_r13.png'))
full=(15,26,50,64); fw,fh=full[2]-full[0],full[3]-full[1]
vel=Image.new('RGB',(3*(W+30)+20,H+60+2*fh+30),(255,255,255)); d=ImageDraw.Draw(vel)
items=[('r15',op(r15.crop(sc),(255,255,255),z)),('model (natief, zelfde stuk/schaal)',op(nat.crop(nc),(255,255,255),z//2)),('r13',op(r13.crop(sc),(255,255,255),z))]
for i,(lab,img) in enumerate(items):
    x=20+i*(W+30); d.text((x,10),lab,fill=(0,0,0)); vel.paste(img,(x,30))
for i,im in enumerate([r15,None,r13]):
    if im is None: continue
    x=20+i*(W+30); f=im.crop(full); y=H+45
    vel.paste(op(f,(255,255,255),1),(x,y)); vel.paste(op(f,(255,255,255),2),(x+fw+6,y)); vel.paste(op(f,(48,48,56),1),(x+3*fw+16,y)); vel.paste(op(f,(48,48,56),2),(x+4*fw+22,y))
m=nat.crop((12,10,91,86)); vel.paste(op(m,(255,255,255),1),(20+(W+30),H+45))
vel.save('sprite_r15/keuze.png')
