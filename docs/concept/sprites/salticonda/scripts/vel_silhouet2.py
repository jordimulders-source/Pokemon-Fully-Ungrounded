"""Vergelijkingsvel silhouet ronde 2 (D, E naast A uit ronde 1)."""
from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/salticonda/'
BG=(236,232,222,255); DARK=(48,40,48,255)
def mask(f):
    p=Image.open(f).crop((0,0,64,64)); P=p.load()
    return {(x,y) for x in range(64) for y in range(64) if P[x,y]!=0}
def sil(pts,col=DARK,sc=1):
    im=Image.new('RGBA',(64*sc,64*sc),(0,0,0,0)); d=ImageDraw.Draw(im)
    for x,y in pts: d.rectangle([x*sc,y*sc,x*sc+sc-1,y*sc+sc-1],fill=col)
    return im
def box(p):
    xs=[q[0] for q in p]; ys=[q[1] for q in p]; return max(xs)-min(xs)+1, max(ys)-min(ys)+1
V=[('A (ronde 1)',mask(D+'silhouet1/variant_A.png')),
   ('D: 4 windingen',mask(D+'silhouet2/variant_D.png')),
   ('E: 3 windingen',mask(D+'silhouet2/variant_E.png'))]
W,H=1300,880
vel=Image.new('RGBA',(W,H),BG); d=ImageDraw.Draw(vel)
def txt(x,y,s): d.text((x,y),s,fill=(30,30,30,255))
x=10
for lab,p in V:
    vel.alpha_composite(sil(p,sc=4),(x,24)); w,h=box(p)
    txt(x,6,'%s  %d px, %dx%d'%(lab,len(p),w,h))
    vel.alpha_composite(sil(p),(x+270,120)); x+=350
# overlay D en E over A
txt(10,300,'Overlay: A uit ronde 1 (groen) over D en E (grijs)')
A=V[0][1]
for i,(lab,p) in enumerate(V[1:]):
    ov=Image.new('RGBA',(256,256),(255,255,255,255))
    ov.alpha_composite(sil(p,(48,40,48,140),4)); ov.alpha_composite(sil(A,(120,200,120,150),4))
    vel.alpha_composite(ov,(10+i*270,318)); txt(10+i*270,578,'A (groen) over '+lab+' (grijs)')
# vergelijkingsrij
y=610
txt(10,y-14,'Vergelijking 1x en 2x')
G=R+'graphics/pokemon/%s/anim_front.png'
cmp=[(n,mask(G%n)) for n in ['torkoal','hippowdon','camerupt','sandaconda','wailord']]
cmp=[('silicobra-U',mask(D+'../silicobra_uyuni/af/silicobra_uyuni.png'))]+cmp+V
x=10
for lab,p in cmp:
    vel.alpha_composite(sil(p),(x,y)); txt(x,y+66,'%s %d'%(lab.split(' ')[0].rstrip(':'),len(p))); x+=80
x=10
for lab,p in cmp[1:]:
    vel.alpha_composite(sil(p,sc=2),(x,y+86)); x+=136
vel.save(D+'silhouet2/vel.png')
