# vel.png: rij 1 r2 8x | r1 8x | model; rij 2: close-ups 16x van Saturnus en asteroide (r2 | r1 | natief model);
# rij 3: 1x/2x op licht en donker + model 1x; rij 4: r2 8x naast Regiaqua af, Regirock, Registeel (gba).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from PIL import Image; import pal, gemeen as g, kaal as kl
import vel_basis as vb
D=g.D
def main():
    sp=vb.laad(os.path.join(D,'regicosmo_r2.png')); r1=vb.laad(os.path.join(D,'../r1/regicosmo_r1.png'))
    mod=vb.modelvak().resize((512,512),Image.LANCZOS)
    BG=(255,255,255); G=16
    nat=Image.open(os.path.join(D,'natief.png')).convert('RGB')
    def nmod(x0,y0,x1,y1,Z):
        nx0=kl.X0+(x0-kl.OX)/kl.s; ny0=kl.Y0+(y0-kl.OY)/kl.s; nx1=kl.X0+(x1-kl.OX)/kl.s; ny1=kl.Y0+(y1-kl.OY)/kl.s
        return nat.resize((nat.width*8,nat.height*8),0).crop((int(nx0*8),int(ny0*8),int(nx1*8),int(ny1*8))).resize(((x1-x0)*Z,(y1-y0)*Z),0)
    rows=[]
    V=Image.new('RGB',(3*512+4*G,512*2+3*(16*16)+200+8*G),(200,200,200))
    for i,im in enumerate([vb.op(sp,BG).resize((512,512),0),vb.op(r1,BG).resize((512,512),0),mod]): V.paste(im,(G+i*(512+G),G))
    y=512+2*G; Z=16
    for (x0,y0,x1,y1) in [(46,23,64,36),(0,38,13,53)]:
        x=G
        for im in [vb.op(sp,BG).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0),vb.op(r1,BG).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0),nmod(x0,y0,x1,y1,Z)]:
            V.paste(im,(x,y)); x+=im.width+G
        y+=(y1-y0)*Z+G
    x=G
    for bg in [(255,255,255),(232,240,208),(144,160,176),(40,40,56),(0,0,0)]:
        V.paste(vb.op(sp,bg),(x,y)); V.paste(vb.op(sp,bg).resize((128,128),0),(x,y+72)); x+=148
    sm=mod.resize((64,64),Image.LANCZOS); V.paste(sm,(x,y)); V.paste(sm.resize((128,128),0),(x,y+72))
    y+=200+G
    ra=vb.op(vb.laad(os.path.join(D,'../../../regiaqua/af/regiaqua.png')),BG)
    W=Image.new('RGB',(4*512+5*G,512),(200,200,200))
    for i,im in enumerate([vb.op(sp,BG),ra,vb.gba('regirock',BG),vb.gba('registeel',BG)]): W.paste(im.resize((512,512),0),(G+i*(512+G),0))
    V2=Image.new('RGB',(max(V.width,W.width),y+512+G),(200,200,200)); V2.paste(V.crop((0,0,V.width,y)),(0,0)); V2.paste(W,(0,y))
    V2.save(os.path.join(D,'vel.png'))
if __name__=='__main__': main()
