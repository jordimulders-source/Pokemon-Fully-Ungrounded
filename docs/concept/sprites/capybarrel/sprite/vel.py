from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'; C=R+'docs/concept/sprites/capybarrel/'
def on(im,col):
    bg=Image.new('RGBA',im.size,col+(255,)); bg.alpha_composite(im.convert('RGBA')); return bg.convert('RGB')
def load(p):  # P met transparency=0 eerst openen
    return Image.open(p).convert('RGBA')
S=8; W=4*(64*S+20)+20; Hh=40+64*S+40+64*S+40+200
V=Image.new('RGB',(W,Hh),(255,255,255)); d=ImageDraw.Draw(V)
# rij 1: model (verkleind tot figuurmaat 46x34 op 8x, zelfde plek) + A B C
m=Image.open(C+'referenties/model_r3.png').convert('RGB').crop((143,254,881,799)).resize((46*S,34*S),Image.LANCZOS)
mm=Image.new('RGB',(64*S,64*S),(235,235,235)); mm.paste(m,(9*S,26*S))
V.paste(mm,(20,40)); d.text((20,20),'model r3 (verkleind naar 46x34, 8x)',fill=(0,0,0))
src={'A':('hypno',(22,25,29,28)),'B':('drowzee',(24,19,31,23)),'C':('camerupt',(18,39,23,44))}
for i,v in enumerate('ABC'):
    sp=load(C+f'sprite/r1/capybarrel_{v}.png')
    V.paste(on(sp,(235,235,235)).resize((64*S,64*S),Image.NEAREST),(20+(i+1)*(64*S+20),40))
    d.text((20+(i+1)*(64*S+20),20),f'{v}: oog uit {src[v][0]}',fill=(0,0,0))
# rij 2: bron-oogsprites 8x met kader om het oog
y2=40+64*S+40
for i,v in enumerate('ABC'):
    n,(x0,y0,x1,y1)=src[v]
    im=Image.open(R+f'graphics/pokemon/{n}/anim_front_gba.png').convert('RGBA').crop((0,0,64,64))
    big=on(im,(235,235,235)).resize((64*S,64*S),Image.NEAREST); dd=ImageDraw.Draw(big)
    dd.rectangle([x0*S-2,y0*S-2,x1*S+1,y1*S+1],outline=(0,160,255),width=3)
    V.paste(big,(20+(i+1)*(64*S+20),y2)); d.text((20+(i+1)*(64*S+20),y2-20),f'bron {v}: {n} (blauw kader = overgenomen pixels)',fill=(0,0,0))
# kop-close-up model vs A/B/C in eerste kolom van rij 2
kop=Image.open(C+'referenties/model_r3.png').convert('RGB').crop((143,254,143+int(23*16.04),254+int(21*16.04))).resize((23*10,21*10),Image.LANCZOS)
V.paste(kop,(20,y2)); d.text((20,y2-20),'kop model / A / B (10x)',fill=(0,0,0))
for k,v in enumerate('AB'):
    sp=on(load(C+f'sprite/r1/capybarrel_{v}.png'),(235,235,235)).crop((9,26,32,47)).resize((230,210),Image.NEAREST)
    V.paste(sp,(20+(k%2)*250,y2+220+ (0)) if k==0 else (270,y2))
sp=on(load(C+'sprite/r1/capybarrel_C.png'),(235,235,235)).crop((9,26,32,47)).resize((230,210),Image.NEAREST); V.paste(sp,(270,y2+220))
d.text((20,y2+435),'links onder A, rechts boven B, rechts onder C',fill=(0,0,0))
# rij 3: 1x op licht en donker
y3=y2+64*S+40
for i,v in enumerate('ABC'):
    sp=load(C+f'sprite/r1/capybarrel_{v}.png')
    for k,col in enumerate([(248,248,240),(40,48,64)]):
        V.paste(on(sp,col),(20+i*200+k*70,y3+20))
        V.paste(on(sp,col).resize((128,128),Image.NEAREST),(700+i*300+k*140,y3+20))
    d.text((20+i*200,y3),f'{v} 1x',fill=(0,0,0))
d.text((700,y3),'2x licht/donker: A | B | C',fill=(0,0,0))
V.save(C+'sprite/r1/vel.png'); print(V.size)
