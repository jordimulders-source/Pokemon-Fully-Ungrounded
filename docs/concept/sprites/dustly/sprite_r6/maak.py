import sys; sys.path.insert(0,'sprite_r1'); import numpy as np, colorsys; from PIL import Image, ImageDraw; import pal; from render import img
# palet r6: kleurfamilie A (hue 336 = A's rozebruin), stappen/verzadiging/hue-shift naar Gastly (A/B/C 312°: v .84/.74/.55,
# s .19/.22/.29; donkerste 9: hue -12°, v .22, s .28; lijn F bijna zwart). Kern iets lichter dan Gastly 9 ("minder zwart").
def hsv(h,s,v): return tuple(round(c*255) for c in colorsys.hsv_to_rgb(h/360,s,v))
R6=list(pal.A)
R6[6]=hsv(336,.19,.84); R6[5]=hsv(336,.22,.74); R6[4]=hsv(336,.29,.55); R6[3]=hsv(324,.34,.36); R6[2]=hsv(318,.32,.24); R6[1]=hsv(312,.38,.13)
L=lambda c: round(.299*c[0]+.587*c[1]+.114*c[2])
print('r6 palet',[(i,R6[i],L(R6[i])) for i in range(1,11)])
V3=np.load('sprite_r5/V3_idx.npy').astype('uint8'); o=np.load('sprite_r6/r6_idx.npy').astype('uint8')
V2P=list(pal.A); V2P[1]=(50,18,42); V2P[2]=(82,34,66); V2P[3]=(108,52,86); V2P[4]=(156,94,120); V2P[5]=(204,148,160); V2P[6]=(234,194,188)
p=Image.fromarray(o,'P'); fl=[v for c in R6 for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save('sprite_r6/dustly_r6.png',transparency=0)
assert (np.asarray(Image.open('sprite_r6/dustly_r6.png'))==o).all(); img(o,R6,8).save('sprite_r6/dustly_r6_8x.png')
G=Image.open('../../../../graphics/pokemon/gastly/anim_front.png'); ga=np.asarray(G)[:64]
gr=np.asarray(G.convert('RGBA'))[:64].copy(); gr[ga==0,3]=0; GI=Image.fromarray(gr)
def gimg(s,bgc):
    b=Image.new('RGBA',(64,64),bgc+(255,)); b.alpha_composite(GI); return b.resize((64*s,64*s),Image.NEAREST)
LICHT,DONKER=(248,248,240),(40,40,48)
m=Image.open('gemini/r6_a.png').convert('RGB').crop((150,150,880,880)).resize((512,512),Image.LANCZOS)
cells=[(gimg(8,LICHT),'Gastly Gen 3'),(m,'model r6_a'),(img(V3,V2P,8,LICHT),'V3'),(img(o,R6,8,LICHT),'r6')]
W=4*512+5*16; out=Image.new('RGB',(W,24+512+24+150),(255,255,255)); d=ImageDraw.Draw(out)
for i,(c,n) in enumerate(cells): out.paste(c.convert('RGB'),(16+i*528,24)); d.text((16+i*528,6),n,fill=(0,0,0))
y=24+512+24; x=16
for bgc in (LICHT,DONKER):
    for s in (1,2):
        c=img(o,R6,s,bgc).convert('RGB'); out.paste(c,(x,y)); x+=c.width+8
    x+=24
d.text((x,y-14),'r6 naast Gastly 1x:',fill=(0,0,0))
for bgc in (LICHT,DONKER):
    out.paste(img(o,R6,1,bgc).convert('RGB'),(x,y)); out.paste(gimg(1,bgc).convert('RGB'),(x+66,y)); x+=150
out.save('sprite_r6/vel.png')
# studie.png: Gastly 12x + palet met L/h/s
st=Image.new('RGB',(64*12+340,64*12),(255,255,255)); st.paste(gimg(12,LICHT).convert('RGB'),(0,0)); d=ImageDraw.Draw(st)
pp=G.getpalette()
for i in range(16):
    c=tuple(pp[3*i:3*i+3]); h,s,v=colorsys.rgb_to_hsv(*[q/255 for q in c]); n=int((ga==i).sum())
    d.rectangle([780,10+i*44,820,46+i*44],fill=c,outline=(0,0,0)); d.text((828,20+i*44),f'{i:2d} L{L(c)} h{round(h*360)} s{s:.2f} n{n}',fill=(0,0,0))
st.save('sprite_r6/studie.png'); print('ok')
