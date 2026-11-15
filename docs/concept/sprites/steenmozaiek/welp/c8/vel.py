# Vel c8: kop op 12x (c7 A, cirkel 1/2/3) naast de foto-kop; daaronder 3x en 1x greige en grijs.
from PIL import Image, ImageDraw
def png(f):
    im=Image.open(f); im.info['transparency']=0; im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
S=12; kb=(6,16,34,42); kw,kh=(kb[2]-kb[0])*S,(kb[3]-kb[1])*S
foto=Image.open('../../referenties/chavin_jaguar_beeld_jordi.png').convert('RGB').crop((400,50,520,170)).resize((kh,kh),Image.LANCZOS)
V=[('c7 A (zonder cirkel)','../c7/welp_c7_a'),('1: 4 px, op ooghoogte','welp_c8_1'),('2: 4 px, lager op de wang','welp_c8_2'),('3: 3 px, hoger bij de slaap','welp_c8_3')]
W=4*(kw+10)+kh+10; H=20+kh+40+192+10+64+20+192+10+64+20
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o)
for i,(n,f) in enumerate(V):
    o.paste(png(f+'.png').crop(kb).resize((kw,kh),Image.NEAREST),(i*(kw+10),20)); d.text((i*(kw+10)+2,4),n,fill='black')
o.paste(foto,(4*(kw+10),20)); d.text((4*(kw+10)+2,4),'foto: kop',fill='black')
y=20+kh+40
for t in ('','_grijs'):
    d.text((4,y-14),'3x en 1x'+(' grijs' if t else ' greige'),fill='black')
    for i,(_,f) in enumerate(V):
        m=png(f+t+'.png'); o.paste(m.resize((192,192),Image.NEAREST),(i*(kw+10),y)); o.paste(m,(i*(kw+10)+200,y+128))
    y+=192+10+64+20
o.save('vel.png')
