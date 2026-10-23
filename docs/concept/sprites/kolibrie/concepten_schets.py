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
def body_end(d,ghost=False,velvet=False):
    V=GBg
    if velvet:
        poly(d,[(28,20),(26,4),(31,2),(33,18)],(20,40,50,255)); ell(d,29,26,9,8,VI)
        poly(d,[(31,22),(44,2),(52,6),(46,16),(37,24)],(46,44,60,255)); poly(d,[(31,22),(36,13),(39,18),(35,24)],TQ,None); ell(d,44,8,1.5,1.5,OR,None)
        line(d,[(36,20),(46,6)],(20,20,30,255),0.6)
        ell(d,18,18,7,7,VK); ell(d,17,13,3,1.6,VI,None); line(d,[(12,17),(0,10)],OL,1.1)
        ell(d,16,17,1.6,2,(250,250,250,255),None); ell(d,16,17,0.8,1.2,(20,20,30,255),None)
        return
    poly(d,[(28,20),(26,4),(31,2),(33,18)],GBd)                    # verre vleugel (V)
    ell(d,29,26,9,8,V)
    if ghost: poly(d,[(24,30),(36,32),(33,40),(30,37),(27,41)],(246,244,238,150))
    ell(d,27,29,6,5,WH,None); line(d,[(27,29),(28,34)],RU,1.0); kraag(d,22,24,4)
    poly(d,[(31,22),(44,2),(52,6),(46,16),(37,24)],GB)               # nabije vleugel (V, waaier)
    line(d,[(36,20),(46,6)],GBd,0.6); line(d,[(38,22),(49,10)],GBd,0.6)
    ell(d,18,18,7,7,V); line(d,[(12,17),(0,10)],OL,1.1)              # lange dunne snavel schuin omhoog
    ell(d,16,17,1.6,2,(20,20,30,255),None); ell(d,19,16,1,1,WH,None)
def body_f1(d):
    ell(d,32,36,11,10,GBg); ell(d,30,41,6,4,WH,None); kraag(d,25,38,3)
    poly(d,[(34,30),(40,20),(45,22),(40,32)],GB); poly(d,[(30,28),(31,22),(34,22),(34,28)],GBd)
    line(d,[(22,35),(14,31)],OL,1.1); ell(d,27,33,1.6,2,(20,20,30,255),None)
IR=[EM,(40,170,170,255),BL,MG,(220,180,230,220),(246,244,238,150)]
# ---- A: iriserend -> rook
def A_end():
    im,d=canvas()
    ribbon(d,[(34,33),(38,40),(42,47),(45,53),(47,58),(48,63)],IR)
    ribbon(d,[(35,33),(41,38),(47,44),(53,48),(58,52),(63,54)],IR)
    body_end(d,ghost=True); return im
def A_f1():
    im,d=canvas(); ribbon(d,[(38,42),(42,48),(45,53),(47,57)],IR[2:],1.3); body_f1(d); return im
# ---- B: donkere staart met zielenringen (nacht/torpor), punten dageraad
def B_end():
    im,d=canvas()
    t1=[(34,33),(38,41),(42,49),(45,56),(47,63)]; t2=[(35,33),(42,39),(49,45),(56,49),(63,52)]
    ribbon(d,t1,[VK,VI,VI,TQ],2.2); ribbon(d,t2,[VK,VI,VI,TQ],2.2)
    for x,y in [(39,43),(43,51),(44,41),(51,46)]: ell(d,x,y,1.6,1.6,VK,WH,K)
    body_end(d,velvet=True); return im
def B_f1():
    im,d=canvas(); ribbon(d,[(38,42),(42,48),(45,54)],[VK,VI,TQ],1.8); ell(d,42,48,1.4,1.4,VK,WH,K)
    ell(d,32,36,11,10,VK); ell(d,33,41,7,4,VI,None); poly(d,[(34,30),(40,20),(45,22),(40,32)],(46,44,60,255)); poly(d,[(34,30),(37,25),(39,28),(37,31)],TQ,None)
    line(d,[(22,35),(14,31)],OL,1.1); ell(d,27,33,1.8,2.2,(250,250,250,255),None); ell(d,27,33,0.9,1.3,(20,20,30,255),None); return im
# ---- C: nabeelden (Ghost/Flying)
def C_end():
    im,d=canvas()
    for off,a in ((10,110),(5,170)):  # bleke kopieen van staart en vleugel
        c=(220,230,250,a)
        line(d,[(34+off,33-off/2),(40+off,44-off/2),(46+off,56-off/2)],c,1.6)
        poly(d,[(31+off,22-off/2),(44+off,2-off/2),(52+off,6-off/2),(37+off,24-off/2)],(lerp(MG,BL,off/8)[:3]+(a,)),None)
    ribbon(d,[(34,33),(40,44),(46,56),(49,63)],[EM,BL,MG],1.6)
    ribbon(d,[(35,33),(43,42),(51,52),(56,60)],[EM,BL,MG],1.6)
    body_end(d); return im
def C_f1():
    im,d=canvas()
    poly(d,[(38,28),(44,18),(49,20),(43,30)],(200,180,240,90),None)
    ribbon(d,[(38,42),(42,48),(45,53)],[EM,BL],1.3); body_f1(d); return im
def spr(n):
    f=G+n+'/anim_front.png'; f=f if os.path.exists(f) else G+n+'/front.png'
    s=Image.open(f); src=s.crop((0,0,64,64)); r=src.convert('RGBA'); px=r.load(); sp=src.load()
    for y in range(64):
        for x in range(64):
            if sp[x,y]==0: px[x,y]=(0,0,0,0)
    return r.resize((B,B),Image.NEAREST)
rows=[("A  Regenboogrook: staart iriserend groen>blauw>magenta, vervaagt tot rook - Ghost/Fairy - 3 fasen",A_end,A_f1,["cutiefly","ribombee","flutter_mane"]),
      ("B  Zielenringen, fluweelpalet (Boissonneaua): zwart>violet>blauwgroen, witte zielenringen op de staart - Ghost/Fairy of Flying - 2 fasen",B_end,B_f1,["natu","taillow","misdreavus"]),
      ("C  Nabeeld (ajayu): staart en vleugels laten bleke kopieen achter - Ghost/Flying - 2 fasen",C_end,C_f1,["ninjask","fletchling","swellow"])]
font=ImageFont.load_default(); HDR=22; LB=16; GAP=8; TOP=36
W=5*(B+GAP)+GAP; H=TOP+len(rows)*(HDR+B+LB)+GAP
out=Image.new('RGB',(W,H),(236,236,230)); d=ImageDraw.Draw(out)
d.text((GAP,6),"Vast voor alle drie (Jordi): hillstar-lijf/palet (grijsbruin, wit, smaragdgroene kraag, roeststreep) + lange dunne snavel + zwevende V-vleugels + lange gevorkte staart met mystiek patroon",fill=(10,10,10),font=font)
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
