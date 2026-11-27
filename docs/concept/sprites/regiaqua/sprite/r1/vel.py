# vel.png: rij 1 sprite 8x | kale reductie 8x | model op dezelfde schaal; rij 2: 1x op licht/donker (+2x);
# rij 3: sprite 8x naast Regice en Registeel (anim_front_gba frame 1 + normal_gba.pal).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image, ImageDraw; import pal, kaal as kl
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(os.path.join(D,'../../../../../..'))
def laad(p):
    im=Image.open(p); im.save('/tmp/_v.png',transparency=0); return Image.open('/tmp/_v.png').convert('RGBA')
def op(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def main(spr='regiaqua_r1.png',uit='vel.png'):
    sp=laad(os.path.join(D,spr)); ka=laad(os.path.join(D,'kaal.png'))
    M=Image.open(os.path.join(D,'../../gemini/r1.png')).convert('RGB')
    cell=10.24; ph=9.75
    def m(xs,ys):  # spritecoord -> modelpx
        return ph+(kl.X0+(xs-kl.OX)/kl.s)*cell, ph-0.05+(kl.Y0+(ys-kl.OY)/kl.s)*cell
    x0,y0=m(0,0); x1,y1=m(64,64)
    mod=M.crop((int(x0),int(y0),int(x1),int(y1))).resize((512,512),Image.LANCZOS)
    BG=(255,255,255); G=16
    W=3*512+4*G; V=Image.new("RGB",(W,512*2+200+4*G),(200,200,200)); dr=ImageDraw.Draw(V)
    for i,im in enumerate([op(sp,BG).resize((512,512),0),op(ka,BG).resize((512,512),0),mod]):
        V.paste(im,(G+i*(512+G),G))
    y=512+2*G; x=G
    for bg in [(255,255,255),(232,240,208),(144,160,176),(40,40,56),(0,0,0)]:
        V.paste(op(sp,bg),(x,y)); V.paste(op(sp,bg).resize((128,128),0),(x,y+72)); x+=148
    sm=mod.resize((64,64),Image.LANCZOS); V.paste(sm,(x,y)); V.paste(sm.resize((128,128),0),(x,y+72))
    y+=400-200+G
    def gba(n):
        im=Image.open(os.path.join(R,'graphics/pokemon',n,'anim_front_gba.png')).crop((0,0,64,64))
        L=open(os.path.join(R,'graphics/pokemon',n,'normal_gba.pal')).read().split()[3:]
        p=[int(v) for v in L]; im=im.convert('P'); im.putpalette(p+[0]*(768-len(p)))
        a=np.array(im); c=np.array(p,'uint8').reshape(-1,3)[a]; c[a==0]=BG
        return Image.fromarray(c)
    V.paste(op(sp,BG).resize((512,512),0),(G,y))
    V.paste(gba('regice').resize((512,512),0),(2*G+512,y)); V.paste(gba('registeel').resize((512,512),0),(3*G+1024,y))
    V.save(os.path.join(D,uit))
if __name__=='__main__': main(*sys.argv[1:])
