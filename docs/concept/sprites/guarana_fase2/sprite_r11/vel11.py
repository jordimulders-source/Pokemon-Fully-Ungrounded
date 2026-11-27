# vel11: voor_jordi_r11_8x.png (r11 | r10a, 8x, wit), afstand.png (r11 en r10a op 1x en 2x), closeups.png (per omcirkelde plek r10a | r11 op 12x)
from PIL import Image, ImageDraw
def w(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a); return B.convert('RGB')
A=w('sprite_r11/guarana2_r11.png'); B=w('sprite_r10/guarana2_r10a.png')
T=Image.new('RGB',(1040,512),'white'); T.paste(A.resize((512,512),0),(0,0)); T.paste(B.resize((512,512),0),(528,0)); T.save('sprite_r11/voor_jordi_r11_8x.png')
T=Image.new('RGB',(2*72+2*136+8,136),'white'); x=4
for im,s in ((A,1),(B,1),(A,2),(B,2)): T.paste(im.resize((64*s,64*s),0),(x,4)); x+=64*s+8
T.save('sprite_r11/afstand.png')
PLEK=[('1+2 midden: half dicht oog + gat',(21,33,13,21)),('3 midden: oog M2',(17,28,17,25)),('4 links: oog L1',(4,15,23,32)),
      ('5 links: oog L5',(12,22,30,40)),('6 rechts: oog boven',(42,54,19,28)),('7 rechts: meest rechtse oog',(50,60,20,28)),('8 rechts: onderpunt',(42,54,32,42))]
Z=12; rows=[]
for n,(x0,x1,y0,y1) in PLEK:
    a=B.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0); b=A.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),0)
    r=Image.new('RGB',(a.width*2+30,a.height+18),'white'); ImageDraw.Draw(r).text((2,2),n+'  (r10a | r11)',fill='black'); r.paste(a,(0,18)); r.paste(b,(a.width+30,18)); rows.append(r)
WW=max(r.width for r in rows); T=Image.new('RGB',(WW*2+20,sum(r.height+10 for r in rows[::2])),'white'); y=0
for i in range(0,len(rows),2):
    T.paste(rows[i],(0,y)); 
    if i+1<len(rows): T.paste(rows[i+1],(WW+20,y))
    y+=max(r.height for r in rows[i:i+2])+10
T.save('sprite_r11/closeups.png')
