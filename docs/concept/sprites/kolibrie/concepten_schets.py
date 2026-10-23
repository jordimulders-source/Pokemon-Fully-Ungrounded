from PIL import Image, ImageDraw, ImageFont
import os,sys
K=4; B=64*K; G='/home/user/projectgrounded/graphics/pokemon/'
OL=(40,30,60,255)
GB=(138,124,112,255); GBd=(98,86,78,255); GBg=(186,178,168,255); WH=(246,244,238,255)
EM=(40,190,120,255); RIM=(28,36,70,255); RU=(184,101,58,255); MG=(200,70,190,255); BL=(60,150,220,255); NV=(44,40,80,255)
def P(pts): return [(x*K,y*K) for x,y in pts]
def ell(d,cx,cy,rx,ry,fill,ol=OL,w=K): d.ellipse([(cx-rx)*K,(cy-ry)*K,(cx+rx)*K,(cy+ry)*K],fill=fill,outline=ol,width=w)
def poly(d,pts,fill,ol=OL,w=K): d.polygon(P(pts),fill=fill,outline=ol,width=w)
def line(d,pts,fill,w=2): d.line(P(pts),fill=fill,width=max(1,int(w*K)),joint='curve')
def canvas(): im=Image.new('RGBA',(B,B),(0,0,0,0)); return im,ImageDraw.Draw(im)
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(4))
def ribbon(d,pts,cols,w=1.6):
    # band met kleurverloop langs de segmenten
    n=len(pts)-1
    for i in range(n):
        line(d,[pts[i],pts[i+1]],OL,w+1.0)
    for i in range(n):
        line(d,[pts[i],pts[i+1]],cols[min(i,len(cols)-1)],w)
def kraag(d,cx,cy,r): ell(d,cx,cy+1,r+1,r*0.8,RIM,None); ell(d,cx,cy,r,r*0.75,EM,None)
VK=(30,26,40,255); VI=(110,70,190,255); TQ=(40,150,150,255); OR=(230,130,50,255)
# Pose (Jordi): hangend/zwevend met de vleugels wijd naar de kijker (Butterfree, Zubat, Zapdos, Moltres);
# lijf licht 3/4, kop iets links, snavel schuin links-voor, staart hangt eronder.
LW=[(27,22),(14,8),(3,4),(1,12),(6,22),(16,30),(26,30)]     # nabije vleugel (groter)
RW=[(37,22),(48,10),(58,8),(60,15),(54,24),(44,30),(37,29)]  # verre vleugel (kleiner, hoger)
def wings(d,near,far,ribs):
    poly(d,RW,far); poly(d,LW,near)
    for q in ((25,24),(18,15)),((24,27),(10,20)): line(d,list(q),ribs,0.6)
    line(d,[(40,24),(52,14)],ribs,0.5)
def body_end(d,ghost=False,velvet=False):
    if velvet:
        wings(d,(46,44,60,255),(30,30,44,255),(20,20,30,255))
        poly(d,[(27,22),(22,18),(20,24),(26,27)],TQ,None); ell(d,4,10,1.4,1.4,OR,None)
        ell(d,32,29,7,9,VI); ell(d,28,17,7,7,VK); ell(d,27,12,3,1.5,VI,None)
        line(d,[(22,19),(4,25)],(250,250,246,255),2.2); line(d,[(22,19),(4,25)],(20,20,30,255),0.9); ell(d,26,17,1.6,2,(250,250,250,255),None); ell(d,26,17,0.8,1.2,(20,20,30,255),None)
        return
    wings(d,GB,GBd,GBd)
    ell(d,32,29,7,9,GBg)
    if ghost: poly(d,[(27,34),(37,34),(35,40),(32,37),(29,40)],(246,244,238,150))
    ell(d,32,30,5,6,WH,None); line(d,[(32,27),(32,35)],RU,1.0); kraag(d,30,23,4)
    ell(d,28,17,7,7,GBg); line(d,[(22,19),(4,25)],(250,250,246,255),2.2); line(d,[(22,19),(4,25)],(20,20,30,255),0.9)
    ell(d,26,17,1.6,2,(20,20,30,255),None); ell(d,28,16,0.9,0.9,WH,None)
def body_f1(d,velvet=False):
    c1,c2,bel=((46,44,60,255),(30,30,44,255),VI) if velvet else (GB,GBd,WH)
    poly(d,[(36,34),(46,24),(52,26),(48,34),(40,38)],c2); poly(d,[(28,34),(18,24),(12,26),(15,36),(24,38)],c1)
    ell(d,32,36,10,9,VK if velvet else GBg); ell(d,33,41,6,3.5,bel,None)
    if not velvet: kraag(d,30,38.5,3)
    line(d,[(24,34),(15,37)],(250,250,246,255),2.0); line(d,[(24,34),(15,37)],(20,20,30,255),0.9)
    if velvet: ell(d,28,33,1.8,2.2,(250,250,250,255),None); ell(d,28,33,0.9,1.3,(20,20,30,255),None)
    else: ell(d,28,33,1.6,2,(20,20,30,255),None)
