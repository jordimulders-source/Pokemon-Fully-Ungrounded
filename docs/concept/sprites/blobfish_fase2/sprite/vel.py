# vel_rN.png: sprite 8x | model verkleind (zelfde schaal, LANCZOS) 8x | kale reductie 8x ; eronder 1x en 2x op licht en donker
import sys; from PIL import Image, ImageDraw
N=sys.argv[1] if len(sys.argv)>1 else 'r1'
def rgba(f):
    return Image.open(f).convert('RGBA')
spr=rgba(N+'.png'); VORIG=sys.argv[2] if len(sys.argv)>2 else 'kaal'; kaal=rgba(VORIG+'.png')
m=Image.open('model_natief.png').convert('RGBA'); bb=m.getbbox(); mc=m.crop(bb)
w=round(mc.width/1.5); h=round(mc.height/1.5); mv=mc.resize((w,h),Image.LANCZOS)
mod=Image.new('RGBA',(64,64),(0,0,0,0)); mod.alpha_composite(mv,(1,17))
def op(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST)
W=3*532+40; v=Image.new('RGB',(max(W,1800),512+200),(255,255,255)); d=ImageDraw.Draw(v)
for k,(im,t) in enumerate([(spr,N),(kaal,VORIG),(mod,'model verkleind')]):
    v.paste(op(im,(255,255,255,255),8),(k*532,0)); d.text((k*532+4,4),t,fill=(0,0,0))
x=10
for bg in [(255,255,255,255),(232,232,224,255),(40,40,56,255)]:
    for s in (1,2):
        t=op(spr,bg,s); v.paste(t,(x,530)); x+=t.width+10
    t=op(kaal,bg,2); v.paste(t,(x,530)); x+=t.width+10
    t=op(mod,bg,2); v.paste(t,(x,530)); x+=t.width+30
v.save('vel_'+N+'.png')
