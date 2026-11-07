"""Onderdelenvel: per onderdeel sprite (links) en Gemini64 (rechts) op dezelfde schaal (12x), met vinkje uit NOTITIES."""
import sys
from PIL import Image, ImageDraw, ImageFont
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r5/'
sys.path.insert(0,D); from palet import PAL
r=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]; im=Image.new('RGB',(64,64))
im.putdata([(255,255,255) if c=='.' else PAL[int(c,16)] for row in r for c in row])
g=Image.open(D+'gemini64.png').convert('RGB')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
DELEN=[('kop',0,16,26,40),('oor ver',3,10,12,22),('oor nabij',13,10,25,22),('oog (bewust anders)',7,22,17,31),('neus',0,27,8,35),('mond',0,30,10,38),
('snorharen',0,29,20,44),('gele snuitpluk',0,22,8,31),('wangaanhangsel',12,23,27,38),('borst',4,34,20,46),('voorpoten',6,40,24,53),('lijf',20,25,48,50),
('buik',20,38,40,52),('achterpoten',20,46,52,63),('staart',44,24,64,50),('pluim',47,8,62,28)]
Z=12; cols=4; cw=2*Z*28+40; W=Image.new('RGB',(cols*cw//2+20, 0+ ((len(DELEN)+1)//2)*(Z*26+30)),'white')
W=Image.new('RGB',(2*(2*Z*28+50),8*(Z*25+28)),(236,236,240)); d=ImageDraw.Draw(W)
for i,(n,x0,y0,x1,y1) in enumerate(DELEN):
    cx=(i%2)*(2*Z*28+50)+10; cy=(i//2)*(Z*25+28)+4
    a=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST); b=g.crop((x0,y0,x1,y1)).resize(a.size,Image.NEAREST)
    d.text((cx,cy),n+'  (sprite | Gemini)',fill='black',font=F); W.paste(a,(cx,cy+18)); W.paste(b,(cx+a.size[0]+8,cy+18))
W.save(D+'onderdelen.png')
