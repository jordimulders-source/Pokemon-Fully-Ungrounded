# zij-aan-zij: sprite-uitsnede (rooster) naast het model op dezelfde schaal, met celraster
import sys
from PIL import Image, ImageDraw
import tempfile; S=tempfile.gettempdir()+'/'
def zij(spr,uit,cx0,cy0,cx1,cy1,z=20):
    im=Image.open(spr)
    if im.mode=='P': im.save(S+'_t.png',transparency=0); im=Image.open(S+'_t.png')
    im=im.convert('RGBA'); OX=6
    s=im.crop((OX+cx0,cy0,OX+cx1,cy1)).resize(((cx1-cx0)*z,(cy1-cy0)*z),Image.NEAREST)
    m=Image.open('r3/model_A3.png').convert('RGBA').crop((91+cx0*16,cy0*16,91+cx1*16,cy1*16)).resize(s.size,Image.LANCZOS)
    V=Image.new('RGBA',(s.size[0]*2+10,s.size[1]),(255,255,255,255)); V.paste(Image.new('RGBA',s.size,(170,200,225,255)),(0,0)); V.paste(s,(0,0),s); V.paste(m,(s.size[0]+10,0))
    d=ImageDraw.Draw(V)
    for ox in (0,s.size[0]+10):
        for i in range(cx1-cx0+1): d.line([(ox+i*z,0),(ox+i*z,V.size[1])],fill=(255,0,0,90) if (cx0+i)%5 else (255,0,0,255))
        for j in range(cy1-cy0+1): d.line([(ox,j*z),(ox+s.size[0],j*z)],fill=(255,0,0,90) if (cy0+j)%5 else (255,0,0,255))
        for i in range(0,cx1-cx0,5): d.text((ox+i*z+2,2),str(cx0+i),fill=(255,0,0))
        for j in range(0,cy1-cy0,5): d.text((ox+2,j*z+2),str(cy0+j),fill=(255,0,0))
    V.save(uit)
if __name__=='__main__':
    a=sys.argv; zij(a[1],a[2],*map(int,a[3:7]),**({'z':int(a[7])} if len(a)>7 else {}))
