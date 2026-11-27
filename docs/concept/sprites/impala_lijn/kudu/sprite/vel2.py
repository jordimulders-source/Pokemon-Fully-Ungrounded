# Vel ronde 2: r2 | r1-A | model (A2a) verkleind, alle 8x; impala (af) 8x; 1x op licht en donker; onderaan manenmodellen A2a/A2b
from PIL import Image, ImageDraw
def rgba(p):
    im=Image.open(p)
    if im.mode=='P': im.save('/tmp/_v.png',transparency=0); im=Image.open('/tmp/_v.png')
    return im.convert('RGBA')
S=512; V=Image.new('RGBA',(4*S+50,S+40+150+40+460),(255,255,255,255)); d=ImageDraw.Draw(V)
tiles=[('r2',rgba('r2/kudu_r2.png')),('r1-A',rgba('r1/kudu_r1_A.png')),('impala (af)',rgba('../../impala/af/impala.png'))]
m=Image.open('r2/model_A2a.png').convert('RGBA').crop((91-6*16,0,91-6*16+1024,1024)).resize((S,S),Image.LANCZOS)
for i,(t,im) in enumerate(tiles[:2]):
    V.paste(im.resize((S,S),Image.NEAREST),(i*(S+10),20),im.resize((S,S),Image.NEAREST)); d.text((i*(S+10),4),t+' 8x',fill=(0,0,0,255))
V.paste(m,(2*(S+10),20)); d.text((2*(S+10),4),'model A2a verkleind (r3b + manen A, boog weg, lokpunten)',fill=(0,0,0,255))
im=tiles[2][1]; V.paste(im.resize((S,S),Image.NEAREST),(3*(S+10),20),im.resize((S,S),Image.NEAREST)); d.text((3*(S+10),4),'impala af 8x',fill=(0,0,0,255))
y=S+40
for j,bg in enumerate([(255,255,255,255),(232,232,224,255),(40,44,52,255),(16,16,16,255)]):
    V.paste(Image.new('RGBA',(150,150),bg),(j*160,y))
    for k,(t,im) in enumerate(tiles):
        V.paste(im,(j*160+4+k*0,y+4+k*0),im) if k==0 else None
    V.paste(tiles[0][1].resize((128,128),Image.NEAREST),(j*160+11,y+11),tiles[0][1].resize((128,128),Image.NEAREST)) if False else None
for j,bg in enumerate([(255,255,255,255),(40,44,52,255)]):
    x=700+j*300; V.paste(Image.new('RGBA',(280,150),bg),(x,y))
    for k,(t,im) in enumerate(tiles): V.paste(im,(x+10+k*85,y+40),im)
d.text((700,y-14),'1x op licht en donker: r2 | r1-A | impala',fill=(0,0,0,255))
y+=190
for i,n in enumerate(['A','A2a','A2b']):
    p={'A':'r1/model_A.png','A2a':'r2/model_A2a.png','A2b':'r2/model_A2b.png'}[n]
    mm=Image.open(p).convert('RGBA').crop((200,350,700,800)).resize((440,396)); V.paste(mm,(i*460,y+16))
    d.text((i*460,y),{'A':'r1 A (boog = oude schouderlijn)','A2a':'A2a: boog weg, punten keelfranje r3b (gebruikt)','A2b':'A2b: boog weg, punten r3c (alternatief)'}[n],fill=(0,0,0,255))
for i,n in enumerate(['A2a','A2b']):
    r=rgba(f'r2/red_{n}.png'); V.paste(r,(1400+i*80,y+30),r)
d.text((1400,y+16),'kale reductie A2a | A2b (1x)',fill=(0,0,0,255))
V.save('r2/vel.png'); print(V.size)
