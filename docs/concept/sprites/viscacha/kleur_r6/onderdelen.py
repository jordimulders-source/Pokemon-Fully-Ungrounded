"""Onderdelenvel: per onderdeel sprite (links) en Gemini64 (rechts) op dezelfde schaal (12x), met vinkje uit NOTITIES."""
import sys
from PIL import Image, ImageDraw, ImageFont
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/viscacha/kleur_r6/'
sys.path.insert(0,D); from palet import PAL
r=[l.rstrip('\n') for l in open(D+'raster.txt')][:64]; im=Image.new('RGB',(64,64))
im.putdata([(255,255,255) if c=='.' else PAL[int(c,16)] for row in r for c in row])
g=Image.open(D+'gemini64.png').convert('RGB')
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
DELEN=[('kop',0,14,30,42),('oor ver',8,14,16,26),('oor nabij',17,15,27,27),('oog (bewust anders)',12,27,21,35),('neus',3,30,12,38),('mond',4,32,14,40),
('snorharen',0,32,25,45),('gele snuitpluk',3,26,12,34),('wangaanhangsel',16,27,30,41),('borst',8,36,26,48),('voorpoten',10,42,28,54),('lijf',24,28,50,52),
('buik',24,40,42,54),('achterpoten',22,48,52,63),('staart',46,26,64,51),('pluim',48,12,62,30)]
Z=12; cols=4; cw=2*Z*28+40; W=Image.new('RGB',(cols*cw//2+20, 0+ ((len(DELEN)+1)//2)*(Z*26+30)),'white')
W=Image.new('RGB',(2*(2*Z*31+50),8*(Z*25+28)),(236,236,240)); d=ImageDraw.Draw(W)
for i,(n,x0,y0,x1,y1) in enumerate(DELEN):
    cx=(i%2)*(2*Z*31+50)+10; cy=(i//2)*(Z*25+28)+4
    a=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST); b=g.crop((x0,y0,x1,y1)).resize(a.size,Image.NEAREST)
    d.text((cx,cy),n+'  (sprite | Gemini)',fill='black',font=F); W.paste(a,(cx,cy+18)); W.paste(b,(cx+a.size[0]+8,cy+18))
W.save(D+'onderdelen.png')
