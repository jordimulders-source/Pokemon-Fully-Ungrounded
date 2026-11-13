# vel.py: r11 + O1..O4 op 6x, Mr. Rime op 6x, en elk op 1x op licht en donker -> vel.png
import os,pal
from PIL import Image,ImageDraw,ImageFont
H=os.path.dirname(os.path.abspath(__file__)); GP=H+'/../../../../../graphics/pokemon/'
try: F=ImageFont.load_default(size=18)
except TypeError: F=ImageFont.load_default()
Z=6; items=[('r11 (basis)','basis_r11.txt'),('O1 grijs lijf,\nwitte borstplaat','opt_O1.txt'),('O2 = O1, flank\nvervaagt naar zwart','opt_O2.txt'),('O3 Mr. Rime:\nronde witte buikvlek','opt_O3.txt'),('O4 = O2 met\nklein strikje','opt_O4.txt')]
def een(rows):
    im=Image.new('RGBA',(64,64),(0,0,0,0)); a=pal.rgb(rows).convert('RGBA'); px=a.load()
    for y in range(64):
        for x in range(64):
            if rows[y][x]=='.': px[x,y]=(0,0,0,0)
    return a
cols=[]
for t,f in items:
    rows=pal.load(H+'/'+f); big=pal.rgb(rows).resize((64*Z,64*Z),Image.NEAREST); one=een(rows)
    c=Image.new('RGB',(64*Z,64*Z+130),'white'); c.paste(big,(0,0))
    for i,bg in enumerate([(248,248,248),(40,40,48)]):
        q=Image.new('RGBA',(64,64),bg+(255,)); q.alpha_composite(one); c.paste(q.convert('RGB'),(i*72,64*Z+6))
    ImageDraw.Draw(c).multiline_text((150,64*Z+10),t,fill=(0,0,0),font=F); cols.append(c)
_r=Image.open(GP+'mr_rime/front.png'); _r.info['transparency']=0; rime=_r.convert('RGBA'); rb=Image.new('RGBA',(64,64),(152,208,160,255)); rb.alpha_composite(rime)
c=Image.new('RGB',(64*Z,64*Z+130),'white'); c.paste(rb.convert('RGB').resize((64*Z,64*Z),Image.NEAREST),(0,0))
for i,bg in enumerate([(248,248,248),(40,40,48)]):
    q=Image.new('RGBA',(64,64),bg+(255,)); q.alpha_composite(rime); c.paste(q.convert('RGB'),(i*72,64*Z+6))
ImageDraw.Draw(c).multiline_text((150,64*Z+10),'Mr. Rime (studie)',fill=(0,0,0),font=F); cols.append(c)
W=3*(64*Z+12); O=Image.new('RGB',(W,2*(64*Z+142)),'white')
for i,c in enumerate(cols): O.paste(c,((i%3)*(64*Z+12),(i//3)*(64*Z+142)))
O.save(H+'/vel.png'); print(O.size)
