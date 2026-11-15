# Vel c10: kop op 12x (c7 A zonder boog, c10 1, c10 2) naast een vergrote foto-uitsnede van de kop (eigen uitsnede,
# gespiegeld zodat hij net als de welp naar links kijkt, plus het origineel); daaronder 3x en 1x greige (normaal) en grijs (shiny).
from PIL import Image, ImageDraw, ImageOps
def png(f):
    im=Image.open(f); im.info['transparency']=0; im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
S=12; kb=(6,16,34,42); kw,kh=(kb[2]-kb[0])*S,(kb[3]-kb[1])*S
foto=Image.open('foto_kop_zoom.png').convert('RGB'); foto=foto.resize((int(foto.width*kh/foto.height),kh),Image.LANCZOS)
V=[('c7 A (zonder boog)','../c7/welp_c7_a'),('1: kom op ooghoogte','welp_c10_1'),('2: kom 1 px lager','welp_c10_2')]
W=3*(kw+10)+2*(foto.width+10); H=20+kh+40+2*(192+10+64+30)
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o)
for i,(n,f) in enumerate(V):
    o.paste(png(f+'.png').crop(kb).resize((kw,kh),Image.NEAREST),(i*(kw+10),20)); d.text((i*(kw+10)+2,4),n,fill='black')
x=3*(kw+10); o.paste(ImageOps.mirror(foto),(x,20)); d.text((x+2,4),'foto-kop, gespiegeld (kijkt naar links)',fill='black')
x+=foto.width+10; o.paste(foto,(x,20)); d.text((x+2,4),'foto-kop, origineel',fill='black')
y=20+kh+40
for t,nm in (('','greige (normaal)'),('_grijs','grijs (shiny)')):
    d.text((4,y-14),'3x en 1x '+nm,fill='black')
    for i,(_,f) in enumerate(V):
        m=png(f+t+'.png'); o.paste(m.resize((192,192),Image.NEAREST),(i*(kw+10),y)); o.paste(m,(i*(kw+10)+200,y+128))
    y+=192+10+64+30
o.save('vel.png')