IR=[EM,(40,170,170,255),BL,MG,(220,180,230,220),(246,244,238,150)]
T1=[(31,37),(30,43),(29,49),(28,54),(28,59),(27,63)]; T2=[(33,37),(35,43),(37,49),(38,54),(39,59),(41,63)]
def A_end():
    im,d=canvas(); ribbon(d,T1,IR); ribbon(d,T2,IR); body_end(d,ghost=True); return im
def A_f1():
    im,d=canvas(); ribbon(d,[(32,44),(33,50),(33,55),(34,60)],IR[2:],1.3); body_f1(d); return im
def B_end():
    im,d=canvas(); cols=[VK,VI,VI,VI,TQ]
    ribbon(d,T1,cols,2.2); ribbon(d,T2,cols,2.2)
    for x,y in [(30,45),(29,53),(36,46),(38,54)]: ell(d,x,y,1.6,1.6,VK,WH,K)
    body_end(d,velvet=True); return im
def B_f1():
    im,d=canvas(); ribbon(d,[(32,44),(33,50),(33,55),(34,60)],[VK,VI,TQ],1.8); ell(d,33,52,1.4,1.4,VK,WH,K); body_f1(d,velvet=True); return im
def C_end():
    im,d=canvas()
    for dy,a in ((-8,110),(-4,170)):   # nabeelden van de vleugels (frame 2 schuift)
        poly(d,[(x,y+dy) for x,y in LW],(MG[:3]+(a,)),None); poly(d,[(x,y+dy) for x,y in RW],(BL[:3]+(a,)),None)
    for dx,a in ((6,110),(3,170)):
        line(d,[(x+dx,y) for x,y in T2],(220,230,250,a),1.4)
    ribbon(d,T1,[EM,EM,BL,BL,MG],1.6); ribbon(d,T2,[EM,EM,BL,BL,MG],1.6)
    body_end(d); return im
def C_f1():
    im,d=canvas()
    poly(d,[(36,30),(46,20),(52,22)],(BL[:3]+(120,)),None); poly(d,[(28,30),(18,20),(12,22)],(MG[:3]+(120,)),None)
    ribbon(d,[(32,44),(33,50),(33,55),(34,60)],[EM,BL,MG],1.3); body_f1(d); return im
def spr(n):
    f=G+n+'/anim_front.png'; f=f if os.path.exists(f) else G+n+'/front.png'
    s=Image.open(f); src=s.crop((0,0,64,64)); r=src.convert('RGBA'); px=r.load(); sp=src.load()
    for y in range(64):
        for x in range(64):
            if sp[x,y]==0: px[x,y]=(0,0,0,0)
    return r.resize((B,B),Image.NEAREST)
rows=[("A  Regenboogrook: staart iriserend groen>blauw>magenta, vervaagt tot rook - Ghost/Fairy - 3 fasen",A_end,A_f1,["butterfree","moltres","flutter_mane"]),
      ("B  Zielenringen, fluweelpalet (Boissonneaua): zwart>violet>blauwgroen, witte zielenringen op de staart - Ghost/Fairy of Flying - 2 fasen",B_end,B_f1,["zubat","zapdos","misdreavus"]),
      ("C  Nabeeld (ajayu): staart en vleugels laten bleke kopieen achter - Ghost/Flying - 2 fasen",C_end,C_f1,["ninjask","zapdos","cutiefly"])]
font=ImageFont.load_default(); HDR=22; LB=16; GAP=8; TOP=36
W=5*(B+GAP)+GAP; H=TOP+len(rows)*(HDR+B+LB)+GAP
out=Image.new('RGB',(W,H),(236,236,230)); d=ImageDraw.Draw(out)
d.text((GAP,6),"Vast voor alle drie (Jordi): hillstar-lijf/palet (grijsbruin, wit, smaragdgroene kraag, roeststreep) + lange dunne snavel + zwevende V-vleugels + lange gevorkte staart met mystiek patroon; pose: hangend met vleugels wijd naar de kijker (Butterfree/Zubat/Zapdos/Moltres)",fill=(10,10,10),font=font)
d.text((GAP,20),"Schetsen in een 64-box (raster = 16 px), geen pixelsprite. Skelet-sprites 4x.",fill=(80,80,80),font=font)
y=TOP
for title,fe,f1,sk in rows:
    d.text((GAP,y+6),title,fill=(10,10,10),font=font); y+=HDR
    items=[(fe(),"eindvorm"),(f1(),"fase 1 (afgeleid)")]+[(spr(n),"skelet: "+n) for n in sk]
    for i,(im,l) in enumerate(items):
        x=GAP+i*(B+GAP); d.rectangle([x,y,x+B-1,y+B-1],fill=(250,250,246),outline=(200,200,195))
        if i<2:
            for g in range(16,64,16): d.line([(x+g*K,y),(x+g*K,y+B-1)],fill=(236,236,230)); d.line([(x,y+g*K),(x+B-1,y+g*K)],fill=(236,236,230))
        out.paste(im,(x,y),im); d.text((x+2,y+B+2),l,fill=(60,60,60),font=font)
    y+=B+LB
out.save(sys.argv[1])
