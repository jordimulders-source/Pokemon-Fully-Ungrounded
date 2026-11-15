# Vel c1: boven A | B | C | p8 op 6x + foto-uitsnede op dezelfde hoogte; onder 3x en 1x naast Growlithe, Vulpix en de volwassen vorm.
from PIL import Image, ImageDraw
G='../../../../../../graphics/pokemon/'
def wit(im):
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
def gba(s):
    im=Image.open(G+s+'/anim_front_gba.png'); im=im.crop((0,0,64,64)); im.info['transparency']=0
    return wit(im.convert('RGBA'))
def png(f): return wit(Image.open(f))
eigen=[('A greige gegraveerd',png('welp_c1_A.png')),('B greige + lila/creme inleg',png('welp_c1_B.png')),('C grijs gegraveerd',png('welp_c1_C.png')),('p8 (oud)',png('../p8/welp_p8.png'))]
foto=Image.open('foto_uitsnede.png').convert('RGB'); foto=foto.resize((int(foto.width*384/foto.height),384),Image.LANCZOS)
ref=[('Growlithe',gba('growlithe')),('Vulpix',gba('vulpix')),('volwassen',png('../../af/steenjaguar.png'))]
W=4*394+foto.width+10; H=20+384+30+192+30+64+20
o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o)
for i,(n,m) in enumerate(eigen):
    o.paste(m.resize((384,384),Image.NEAREST),(i*394,20)); d.text((i*394+4,4),n,fill='black')
o.paste(foto,(4*394,20)); d.text((4*394+4,4),'foto Jordi (uitsnede)',fill='black')
y3=20+384+30; d.text((4,y3-14),'3x en 1x',fill='black')
rij=[m for _,m in eigen[:3]]+[m for _,m in ref]
for i,m in enumerate(rij):
    o.paste(m.resize((192,192),Image.NEAREST),(i*200,y3)); o.paste(m,(i*200+64,y3+192+30))
o.save('vel.png')
