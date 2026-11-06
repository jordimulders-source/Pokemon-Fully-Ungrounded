"""Overtrek bekrand op de gespiegelde leidraad (punten met de hand afgelezen op 3x met raster, 10-px-raster in fotocoördinaten).
Bovenrand: snavelpunt/haak linksboven -> onder het oog -> mondhoek; nabije kaakrand omlaag naar de punt; verre kaakrand terug omhoog."""
import json, math
from PIL import Image, ImageDraw
# (X,Y) in de 3x-uitsnede (x0=100,y0=180); omrekenen naar foto: x=100+X/3, y=180+Y/3
P3=[(72,200),(110,200),(160,203),(210,206),(260,208),(310,212),(360,222),(410,238),(460,258),(510,280),(560,302),(605,322),(640,345),
    (648,380),(645,420),(638,465),(628,510),(612,555),(590,595),(560,630),(528,662),(497,695),(468,727),(440,760),(415,792),(395,825),
    (372,822),(345,800),(318,772),(292,740),(268,705),(248,668),(232,630),(218,590),(206,550),(192,510),(176,470),(160,432),(146,398),
    (120,378),(95,362),(80,340),(72,305),(70,270),(70,235)]
P=[(100+X/3,180+Y/3) for X,Y in P3]
OOG=(100+485/3,180+130/3,29,27)   # midden x,y + straal x,y
KOP=[(125,236),(128,215),(140,190),(160,160),(185,138),(215,122),(250,112),(285,113),(320,124),(350,142),(375,168),(392,198),(402,232),(408,268)]
def cr(pts,n=8,closed=True):
    out=[]; L=len(pts)
    rng=range(L) if closed else range(L-1)
    for i in rng:
        p0,p1,p2,p3=[pts[(i+k)%L] if closed else pts[min(max(i+k,0),L-1)] for k in (-1,0,1,2)]
        for t in [j/n for j in range(n)]:
            t2,t3=t*t,t*t*t
            out.append(tuple(0.5*((2*p1[a])+(-p0[a]+p2[a])*t+(2*p0[a]-5*p1[a]+4*p2[a]-p3[a])*t2+(-p0[a]+3*p1[a]-3*p2[a]+p3[a])*t3) for a in (0,1)))
    return out
if __name__=='__main__':
    json.dump({'bekrand':P,'oog':OOG,'kop':KOP},open('overtrek.json','w'),indent=1)
    foto=Image.open('leidraad_gespiegeld.png').convert('RGB')
    S=800/720; F=foto.resize((int(640*S),800),Image.LANCZOS)
    def draw(im,col_bek=(0,255,255),bg=False):
        d=ImageDraw.Draw(im)
        k=[(x*S,y*S) for x,y in cr(KOP,closed=False)]; d.line(k,fill=(255,200,0),width=2)
        ox,oy,rx,ry=OOG; d.ellipse([(ox-rx)*S,(oy-ry)*S,(ox+rx)*S,(oy+ry)*S],outline=(255,60,60),width=3)
        d.line([((ox-4)*S,oy*S),((ox+4)*S,oy*S)],fill=(255,60,60),width=2); d.line([(ox*S,(oy-4)*S),(ox*S,(oy+4)*S)],fill=(255,60,60),width=2)
        b=[(x*S,y*S) for x,y in cr(P)]; d.line(b+[b[0]],fill=col_bek,width=3)
    a=F.copy(); draw(a)
    w=Image.new('RGB',F.size,(255,255,255)); draw(w,col_bek=(0,120,200))
    W=Image.new('RGB',(F.size[0]*2+20,800),(235,235,240)); W.paste(a,(0,0)); W.paste(w,(F.size[0]+20,0))
    d=ImageDraw.Draw(W); d.text((10,780),'leidraad gespiegeld + overtrek bekrand (cyaan), oog (rood), kop (geel)',fill=(255,255,255)); d.text((F.size[0]+30,780),'zelfde lijnen op wit',fill=(0,0,0))
    W.save('bekrand_op_foto.png')
    # controle close-up 3x
    x0,y0,x1,y1=100,180,360,480
    c=foto.crop((x0,y0,x1,y1)).resize(((x1-x0)*3,(y1-y0)*3),Image.LANCZOS); d=ImageDraw.Draw(c)
    b=[((x-x0)*3,(y-y0)*3) for x,y in cr(P)]; d.line(b+[b[0]],fill=(0,255,255),width=2)
    ox,oy,rx,ry=OOG; d.ellipse([(ox-rx-x0)*3,(oy-ry-y0)*3,(ox+rx-x0)*3,(oy+ry-y0)*3],outline=(255,60,60),width=2)
    c.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/279ed44b-aa1d-54e2-8396-02fa8e081036/scratchpad/r3/ctrl.png')
    print(len(P),'punten')
