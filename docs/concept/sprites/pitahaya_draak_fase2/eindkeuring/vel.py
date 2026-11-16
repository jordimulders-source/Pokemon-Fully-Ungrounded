# vel.py -> vel.png: r9A op 8x met omcirkelde probleemzones, het model op dezelfde maat, 2 Gen 3-referenties (Salamence, Lairon),
# en de keurderproef (proef_alles.png, alleen om de reparatielijst te toetsen) op 8x; onderaan alles op 1x en 2x.
from PIL import Image, ImageDraw
B='/home/user/Pokemon-Fully-Ungrounded/'; P=B+'docs/concept/sprites/pitahaya_draak_fase2/'
def spr(p,s,box=(0,26,64,64),bg=(232,236,240,255)):
    im=Image.open(p).convert('RGBA').crop(box); g=Image.new('RGBA',im.size,bg); g.alpha_composite(im); return g.resize((im.width*s,im.height*s),Image.NEAREST)
s=8; sp=spr(P+'sprite_r9/pitahaya2_r9A.png',s); d=ImageDraw.Draw(sp)
Z=[((7,42,22,56),(220,0,160),'A bek-roze'),((9,32,25,36),(255,140,0),'B kop'),((7,54,19,61),(255,140,0),'B poot'),((57,44,63,56),(255,140,0),'B staart'),
   ((18,43,48,47),(0,120,255),'D evenaar'),((24,31,34,35),(0,170,0),'C randen G/p'),((47,37,59,45),(0,170,0),'C'),((27,58,31,61),(0,170,0),'C')]
for (x0,y0,x1,y1),c,t in Z:
    d.ellipse([x0*s-6,(y0-26)*s-6,x1*s+6,(y1-26)*s+6],outline=c,width=3); d.text((x0*s,(y0-26)*s-16),t,fill=c)
m=Image.open(P+'model/model.png').convert('RGBA'); f=8/(3*5.076); m=m.resize((round(m.width*f),round(m.height*f)),Image.LANCZOS)
# uitlijnen: natief (nx,ny) = model/5.076; sprite x = (nx-2)/3, y = ny/3+13 -> modelpixel X*f = 8*sx + 16/3... crop naar het spritevlak
# model op 8 px per spritepixel; spritepixel (sx,sy) <-> model (3*sx+2, 3*(sy-13))*5.076
mm=Image.new('RGBA',sp.size,(255,255,255,255)); mm.paste(m,(round(-2*f*5.076/1),round(-(3*(26-13))*5.076*f)),m)
r1=spr(B+'graphics/pokemon/salamence/anim_front.png',5,(0,0,64,64)); r2=spr(B+'graphics/pokemon/lairon/anim_front.png',5,(0,0,64,64))
pr=spr(P+'eindkeuring/proef_alles.png',s)
W=Image.new('RGB',(sp.width+40+2*r1.width+20, sp.height+max(sp.height,r1.height)+200),(255,255,255)); D=ImageDraw.Draw(W)
W.paste(sp,(10,20)); D.text((10,4),'r9A 8x (probleemzones omcirkeld)',fill=(0,0,0))
W.paste(mm,(sp.width+30,20)); D.text((sp.width+30,4),'model (bevroren) op dezelfde maat',fill=(0,0,0))
y=sp.height+40; W.paste(pr,(10,y)); D.text((10,y-16),'proef keurder: reparaties A+B+C+palet (geen oplevering, alleen toets)',fill=(0,0,0))
W.paste(r1,(sp.width+30,y)); W.paste(r2,(sp.width+30+r1.width+10,y)); D.text((sp.width+30,y-16),'Gen 3: Salamence, Lairon (5x)',fill=(0,0,0))
y2=y+max(pr.height,r1.height)+30; x=10
for p in [P+'sprite_r9/pitahaya2_r9A.png',P+'eindkeuring/proef_alles.png',B+'graphics/pokemon/salamence/anim_front.png',B+'graphics/pokemon/lairon/anim_front.png']:
    for k in (1,2):
        im=spr(p,k,(0,0,64,64)); W.paste(im,(x,y2)); x+=im.width+8
D.text((10,y2-16),'1x en 2x: r9A, proef, Salamence, Lairon',fill=(0,0,0))
W.save(P+'eindkeuring/vel.png'); print(W.size)
