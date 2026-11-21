# vel4.py: r4 8x | r3 8x | model 8x | echte Swablu 8x / kop+snavel 12x: r4 | model | echte Swablu-kop / 1x op 4 achtergronden + model 1x
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); import gemeen as G
def rgb_from(im,bg=(255,255,255)):
    im=im.convert('P') if im.mode!='P' else im
    o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
r4=Image.open('sprite_r4/swablu_r4.png'); r3=Image.open('sprite_r3/swablu_r3.png')
sw=Image.open('../../../../graphics/pokemon/swablu/anim_front.png')
s4=rgb_from(r4); s3=rgb_from(r3); m=G.model_op_schaal(); g=rgb_from(sw)
top=[x.resize((512,512),Image.NEAREST) for x in (s4,s3,m,g)]
M=Image.open(G.MODEL).convert('RGB')
def mcrop(x0,y0,x1,y1,z):
    u0=(x0-G.X0)/G.S+G.U0; u1=(x1-G.X0)/G.S+G.U0; v0=(y0-G.Y0)/G.S+G.V0; v1=(y1-G.Y0)/G.S+G.V0
    fx=lambda u:G.PHX+0.5+G.PX*u; fy=lambda v:G.PHY+0.5+G.PY*v
    return M.crop((int(fx(u0)),int(fy(v0)),int(fx(u1)),int(fy(v1)))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
z=12; kop=(17,22,37,39)
c1=s4.crop(kop).resize(((kop[2]-kop[0])*z,(kop[3]-kop[1])*z),Image.NEAREST)
c2=mcrop(*kop,z)
c3=g.crop((16,24,36,41)).resize((20*z,17*z),Image.NEAREST)
W=4*520; H=520+c1.height+16+80
v=Image.new('RGB',(W,H),'white')
for i,p in enumerate(top): v.paste(p,(i*520,0))
x=0
for p in (c1,c2,c3): v.paste(p,(x,520)); x+=p.width+16
y=520+c1.height+16
for i,bg in enumerate([(255,255,255),(248,248,232),(40,48,56),(24,24,24)]): v.paste(rgb_from(r4,bg),(i*72,y))
v.paste(m,(4*72,y)); v.save('sprite_r4/vel.png'); print(v.size)
