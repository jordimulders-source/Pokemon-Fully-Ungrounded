# vel.png: r3 8x | r2 8x | model 8x (zelfde kader) | 1x op licht en donker
from PIL import Image, ImageDraw
def s8(p):
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGB',(64,64),(232,240,232)); bg.paste(im,(0,0),im); return bg.resize((512,512),Image.NEAREST),im
a,ra=s8('bokser.png'); b,_=s8('../sprite_r2/bokser.png')
m=Image.open('../r12.png').convert('RGB'); pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
p=10.24; ph=10.25; s=88/63; x0=ph+(12-10*s)*p; y0=ph+5*p; side=64*s*p
mk=pad.crop((int(x0)+200,int(y0)+200,int(x0+side)+200,int(y0+side)+200)).resize((512,512),Image.LANCZOS)
o=Image.new('RGB',(3*522+120,560),(255,255,255)); d=ImageDraw.Draw(o)
for i,(t,im) in enumerate([('r3',a),('r2',b),('model r12',mk)]): o.paste(im,(i*522,30)); d.text((i*522,10),t+' (8x)',fill=(0,0,0))
for i,c in enumerate([(248,248,248),(40,48,64)]):
    t=Image.new('RGB',(80,80),c); t.paste(ra,(8,8),ra); o.paste(t,(3*522+20,30+i*100))
d.text((3*522+20,10),'1x',fill=(0,0,0)); o.save('vel.png')
w=Image.new('RGB',(512,512),(255,255,255)); w.paste(Image.open('bokser.png').convert('RGBA').resize((512,512),Image.NEAREST),(0,0),Image.open('bokser.png').convert('RGBA').resize((512,512),Image.NEAREST)); w.save('bokser_8x.png')
