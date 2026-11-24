# vel.png: sprite 8x | model in hetzelfde kader 8x | 1x op licht en donker. bokser_8x.png apart.
import sys; from PIL import Image, ImageDraw; import numpy as np
SP=sys.argv[1] if len(sys.argv)>1 else 'bokser.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'vel.png'
sp=Image.open(SP); rgba=sp.convert('RGBA')
s8=rgba.resize((512,512),Image.NEAREST)
# model: natief (12..72, 5..93) = 43x63 spritecellen -> in 64x64 kader op x+10
m=Image.open('../r12.png').convert('RGB'); p=10.24; ph=10.25; s=88/63
x0=ph+(12-10*s)*p; y0=ph+5*p; side=64*s*p
pad=Image.new('RGB',(1424,1424),(255,255,255)); pad.paste(m,(200,200))
mk=pad.crop((int(x0)+200,int(y0)+200,int(x0+side)+200,int(y0+side)+200)).resize((512,512),Image.LANCZOS)
o=Image.new('RGB',(512*2+40+200,560),(255,255,255)); d=ImageDraw.Draw(o)
bg=Image.new('RGB',(512,512),(232,240,232)); bg.paste(s8,(0,0),s8); o.paste(bg,(10,30)); o.paste(mk,(542,30))
d.text((10,8),'sprite r1 (8x)',fill=(0,0,0)); d.text((542,8),'model r12 (zelfde kader)',fill=(0,0,0))
for i,c in enumerate([(248,248,248),(40,48,64)]):
    t=Image.new('RGB',(80,80),c); t.paste(rgba,(8,8),rgba); t2=t.resize((160,160),Image.NEAREST) if False else t
    o.paste(t,(1080,30+i*100))
    t2=Image.new('RGB',(64,64),c); t2.paste(rgba,(0,0),rgba); o.paste(t2.resize((128,128),Image.NEAREST),(1080,230+i*150) if False else (1180,30+i*100)) if False else None
d.text((1080,10),'1x licht/donker',fill=(0,0,0))
o.save(OUT)
bg2=Image.new('RGB',(512,512),(255,255,255)); bg2.paste(s8,(0,0),s8); bg2.save(SP.replace('.png','_8x.png'))
