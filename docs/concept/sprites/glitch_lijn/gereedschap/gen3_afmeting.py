"""Gen 3-tegenhanger van MissingNo's ontstaan: een ECHTE sprite die met de VERKEERDE afmeting
wordt uitgelezen. In Gen 1 komt de omgekeerde L uit een maatfout (header 8x8 tegels in een
7x7-buffer, plus een overloop in de centreerformule). Hier: de 4bpp-tegeldata van een echte
Gen 3-frontsprite (zoals in de ROM) wordt uitgelezen met een verkeerd aantal tegels per rij
en/of een verschoven startadres. Doorzichtigheid (index 0) blijft echt, dus de omtrek is
onregelmatig. Palet: index 0 (?-palet) of het eigen palet.
Gebruik: python3 gen3_afmeting.py UITMAP soort1 soort2 ..."""
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import pal_none, REPO
def tiles4bpp(png):
    im=Image.open(png); im=im.crop((0,0,64,64)); px=im.load(); out=bytearray()
    for ty in range(8):
        for tx in range(8):
            for y in range(8):
                for x in range(0,8,2):
                    out.append((px[tx*8+x,ty*8+y]&0xF)|((px[tx*8+x+1,ty*8+y]&0xF)<<4))
    return bytes(out), [tuple(im.getpalette()[i*3:i*3+3]) for i in range(16)]
def lees(data,pal,per_rij=8,start=0,breed=64):
    im=Image.new('RGBA',(breed,64),(0,0,0,0)); px=im.load(); n=start
    for t in range((breed//8)*8):
        tx,ty=t%per_rij,t//per_rij
        for i in range(32):
            b=data[n % len(data)] if 0<=n<len(data) else 0; n+=1
            for k,v in enumerate((b&0xF,b>>4)):
                x,y=tx*8+(i*2+k)%8,ty*8+(i*2+k)//8
                if v and x<breed and y<64: px[x,y]=pal[v]+(255,)
    return im
if __name__=='__main__':
    uit=sys.argv[1]; soorten=sys.argv[2:]; os.makedirs(uit,exist_ok=True); pn=pal_none()
    varianten=[(8,0,'echt'),(7,0,'7 per rij'),(6,0,'6 per rij'),(9,0,'9 per rij'),(8,13,'start +13'),(7,200,'7/rij +200')]
    sh=Image.new('RGB',(len(varianten)*2*72+8,len(soorten)*80+16),(255,255,255)); d=ImageDraw.Draw(sh)
    for j,(lab) in enumerate(varianten): d.text((8+j*144,2),lab[2],fill=(0,0,0))
    for i,s in enumerate(soorten):
        data,eig=tiles4bpp(os.path.join(REPO,f'graphics/pokemon/{s}/anim_front_gba.png'))
        for j,(pr,st,lab) in enumerate(varianten):
            for q,pal in enumerate((eig,pn)):
                im=lees(data,pal,pr,st); x,y=8+j*144+q*72,14+i*80
                sh.paste(im,(x,y),im); im.save(f'{uit}/{s}_{pr}_{st}_{"eigen" if q==0 else "vraag"}.png')
        d.text((2,14+i*80+66),s,fill=(200,0,0))
    sh.resize((sh.size[0]*2,sh.size[1]*2),Image.NEAREST).save(f'{uit}/vel.png')
