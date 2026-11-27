# Vellen ronde 7: vel.png (r7 | r6 | model, 8x; 1x licht/donker), studie_manen.png, lijnkaart_lokken.png
import json, os
from PIL import Image, ImageDraw
GP='../../../../../../graphics/pokemon/'
def rgba(p):
    im=Image.open(p).convert('RGBA'); return im
# ---------- vel
Z=512; V=Image.new('RGBA',(3*(Z+10),Z+40+170),(255,255,255,255)); d=ImageDraw.Draw(V)
r7=rgba('r7/kudu_r7.png'); r6=rgba('r6/kudu_r6.png'); imp=rgba('../../impala/af/impala.png')
mm=Image.open('r3/model_A3.png').convert('RGBA').crop((91-6*16,0,91-6*16+1024,1024)).resize((Z,Z),Image.LANCZOS)
for i,(t,im) in enumerate([('r7 8x (manen als losse lokken)',r7),('r6 8x',r6)]):
    b=im.resize((Z,Z),Image.NEAREST); V.paste(b,(i*(Z+10),20),b); d.text((i*(Z+10),4),t,fill=(0,0,0))
V.paste(mm,(2*(Z+10),20)); d.text((2*(Z+10),4),'model A3 verkleind',fill=(0,0,0))
y=Z+50
for j,bg in enumerate([(255,255,255,255),(40,44,52,255)]):
    x=j*320; V.paste(Image.new('RGBA',(300,150),bg),(x,y))
    for k,im in enumerate([r7,r6,imp]): V.paste(im,(x+10+k*95,y+40),im)
d.text((0,y-14),'1x op licht en donker: r7 | r6 | impala (af)',fill=(0,0,0))
V.save('r7/vel.png')
# ---------- studie
def sprite(n):
    f=GP+n+'/anim_front_gba.png'; p=GP+n+'/normal_gba.pal'
    if not os.path.exists(f): f=GP+n+'/anim_front.png'; p=GP+n+'/normal.pal'
    if not os.path.exists(p): p=os.path.dirname(GP+n)+'/normal.pal'
    im=Image.open(f); pal=[tuple(map(int,l.split())) for l in open(p).read().split('\n')[3:19] if l.strip()]
    px=im.load(); out=Image.new('RGB',(64,64))
    for yy in range(64):
        for xx in range(64): out.putpixel((xx,yy),(255,255,255) if px[xx,yy]==0 else pal[px[xx,yy]])
    return out
ST=[('growlithe','Gen 3 - JORDI\'S BRON',[
  'Kraag + borstplukken = eigen vorm over het lijf.',
  'Rand plukken: lichtkant selout = donkerste eigen',
  'creme (a, lum 95); schaduwkant/onderkant zwart.',
  'Lijf naast de kraag krijgt donkere lijftint (c/d):',
  'de kraag "werpt schaduw" -> los van het lijf.',
  'Pluk: grote lichte vlakken (1/7), 1 tint donkerder',
  '(8) aan onder-/rechterkant, punten als zigzag.',
  'Binnenlijn kort (2-5 px), alleen waar pluk over',
  'pluk valt; nooit per-pixel-gemiddelde tinten.']),
 ('arcanine','Gen 3 - JORDI\'S BRON',[
  'Manen = 4-6 grote plukken, elk 4-8 px breed.',
  'Tinten: 7/8 licht (240), 9 midden (196), a lijn',
  '(112). a = lijn EN selout; zwart (f) alleen op',
  'de schaduwkant van de buitenrand.',
  'Plukken eindigen in punten (zigzag aaa/a77).',
  'Waar manen over het oranje lijf vallen: zwarte',
  'omtrek + donker lijf (e/d) eronder = los.',
  'Licht linksboven per pluk, harde tintgrenzen.']),
 ('sawsbuck','Gen 5 - hert, nekkraag',[
  'Creme nekkraag als eigen vorm over de bruine',
  'hals/borst: rondom omlijnd (2/8/9), lok-',
  'punten steken over de borst. Kraag 2 tinten',
  '(6 licht, c schaduw) + lijn.']),
 ('mudsdale','Gen 7 - paardenmanen',[
  'Manen hangen in lokken (4-5 px) langs de hals',
  'en eindigen op de schouder; tussen elke lok een',
  '1-px lijn (a); lichtere spikkel (1) bovenaan elke',
  'lok. Manen hebben eigen omtrek tegen het lijf.']),
 ('lycanroc','Gen 7 - nekkraag met punten',[
  'Kraag om de hals als losse vorm, punten naar',
  'onder/achter over schouder en borst, omlijnd.']),
 ('stoutland','Gen 5 - vachtmantel',[
  'Mantel ligt als aparte vorm over de rug,',
  'eigen donkere omtrek tegen het lijf.'])]
