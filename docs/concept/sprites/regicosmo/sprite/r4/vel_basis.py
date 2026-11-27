# vel.png: rij 1 sprite 8x | kale reductie 8x | model op dezelfde schaal; rij 2: 1x en 2x op licht/donker + model 1x;
# rij 3: sprite 8x naast Regiaqua (af), Regirock en Registeel (anim_front_gba frame 1 + normal_gba.pal).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image, ImageDraw; import pal, gemeen as g, kaal as kl
D=g.D; R=os.path.abspath(os.path.join(D,'../../../../../..'))
def laad(p):   # P-png met index 0 transparant -> RGBA (convert('RGBA') negeert de transparantie)
    im=Image.open(p); a=np.array(im); P=np.array(im.getpalette()[:768],'uint8').reshape(-1,3)
    return Image.fromarray(np.dstack([P[a],np.where(a==0,0,255).astype('uint8')]),'RGBA')
def op(im,bg):
    b=Image.new('RGBA',im.size,bg+(255,)); b.alpha_composite(im); return b.convert('RGB')
def modelvak():   # het 64x64-vak van de sprite, teruggerekend naar modelpixels
    px,phx,py,phy=np.load(os.path.join(D,'natief_rooster.npy'))
    M=Image.open(os.path.join(D,'../../model.png')).convert('RGB')
    def m(xs,ys): return phx+0.5+(kl.X0+(xs-kl.OX)/kl.s)*px, phy+0.5+(kl.Y0+(ys-kl.OY)/kl.s)*py
    x0,y0=m(0,0); x1,y1=m(64,64)
    W=Image.new('RGB',(int(x1-x0)+2,int(y1-y0)+2),'white'); W.paste(M,(-int(x0),-int(y0)))
    return W
def gba(n,BG):
    im=Image.open(os.path.join(R,'graphics/pokemon',n,'anim_front_gba.png')).crop((0,0,64,64))
    L=open(os.path.join(R,'graphics/pokemon',n,'normal_gba.pal')).read().split()[3:]
    p=[int(v) for v in L]; a=np.array(im); c=np.array(p,'uint8').reshape(-1,3)[a]; c[a==0]=BG
    return Image.fromarray(c)
def main(spr='regicosmo_r1.png',uit='vel.png'):
    sp=laad(os.path.join(D,spr)); ka=laad(os.path.join(D,'kaal.png'))
    mod=modelvak().resize((512,512),Image.LANCZOS)
    BG=(255,255,255); G=16
    V=Image.new("RGB",(4*512+5*G,3*512+4*G-250),(200,200,200))
    for i,im in enumerate([op(sp,BG).resize((512,512),0),op(ka,BG).resize((512,512),0),mod]):
        V.paste(im,(G+i*(512+G),G))
    y=512+2*G; x=G
    for bg in [(255,255,255),(232,240,208),(144,160,176),(40,40,56),(0,0,0)]:
        V.paste(op(sp,bg),(x,y)); V.paste(op(sp,bg).resize((128,128),0),(x,y+72)); x+=148
    sm=mod.resize((64,64),Image.LANCZOS); V.paste(sm,(x,y)); V.paste(sm.resize((128,128),0),(x,y+72))
    y+=200+G
    ra=op(laad(os.path.join(D,'../../../regiaqua/af/regiaqua.png')),BG)
    for i,im in enumerate([op(sp,BG),ra,gba('regirock',BG),gba('registeel',BG)]):
        V.paste(im.resize((512,512),0),(G+i*(512+G),y))
    V.save(os.path.join(D,uit))
if __name__=='__main__': main(*sys.argv[1:])
