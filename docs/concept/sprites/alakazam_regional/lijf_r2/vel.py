# vel.py: per optie hele sprite 6x + 1x op licht/donker + label, daaronder borst-close-up 16x -> vel.png
import os,pal
from PIL import Image,ImageDraw,ImageFont
H=os.path.dirname(os.path.abspath(__file__))
try: F=ImageFont.load_default(size=18)
except TypeError: F=ImageFont.load_default()
L=[('O1r (basis, strikje)','basis_O1r.txt'),('S1 keelwam','opt_S1.txt'),('S2 sleutelbeen-\nvlekken','opt_S2.txt'),('S3 keelvlek\n(roodborstje)','opt_S3.txt'),
   ('S4 rode\nstropdastekening','opt_S4.txt'),('S5 zwarte streep\n+ rood accent','opt_S5.txt'),('S6 geen rood','opt_S6.txt'),('S7 rode ruit\nop borstbeen','opt_S7.txt'),('S8 zwarte streep\nzonder rood','opt_S8.txt')]
Z=6; CB=(24,21,38,36); CZ=16
def een(rows):
    a=pal.rgb(rows).convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if rows[y][x]=='.': px[x,y]=(0,0,0,0)
    return a
cells=[]
for t,f in L:
    rows=pal.load(H+'/'+f); W=64*Z; cw=(CB[2]-CB[0])*CZ; ch=(CB[3]-CB[1])*CZ
    c=Image.new('RGB',(max(W,cw),W+100+ch+10),'white'); c.paste(pal.rgb(rows).resize((W,W),Image.NEAREST),(0,0))
    one=een(rows)
    for i,bg in enumerate([(248,248,248),(40,40,48)]):
        q=Image.new('RGBA',(64,64),bg+(255,)); q.alpha_composite(one); c.paste(q.convert('RGB'),(i*72,W+6))
    ImageDraw.Draw(c).multiline_text((150,W+10),t,fill=(0,0,0),font=F)
    c.paste(pal.rgb(rows).crop(CB).resize((cw,ch),Image.NEAREST),(0,W+100)); cells.append(c)
cw,chh=cells[0].size; O=Image.new('RGB',(3*(cw+12),3*(chh+16)),'white')
for i,c in enumerate(cells): O.paste(c,((i%3)*(cw+12),(i//3)*(chh+16)))
O.save(H+'/vel.png'); print(O.size)