W8=64*6; S=Image.new('RGB',(3*(W8+300),2*(W8+30)+60),'white'); d=ImageDraw.Draw(S)
d.text((4,4),'Studie manen (Jordi: Growlithe/Arcanine = bron; manen LOS van het lichaam). 6x. Gen 4+ alleen voor de vorm.',fill=(0,0,0))
for i,(n,t,notes) in enumerate(ST):
    cx=(i%3)*(W8+300); cy=30+(i//3)*(W8+30)
    S.paste(sprite(n).resize((W8,W8),Image.NEAREST),(cx,cy+14)); d.text((cx,cy),n+'  ('+t+')',fill=(160,0,0) if i<2 else (0,0,0))
    for k,s in enumerate(notes): d.text((cx+W8+6,cy+20+k*14),s,fill=(0,0,0))
S.save('r7/studie_manen.png')
# ---------- lijnkaart: model met de r7-lijnen (d = lokrand/binnenlijn, 0 = omtrek schaduwkant) en lokken
g=json.load(open('r7/grid.json'))['grid']; r6=json.load(open('r6/grid.json'))['grid']
x1,x2,y1,y2=7,33,23,48; p=16; k=3
M=Image.open('r3/model_A3.png').convert('RGBA').crop((91+x1*p,y1*p,91+x2*p,y2*p)).resize(((x2-x1)*p*k//2,(y2-y1)*p*k//2),Image.NEAREST)
c=(p*k)//2; O=Image.new('RGBA',M.size,(0,0,0,0)); od=ImageDraw.Draw(O)
for yy in range(y1,y2):
    for xx in range(x1,x2):
        if g[yy][xx]==r6[yy][xx] and g[yy][xx] not in 'lmd': continue
        X=(xx-x1)*c; Y=(yy-y1)*c
        if g[yy][xx]=='d': od.rectangle([X+6,Y+6,X+c-6,Y+c-6],outline=(255,0,0,255),width=3)
        elif g[yy][xx]=='0': od.rectangle([X+6,Y+6,X+c-6,Y+c-6],outline=(0,90,255,255),width=3)
M.alpha_composite(O); dm=ImageDraw.Draw(M)
for t,(xx,yy) in {'KA':(9.4,34),'KB':(12.2,37),'K-onder':(14.2,43),'M1':(16.3,33),'M2':(19.8,34),'M3 schouder':(22.6,36.5),
                  'kam A':(23.5,26.6),'kam B':(25.6,28.6),'kam C':(26.4,30.0),'kam D':(23,31),'hals':(13.0,30)}.items():
    X=(xx-x1)*c; Y=(yy-y1)*c; dm.rectangle([X-1,Y-1,X+6*len(t)+2,Y+11],fill=(255,255,255,200)); dm.text((X+1,Y),t,fill=(0,0,0))
L=Image.new('RGBA',(M.width,M.height+30),(255,255,255,255)); L.paste(M,(0,30))
ImageDraw.Draw(L).text((4,4),'Model A3 (rij 23-47, x 7-32) met r7: rood = d (lokrand lichtkant / binnenlijn), blauw = 0 (omtrek schaduwkant)',fill=(0,0,0))
L.save('r7/lijnkaart_lokken.png'); print('ok')
