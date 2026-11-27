# r16: studie.png (Gen 3-hoefdieren + impala/viscacha met toonkaart) en vel.png (A | B | r15 op 8x + 1x/2x op licht/donker
# naast de impala en Stantler_gba). Gebruik: python3 vel16.py
import numpy as np
from PIL import Image, ImageDraw
R='../../../../../../'
def gba(n):
    im=Image.open(R+f'graphics/pokemon/{n}/anim_front_gba.png').crop((0,0,64,64))
    L=open(R+f'graphics/pokemon/{n}/normal_gba.pal').read().split('\n')[3:19]; pl=[int(v) for l in L if l.strip() for v in l.split()]
    im=im.convert('P') if im.mode!='P' else im; im.putpalette(pl+[0]*(768-len(pl)))
    a=np.array(im); rgba=np.array(im.convert('RGBA')); rgba[a==0,3]=0; return Image.fromarray(rgba)
def eigen(p): return Image.open(p).convert('RGBA')
def toon(im):  # toonkaart: elke kleur -> grijs naar luminantierang; lijn (<70) zwart, wit/hoorn blijft licht
    a=np.array(im).astype(int); lum=(.299*a[...,0]+.587*a[...,1]+.114*a[...,2]); al=a[...,3]>0
    out=np.zeros_like(a); out[...,3]=a[...,3]
    q=np.select([lum<70,lum<125,lum<165,lum<200,lum<235],[20,90,140,185,225],250)
    for c in range(3): out[...,c]=np.where(al,q,0)
    return Image.fromarray(out.astype(np.uint8))
BG=(196,206,218,255)
def plak(V,im,x,y,s,bg=None):
    if bg: V.paste(Image.new('RGBA',(im.width*s,im.height*s),bg),(x,y))
    V.alpha_composite(im.resize((im.width*s,im.height*s),Image.NEAREST),(x,y))
# --- studie ---
REF=[('stantler',gba('stantler')),('tauros',gba('tauros')),('girafarig',gba('girafarig')),('ponyta',gba('ponyta')),
     ('arcanine',gba('arcanine')),('impala (lijn)',eigen('../../impala/af/impala.png')),('viscacha',eigen('../../../viscacha/af/viscacha.png'))]
S=4; V=Image.new('RGBA',(2*(64*S+10)*4+10,(64*S+24)*2+150),BG); d=ImageDraw.Draw(V)
for i,(n,im) in enumerate(REF):
    x=10+(i%4)*2*(64*S+10); y=10+(i//4)*(64*S+24)
    d.text((x,y),n+'  |  toonkaart (lijn, schaduw, midden, licht, hooglicht)',fill=(0,0,0,255))
    plak(V,im,x,y+12,S); plak(V,toon(im),x+64*S+6,y+12,S)
T=["Metingen (anim_front_gba): vachtvlak = 3 tinten + vaak 1 extra lichte op de grootste bolling; lijnbasis apart.",
   "Stantler: licht 214/221/245 . midden 184 . schaduw 136 (schaduw is de grootste groep: 344 px tegen 311 midden). Hooglicht op de dij (bol, linksboven),",
   "  voorkant hals/borst; schaduw als sikkel achter/onder de dij, onder de buik en als gebogen spierlijn schouder/romp. Hue 37->38->42/44->60 (lichter = geler).",
   "Ponyta: 241 . 229 . 201 (+lijn 110): hooglicht = ronde vlek boven op romp/rug en borst; schaduw onder buik en achterkant poten.",
   "Tauros: 218 . 196 . 154 . 98: licht op de schouderbult en de bil, gebogen grenzen. Arcanine: 238 . 196 . 112. Girafarig: 213 . 182 . 139.",
   "Poten (Kirlia-opbouw): lichte strook in de lengte aan de lichtkant, 3-5 px; verre poten in schaduw.",
   "Grenzen lopen met de vorm mee (bogen), nooit een horizontale band dwars over een vlak."]
y=10+2*(64*S+24)
for t in T: d.text((10,y),t,fill=(0,0,0,255)); y+=16
V.save('r16/studie.png')
# --- vel ---
A=eigen('r16/kudu_r16A.png'); B=eigen('r16/kudu_r16B.png'); O=eigen('r15/kudu_r15.png'); IMP=eigen('../../impala/af/impala.png'); ST=gba('stantler')
V=Image.new('RGBA',(3*(512+10)+10,512+40+2*140),BG); d=ImageDraw.Draw(V)
for i,(n,im) in enumerate([('r16 A (subtiel)',A),('r16 B (duidelijk)',B),('r15',O)]):
    d.text((10+i*522,4),n,fill=(0,0,0,255)); plak(V,im,10+i*522,20,8)
y=20+512+10
for bg in [(248,248,248,255),(40,44,52,255)]:
    x=10
    for im in [A,B,O,IMP,ST]: plak(V,im,x,y,1,bg); x+=70
    x=370
    for im in [A,B,O,IMP,ST]: plak(V,im,x,y,2,bg); x+=134
    y+=134
d.text((10,y),'1x en 2x: A, B, r15, impala, Stantler (licht en donker)',fill=(0,0,0,255))
V=V.crop((0,0,V.width,y+18)); V.save('r16/vel.png')
for v,im in (('A',A),('B',B)): im.resize((512,512),Image.NEAREST).save(f'r16/kudu_r16{v}_8x.png')
print('ok')
