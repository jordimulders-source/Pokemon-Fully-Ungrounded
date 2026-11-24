import sys
from PIL import Image, ImageDraw
from collections import Counter
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
def run(src,dst,rows,refs=('emolga','umbreon','houndoom')):
    """rows: list of (zone, y, x0, string) ; string chars = index (hex) or '.' = skip"""
    a=Image.open(src); im=a.copy()
    cnt=Counter()
    for zone,y,x0,s in rows:
        for k,ch in enumerate(s):
            if ch in '. ': continue
            x=x0+k; new=int(ch,16); cur=a.getpixel((x,y))
            assert cur not in (0,1),(zone,x,y,cur)
            if cur!=new: im.putpixel((x,y),new); cnt[zone]+=1
    M=lambda i,v:[i.getpixel((x,y))==v for y in range(64) for x in range(64)]
    assert M(a,0)==M(im,0) and M(a,1)==M(im,1)
    assert all(not M(im,v)[j] or M(a,v)[j] or True for v in (0,) for j in range(1))
    im.save(dst+'/A0.png',transparency=0)
    # vel
    def big(f,c=(0,0,64,64)):
        return Image.open(f).convert('RGBA').crop(c).resize((512,512),0)
    V=Image.new('RGBA',(3*522+10,1180),(236,236,236,255)); d=ImageDraw.Draw(V)
    for i,f in enumerate([src,dst+'/A0.png']):
        b=big(f); V.paste(b,(10+i*522,30),b); d.text((14+i*522,10),['vorige','nieuw'][i]+': '+f,fill=(0,0,0))
    x0=10+2*522
    for j,(bg,f) in enumerate([((248,248,248),src),((248,248,248),dst+'/A0.png'),((24,24,32),src),((24,24,32),dst+'/A0.png')]):
        bx=x0+(j%2)*150; by=30+(j//2)*150
        d.rectangle([bx,by,bx+139,by+139],fill=bg)
        s1=Image.open(f).convert('RGBA'); V.paste(s1,(bx+38,by+38),s1)
    d.text((x0,330),'1x: vorige | nieuw (licht / donker)',fill=(0,0,0))
    for i,m in enumerate(refs):
        b=big(G+m+'/anim_front.png'); V.paste(b,(10+i*522,640)); d.text((14+i*522,620),m+' (Gen 3)',fill=(0,0,0))
    V.save(dst+'/vel.png')
    diff=Counter((a.getpixel((x,y)),im.getpixel((x,y))) for x in range(64) for y in range(64) if a.getpixel((x,y))!=im.getpixel((x,y)))
    print(dict(cnt),sum(cnt.values()),dict(diff)); print('masker + omlijning identiek')
    W=Image.new('RGB',(2*480+12,480),(255,255,255))
    for i,f in enumerate([src,dst+'/A0.png']):
        c=Image.open(f).convert('RGBA').crop((0,24,48,64)).resize((480,400),0); W.paste(c,(i*492,0),c)
    W.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad/crop_'+dst.split('/')[-1]+'.png')
