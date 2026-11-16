import sys; sys.path.insert(0,'sprite_r1'); import numpy as np, colorsys; from PIL import Image, ImageDraw; import pal; from render import img
# palet r6: kleurfamilie A (hue 336 = A's rozebruin), stappen/verzadiging/hue-shift naar Gastly (A/B/C 312°: v .84/.74/.55,
# s .19/.22/.29; donkerste 9: hue -12°, v .22, s .28; lijn F bijna zwart). Kern iets lichter dan Gastly 9 ("minder zwart").
def hsv(h,s,v): return tuple(round(c*255) for c in colorsys.hsv_to_rgb(h/360,s,v))
R6=list(pal.A)
R6[6]=hsv(336,.19,.84); R6[5]=hsv(336,.22,.74); R6[4]=hsv(336,.29,.55); R6[3]=hsv(324,.34,.36); R6[2]=hsv(318,.32,.24); R6[1]=hsv(312,.38,.13)
L=lambda c: round(.299*c[0]+.587*c[1]+.114*c[2])
# r6b: zelfde kleurtoon en helderheid per index als r6, verzadiging omhoog (gas .35/.38/.42, kern .45, lijnen .45/.45)
def hsvL(h,s,Lt):
    best=None
    for v in np.arange(.05,1.0001,.0025):
        c=hsv(h,s,min(v,1)); d=abs(L(c)-Lt)
        if best is None or d<best[0]: best=(d,c)
    return best[1]
R6B=list(R6)
for i,(h,s) in {6:(336,.35),5:(336,.38),4:(336,.42),3:(324,.45),2:(318,.45),1:(312,.45)}.items(): R6B[i]=hsvL(h,s,L(R6[i]))
print('r6b palet',[(i,R6B[i],L(R6B[i]),round(colorsys.rgb_to_hsv(*[q/255 for q in R6B[i]])[1],2)) for i in range(1,7)])
print('r6 palet',[(i,R6[i],L(R6[i])) for i in range(1,11)])
V3=np.load('sprite_r5/V3_idx.npy').astype('uint8'); o=np.load('sprite_r6/r6_idx.npy').astype('uint8')
V2P=list(pal.A); V2P[1]=(50,18,42); V2P[2]=(82,34,66); V2P[3]=(108,52,86); V2P[4]=(156,94,120); V2P[5]=(204,148,160); V2P[6]=(234,194,188)
p=Image.fromarray(o,'P'); fl=[v for c in R6 for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save('sprite_r6/dustly_r6.png',transparency=0)
assert (np.asarray(Image.open('sprite_r6/dustly_r6.png'))==o).all(); img(o,R6,8).save('sprite_r6/dustly_r6_8x.png')
p=Image.fromarray(o,'P'); fl=[v for c in R6B for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save('sprite_r6/dustly_r6b.png',transparency=0)
assert (np.asarray(Image.open('sprite_r6/dustly_r6b.png'))==o).all(); img(o,R6B,8).save('sprite_r6/dustly_r6b_8x.png')
G=Image.open('../../../../graphics/pokemon/gastly/anim_front.png'); ga=np.asarray(G)[:64]
gr=np.asarray(G.convert('RGBA'))[:64].copy(); gr[ga==0,3]=0; GI=Image.fromarray(gr)
def gimg(s,bgc):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(GI); return b.resize((64*s,64*s),Image.NEAREST)
LICHT,DONKER=(248,248,240),(40,40,48)
m=Image.open('gemini/r6_a.png').convert('RGB').crop((150,150,880,880)).resize((512,512),Image.LANCZOS)
cells=[(gimg(8,LICHT),'Gastly Gen 3'),(m,'model r6_a'),(img(V3,V2P,8,LICHT),'V3'),(img(o,R6,8,LICHT),'r6'),(img(o,R6B,8,LICHT),'r6b')]
W=5*512+6*16; out=Image.new('RGB',(W,24+512+24+150),(255,255,255)); d=ImageDraw.Draw(out)
for i,(c,n) in enumerate(cells): out.paste(c.convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),n,fill=(0,0,0))
y=24+512+24; x=16
for P in (R6,R6B):
    for bgc in (LICHT,DONKER):
        for s in (1,2):
            c=img(o,P,s,bgc).convert('RGB'); out.paste(c,(x,y)); x+=c.width+8
        x+=24
d.text((x,y-14),'1x: r6 | r6b | Gastly',fill=(0,0,0))
for bgc in (LICHT,DONKER):
    out.paste(img(o,R6,1,bgc).convert('RGB'),(x,y)); out.paste(img(o,R6B,1,bgc).convert('RGB'),(x+66,y)); out.paste(gimg(1,bgc).convert('RGB'),(x+132,y)); x+=220
out.save('sprite_r6/vel.png')
# studie.png: Gastly 12x + palet met L/h/s
st=Image.new('RGB',(64*12+340,64*12),(255,255,255)); st.paste(gimg(12,LICHT).convert('RGB'),(0,0)); d=ImageDraw.Draw(st)
pp=G.getpalette()
for i in range(16):
    c=tuple(pp[3*i:3*i+3]); h,s,v=colorsys.rgb_to_hsv(*[q/255 for q in c]); n=int((ga==i).sum())
    d.rectangle([780,10+i*44,820,46+i*44],fill=c,outline=(0,0,0)); d.text((828,20+i*44),f'{i:2d} L{L(c)} h{round(h*360)} s{s:.2f} n{n}',fill=(0,0,0))
st.save('sprite_r6/studie.png'); print('ok')
