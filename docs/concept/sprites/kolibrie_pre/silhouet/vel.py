from PIL import Image, ImageDraw
import numpy as np, sys
sys.path.insert(0,'.')
import silhouet as S
R='../../../../../'
def sil_of(path, frame=True):
    im=Image.open(path).convert('RGBA')
    if frame: im=im.crop((0,0,64,64))
    a=np.asarray(im.convert('RGB')); bg=a[0,0]
    return (a!=bg).any(-1) if im.getpixel((0,0))[3]==255 else np.asarray(im)[...,3]>0
def render(m,sc,col=(40,30,60)):
    im=Image.new('RGB',(64,64),(255,255,255)); px=im.load()
    for y,x in zip(*np.nonzero(m)): px[x,y]=col
    return im.resize((64*sc,64*sc),0)
def vel(versie, out, kopschaal=1.3):
    m,big=S.maak(kopschaal)
    foto=Image.open('../referenties/jordi_1_zittend_jong.webp').convert('RGB')
    ov=foto.copy(); ovl=Image.new('RGBA',foto.size,(0,0,0,0))
    a=np.asarray(big)>0; o=np.zeros((*a.shape,4),'uint8'); o[a]=(120,40,200,110)
    ov.paste(Image.fromarray(o),(0,0),Image.fromarray(o))
    ov=ov.crop((180,100,760,720)).resize((290,310))
    V=Image.new('RGB',(290+256+64+40+20,330+150),(235,235,235)); d=ImageDraw.Draw(V)
    V.paste(ov,(10,10)); V.paste(render(m,4),(310,10)); V.paste(render(m,1),(580,10))
    d.text((10,322),'foto 1 + nieuwe kop/bek (paars)',fill=0); d.text((310,270),f'silhouet {versie} 4x ({m.sum()} px)',fill=0); d.text((580,80),'1x',fill=0)
    refs=['natu','togepi','pichu','fletchling','taillow']
    x=10
    for n in refs:
        r=sil_of(R+f'graphics/pokemon/{n}/anim_front.png')
        V.paste(render(r,2),(x,340)); d.text((x,470),f'{n} {r.sum()}',fill=0); x+=130
    kol=sil_of(R+'docs/concept/sprites/kolibrie/af/kolibrie.png',False)
    V.paste(render(kol,1),(580,120)); d.text((580,186),'eindvorm 1x',fill=0)
    V.save(out)
if __name__=='__main__': vel('v1','vel_v1.png')
