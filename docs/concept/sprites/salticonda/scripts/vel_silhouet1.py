"""Vergelijkingsvel silhouet ronde 1."""
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
BG=(236,232,222,255); DARK=(48,40,48,255); GREY=(150,150,160,255)
def gen3(n):
    p=Image.open(R+'graphics/pokemon/%s/anim_front.png'%n).crop((0,0,64,64)); return mask(p)
def mask(p):
    P=p.load(); return {(x,y) for x in range(64) for y in range(64) if P[x,y]!=0 and (p.mode=='P' or P[x,y][3])}
def sil(pts,col=DARK,sc=1):
    im=Image.new('RGBA',(64*sc,64*sc),(0,0,0,0)); d=ImageDraw.Draw(im)
    for x,y in pts: d.rectangle([x*sc,y*sc,x*sc+sc-1,y*sc+sc-1],fill=col)
    return im
pre=mask(Image.open(D+'../silicobra_uyuni/af/silicobra_uyuni.png').convert('P') if False else Image.open(D+'../silicobra_uyuni/af/silicobra_uyuni.png'))
ek=gen3('ekans')
V={k:mask(Image.open(D+'silhouet1/variant_%s.png'%k)) for k in 'ABC'}
names={'A':'A: 4 windingen, kop bovenop, staartspits rechtsonder','B':'B: 3 windingen, laag en breed, kop hangt links-voor','C':'C: 4 windingen, staart als spits omhoog (Ekans)'}
# Ekans opgeschaald x1.4 voor de overlay, onderkant en midden gelijk
def scale(pts,f,ax,ay):
    out=set()
    for x in range(64):
        for y in range(64):
            sx=ax+(x-ax)/f; sy=ay+(y-ay)/f
            if (int(sx),int(sy)) in pts: out.add((x,y))
    return out
ek14=scale(ek,1.4,34,53)
W,H=1500,1420
vel=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(vel)
def txt(x,y,s): d.text((x,y),s,fill=(30,30,30,255))
# rij 0: bronnen
txt(10,8,'Bronnen: Ekans (skelet) 1x | Silicobra-Uyuni (pre-evo) 1x | Sandaconda 1x  -- foto\'s van Jordi')
x=10
for lab,p in [('Ekans %d px'%len(ek),ek),('Silicobra-U %d px'%len(pre),pre),('Sandaconda %d px'%len(gen3('sandaconda')),gen3('sandaconda'))]:
    vel.alpha_composite(sil(p),(x,40)); txt(x,108,lab); x+=110
for f,w in [('anaconda_kop_zijkant.png',200),('anaconda_kop_close.webp',300),('anaconda_opgerold.webp',260)]:
    im=Image.open(D+'referenties/'+f).convert('RGBA'); im.thumbnail((w,200)); vel.alpha_composite(im,(x,28)); x+=im.width+10
# rijen per variant
y=250
for k in 'ABC':
    txt(10,y-14,names[k]+'  (%d px)'%len(V[k]))
    vel.alpha_composite(sil(V[k],sc=4),(10,y))
    vel.alpha_composite(sil(V[k]),(280,y+96))
    ov=Image.new('RGBA',(256,256),(255,255,255,255)); ov.alpha_composite(sil(ek14,(120,200,120,255),4)); 
    s4=sil(V[k],(48,40,48,150),4); ov.alpha_composite(s4); vel.alpha_composite(ov,(360,y)); 
    # kop 8x naast de kopfoto
    xs=[p[0] for p in V[k]]; 
    head=Image.new('RGBA',(36*6,24*6),(255,255,255,255))
    hy={'A':9,'B':20,'C':9}[k]; hx={'A':7,'B':0,'C':8}[k]
    for (px,py) in V[k]:
        if hx<=px<hx+36 and hy<=py<hy+24:
            ImageDraw.Draw(head).rectangle([(px-hx)*6,(py-hy)*6,(px-hx)*6+5,(py-hy)*6+5],fill=DARK)
    vel.alpha_composite(head,(640,y)); 
    im=Image.open(D+'referenties/anaconda_kop_zijkant.png').convert('RGBA').resize((144,144)); vel.alpha_composite(im,(870,y))
    txt(360,y+258,'over Ekans x1.4 (groen)'); txt(640,y+150,'kop 6x naast de foto')
    y+=300
# vergelijking
txt(10,y-14,'Vergelijking 1x en 2x: zware Gen 3-eindvormen + varianten')
cmp=['torkoal','hippowdon','steelix','sandaconda','wailord','camerupt','ekans']
x=10
for n in cmp:
    p=gen3(n); vel.alpha_composite(sil(p),(x,y)); vel.alpha_composite(sil(p,sc=2),(x,y+70)); txt(x,y+200,'%s %d'%(n,len(p))); x+=140
for k in 'ABC':
    vel.alpha_composite(sil(V[k]),(x,y)); vel.alpha_composite(sil(V[k],sc=2),(x,y+70)); txt(x,y+200,'%s %d'%(k,len(V[k]))); x+=140
vel.save(D+'silhouet1/vel.png')
