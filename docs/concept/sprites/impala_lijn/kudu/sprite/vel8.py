# Ronde 8: bouwt r8/kudu_r8{A,B,C}.png (+_8x), r8/vel.png, r8/telling.txt, r8/bronnen.txt. Oog = K4 (Jordi), 1-op-1 uit r6/kudu_r6_oogK4.png.
import r8, r8lib as L, numpy as np, collections
from PIL import Image, ImageDraw
K4=np.array(Image.open('r6/kudu_r6_oogK4.png').convert('RGB')); RGB2={v:k for k,v in L.PAL.items() if k!='.'}
OOG={(x,y) for x in range(9,15) for y in range(21,27)}   # ruim oogvlak (beeld x15-20, y21-26)
def met_oog(g):
    g=[list(r) for r in g]
    for x,y in OOG:
        c=tuple(int(v) for v in K4[y,x+6]); 
        if c in RGB2: g[y][x]=RGB2[c]
    return [''.join(r) for r in g]
REF=met_oog(L.R6)   # r6 met oog K4 = uitgangspunt
COL={'A_UP2':(230,40,40),'A_UP1':(230,40,40),'A_LEFT':(40,90,230),'A_DOWN':(20,170,60),'A_RIGHT':(255,140,0),
     'A_BUMP':(220,0,220),'G_UP':(0,190,210),'G_LEFT':(130,60,200),'G_DOWN':(150,90,40)}
NAAM={v:k for k,v in vars(r8).items() if isinstance(v,tuple) and len(v)==5 and v[0] in('arcanine','growlithe')}
def src_img(n):
    a=np.array(Image.open(L.GP+n+'/anim_front_gba.png'))[:64]
    pal=[tuple(map(int,l.split())) for l in open(L.GP+n+'/normal_gba.pal').read().split('\n')[3:19]]
    im=Image.new('RGB',(64,64),'white')
    for y in range(64):
        for x in range(64):
            if a[y,x]: im.putpixel((x,y),pal[a[y,x]])
    return im
out={}; tel=open('r8/telling.txt','w'); bron=open('r8/bronnen.txt','w')
for k,(titel,stamps) in r8.VARIANTEN.items():
    v,g=r8.bouw(k); g=met_oog(g)
    diff={(x,y) for y in range(L.H) for x in range(L.W) if g[y][x]!=REF[y][x]}
    buiten=diff-L.ZONE; oog=diff&OOG
    rech=L.rechte(g,L.ZONE); kl=len(set(c for r in g for c in r))
    L.png(g,'r8/kudu_r8%s.png'%k); L.rgba8(g).resize((512,512),0).save('r8/kudu_r8%s_8x.png'%k)
    soort=collections.Counter(b[0].split(' (')[0].split(':')[0] if b else '?' for p,b in v.bron.items() if p in diff)
    tel.write('Variant %s (%s): %d px anders dan r6+oog K4; buiten de manenzone: %d %s; in het oogvlak: %d; rechte lijnstukken >3 px in de manen: %s; kleuren incl. transparant: %d\n'%(k,titel,len(diff),len(buiten),sorted(buiten),len(oog),rech or 'geen',kl))
    bron.write('== Variant %s: %s\n'%(k,titel))
    for p in sorted(diff,key=lambda p:(p[1],p[0])):
        b=v.bron.get(p,('?',)); bron.write('  (%d,%d) %s -> %s  %s\n'%(p[0],p[1],REF[p[1]][p[0]],g[p[1]][p[0]],' '.join(map(str,b))))
    out[k]=(titel,stamps,g)
    print(k,len(diff),len(buiten),len(oog),rech,kl)
tel.close(); bron.close()
# ---------- vel
Z=512; S8=8; ARCI=src_img('arcanine'); GROI=src_img('growlithe')
rows=len(out); RH=Z+60+150
V=Image.new('RGB',(Z*3+60,rows*RH+40),'white'); d=ImageDraw.Draw(V)
d.text((10,8),'Kudu r8 - manen: een vorm (model A3), los van het lijf, rand licht gerafeld met randstukken 1-op-1 uit Arcanine/Growlithe (gba). Oog K4. Kaders: zelfde kleur = zelfde bronstuk.',fill=(0,0,0))
for i,(k,(titel,stamps,g)) in enumerate(out.items()):
    y0=40+i*RH
    d.text((10,y0),'Variant %s: %s'%(k,titel),fill=(0,0,0))
    ku=L.rgba8(g).resize((Z,Z),0); dk=ImageDraw.Draw(ku)
    a8=ARCI.resize((Z,Z),0); da=ImageDraw.Draw(a8); g8=GROI.resize((Z,Z),0); dg=ImageDraw.Draw(g8)
    # vlak
    vx0,vy0,vx1,vy1,dx,dy=r8.VELD[1:]
    da.rectangle([vx0*S8,vy0*S8,(vx1+1)*S8-1,(vy1+1)*S8-1],outline=(150,150,150),width=2)
    dk.rectangle([(dx+6)*S8,dy*S8,(dx+6+vx1-vx0+1)*S8-1,(dy+vy1-vy0+1)*S8-1],outline=(150,150,150),width=2)
    gebruikt_g=False
    for n,st in enumerate(stamps,1):
        sn,tx,ty=st[0],st[1],st[2]; c=COL[NAAM[sn]]; naam,x0,y0s,x1,y1=sn
        dd=da if naam=='arcanine' else dg; gebruikt_g|=naam=='growlithe'
        dd.rectangle([x0*S8,y0s*S8,(x1+1)*S8-1,(y1+1)*S8-1],outline=c,width=3)
        dk.rectangle([(tx+6)*S8,ty*S8,(tx+6+x1-x0+1)*S8-1,(ty+y1-y0s+1)*S8-1],outline=c,width=2)
        dk.text(((tx+6)*S8+2,ty*S8+1),str(n),fill=c)
    V.paste(ku,(10,y0+14)); d.text((10+Z-150,y0+14+Z+2),'kudu r8%s 8x'%k,fill=(0,0,0))
    V.paste(a8,(20+Z,y0+14)); d.text((20+Z,y0+14+Z+2),'Arcanine gba 8x (grijs = vlak)',fill=(0,0,0))
    if gebruikt_g:
        V.paste(g8,(30+2*Z,y0+14)); d.text((30+2*Z,y0+14+Z+2),'Growlithe gba 8x',fill=(0,0,0))
    else:
        d.text((30+2*Z,y0+30),'Growlithe niet gebruikt',fill=(120,120,120))
    yb=y0+14+Z+18
    for j,bg in enumerate([(255,255,255),(40,44,52)]):
        V.paste(Image.new('RGB',(220,110),bg),(10+j*230,yb))
        V.paste(L.rgba8(g,bg),(20+j*230,yb+30)); V.paste(L.rgba8(L.R7,bg),(100+j*230,yb+30))
    d.text((480,yb+20),'1x op licht en donker: r8%s | r7'%k,fill=(0,0,0))
    leg=['%d %s <- %s (%d,%d)-(%d,%d)'%(n,st[3],st[0][0],*st[0][1:]) for n,st in enumerate(stamps,1)]
    for j,t in enumerate(leg): d.text((700+(j//8)*420,yb+j%8*13),t,fill=COL[NAAM[stamps[j][0]]])
V.save('r8/vel.png')
