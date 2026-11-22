# vel.py SPRITE.png UIT.png [VORIGE.png] [kopregel]: sprite 8x | (vorige 8x) | model op dezelfde schaal 8x (vlakgemiddelde per spritecel)
# / close-ups 12x (sprite | model met spriteraster): kop+mond, kaken / 1x op wit, licht, donker naast Pinsir 1x en het model 1x
import sys; sys.path.insert(0,'gereedschap')
from PIL import Image, ImageDraw; import numpy as np
MODEL='referenties/gemini_gekozen_r4B.png'; CEL=974/64; MX0,MY0=31,134; DY=13
def rgbp(path,bg=(255,255,255)):
    im=Image.open(path); o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
M=Image.open(MODEL).convert('RGB')
def model_op_schaal():
    box=(MX0,MY0-DY*CEL,MX0+64*CEL,MY0+(64-DY)*CEL)
    big=Image.new('RGB',(1200,1200),'white'); big.paste(M,(100,100))
    return big.crop(tuple(int(round(v+100)) for v in box)).resize((64,64),Image.BOX)
def model_crop(x0,y0,x1,y1,z):
    box=(MX0+x0*CEL,MY0+(y0-DY)*CEL,MX0+x1*CEL,MY0+(y1-DY)*CEL)
    big=Image.new('RGB',(1300,1300),'white'); big.paste(M,(100,100))
    return big.crop(tuple(int(round(v+100)) for v in box)).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
if __name__=='__main__':
    sp=rgbp(sys.argv[1]); m=model_op_schaal()
    pan=[sp]+([rgbp(sys.argv[3])] if len(sys.argv)>3 and sys.argv[3]!='-' else [])+[m]
    zones=[('kop en mond',10,24,30,38),('kaken',0,24,26,48),('poten en staart',14,40,64,62)]
    z=12; rows=[]
    for n,x0,y0,x1,y1 in zones:
        A=sp.crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); B=model_crop(x0,y0,x1,y1,z)
        r=Image.new('RGB',(A.width*2+8,A.height+16),'white'); r.paste(A,(0,16)); r.paste(B,(A.width+8,16))
        d=ImageDraw.Draw(r); d.text((2,2),n+' (sprite | model met spriteraster) x%d-%d y%d-%d'%(x0,x1,y0,y1),fill=(0,0,0))
        g=np.asarray(r).copy(); h0=16
        for off,col,al in ((0,(200,200,200),1.0),(A.width+8,(60,140,255),0.35)):
            for x in range(0,A.width+1,z):
                xx=min(off+x,g.shape[1]-1); g[h0:h0+A.height,xx]=(g[h0:h0+A.height,xx]*(1-al)+np.array(col)*al).astype('uint8')
            for y in range(0,A.height+1,z):
                yy=min(h0+y,g.shape[0]-1); g[yy,off:off+A.width]=(g[yy,off:off+A.width]*(1-al)+np.array(col)*al).astype('uint8')
        r=Image.fromarray(g); d=ImageDraw.Draw(r)
        rows.append(r)
    pin=Image.open('../../../../graphics/pokemon/pinsir/anim_front.png').convert('P')
    pin.save('/tmp/_pin.png',transparency=0)
    W=max(len(pan)*520,rows[0].width+rows[1].width+16,rows[2].width)
    H=530+max(rows[0].height,rows[1].height)+8+rows[2].height+8+90
    v=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(v)
    for i,p in enumerate(pan): v.paste(p.resize((512,512),Image.NEAREST),(i*520,14))
    d.text((2,0),sys.argv[4] if len(sys.argv)>4 else 'sprite 8x | model op dezelfde schaal 8x',fill=(0,0,0))
    y=532; x=0
    for r in rows[:2]: v.paste(r,(x,y)); x+=r.width+16
    y+=max(rows[0].height,rows[1].height)+8; v.paste(rows[2],(0,y)); y+=rows[2].height+8
    for i,bg in enumerate([(255,255,255),(232,232,216),(40,48,56)]):
        v.paste(rgbp(sys.argv[1],bg),(i*140,y+8)); v.paste(rgbp('/tmp/_pin.png',bg),(i*140+68,y+8))
    v.paste(m,(3*140,y+8)); d.text((2,y+76),'1x: sprite | Pinsir op wit, licht, donker; model op schaal',fill=(0,0,0))
    v.save(sys.argv[2]); print(sys.argv[2],v.size)
