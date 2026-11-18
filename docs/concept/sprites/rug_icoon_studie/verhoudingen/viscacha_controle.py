"""Past de rekenregels (data/samenvatting.json, groep zijaanzicht) toe op de viscacha-front en vergelijkt met icon_a2_af.
python3 viscacha_controle.py  -> tabel op het scherm + vel_viscacha.png (front 4x | icoon 8x met voorspelde kop en oog)"""
import json,numpy as np
from PIL import Image,ImageDraw
V='../../viscacha/'
def emb(p,n,w):
    im=Image.open(p); q=im.getpalette()[:48]; P=[tuple(q[3*k:3*k+3]) for k in range(16)]
    ix=np.array(im)[:n,:w]; o=np.zeros(ix.shape+(4,),np.uint8)
    for k in range(1,16): o[ix==k]=P[k]+(255,)
    return o
F=emb(V+'af/viscacha.png',64,64); I=emb(V+'icoon/onderdelen/icon_a2_af.png',32,32)
# punten, zelfde afspraken als punten.py (pixelindexen). Front gecontroleerd tegen gelijkenis.py FRONT['viscacha'] (zie STUDIE_VERHOUDINGEN.md)
VF=dict(kop=[7,23,24,39],oog=[16,30,4,3],oor=15,romp=[24,50],vp_len=7,ap_len=11,staart=[50,15,62,50],kraag_x=22.5)
VI=dict(kop=[6,13,15,20],oog=[9,16.5,3,2],oor=8,vp_len=3,ap_len=4.5,staart=[21,10,28,24],kraag_x=12.3)
S=json.load(open('data/samenvatting.json'))['zijaanzicht (3/4 of profiel, geen posewissel)']
hoogte=lambda a:(lambda ys:ys.max()-ys.min()+1)(np.nonzero(a[...,3])[0])
Hf,Hi=hoogte(F),hoogte(I); s=S['schaal']['med']; Hp=Hf*s
def pr(naam,fw,regel,huidig):
    q=S[regel]; v=lambda r:fw*s*r
    print(f"{naam:22s} front {fw:5.1f}  voorspeld {v(q['med']):4.1f} (p25-p75 {v(q['p25']):4.1f}-{v(q['p75']):4.1f})  icon_a2_af {huidig:4.1f}")
    return v(q['med'])
print(f"figuurhoogte           front {Hf}  voorspeld {Hp:4.1f} (p25-p75 {Hf*S['schaal']['p25']:.1f}-{Hf*S['schaal']['p75']:.1f})  icon_a2_af {Hi}")
k=VF['kop']; ki=VI['kop']
kb=pr('kopbreedte',k[2]-k[0]+1,'rel_kop_b',ki[2]-ki[0]+1)
kh=pr('kophoogte',k[3]-k[1]+1,'rel_kop_h',ki[3]-ki[1]+1)
pr('oorlengte',k[1]-VF['oor'],'rel_oor',ki[1]-VI['oor'])
pr('oog (wortel b x h)',(VF['oog'][2]*VF['oog'][3])**.5,'rel_oog',(VI['oog'][2]*VI['oog'][3])**.5)
sn=pr('snuit (snuit -> oog)',VF['oog'][0]-k[0]+.5,'rel_snuit',VI['oog'][0]-ki[0]+.5)
pr('voorpoot',VF['vp_len'],'rel_vp',VI['vp_len'])
pr('achterpoot',VF['ap_len'],'rel_ap',VI['ap_len'])
pr('staart',max(VF['staart'][2]-VF['staart'][0]+1,VF['staart'][3]-VF['staart'][1]+1),'rel_staart',max(VI['staart'][2]-VI['staart'][0]+1,VI['staart'][3]-VI['staart'][1]+1))
pr('lijf',VF['romp'][1]-VF['romp'][0]+1,'rel_lijf',float('nan'))
oh=(VF['oog'][0]-k[0])/(k[2]-k[0]); ov=(VF['oog'][1]-k[1])/(k[3]-k[1])
dh,dv=S['d_oog_h'],S['d_oog_v']
# voorspelde oogplek binnen het huidige icoonkopkader, en binnen een kader met de voorspelde breedte vanaf dezelfde snuit
W=ki[2]-ki[0]; Hh=ki[3]-ki[1]
px=lambda h,w:ki[0]+h*w; py=lambda v:ki[1]+v*Hh
print(f"oog horizontaal in kop front {oh:.2f} -> voorspeld {oh+dh['med']:.2f} (p25-p75 {oh+dh['p25']:.2f}-{oh+dh['p75']:.2f}); icon_a2_af {(VI['oog'][0]-ki[0])/W:.2f}")
print(f"oog verticaal in kop   front {ov:.2f} -> voorspeld {ov+dv['med']:.2f} (p25-p75 {ov+dv['p25']:.2f}-{ov+dv['p75']:.2f}); icon_a2_af {(VI['oog'][1]-ki[1])/Hh:.2f}")
print(f"oogmidden x: voorspeld {px(oh+dh['med'],W):.1f} in de huidige kop (breedte {W+1}), {px(oh+dh['med'],kb-1):.1f} bij voorspelde kopbreedte {kb:.1f}; bereik {px(oh+dh['p25'],W):.1f}-{px(oh+dh['p75'],kb-1):.1f}; icon_a2_af {VI['oog'][0]}")
print(f"oogmidden y: voorspeld {py(ov+dv['med']):.1f} (bereik {py(ov+dv['p25']):.1f}-{py(ov+dv['p75']):.1f}); icon_a2_af {VI['oog'][1]}")
print(f"via snuitlengte: oogmidden x = snuit {ki[0]} + {sn:.1f} - 0.5 = {ki[0]+sn-.5:.1f}")
print(f"oog -> kraagmidden: front {VF['kraag_x']-VF['oog'][0]:.1f} px, voorspeld {(VF['kraag_x']-VF['oog'][0])*s*S['rel_kop_b']['med']:.1f}, icon_a2_af {VI['kraag_x']-VI['oog'][0]:.1f}")
# vel
def teken(a,d,Z,pred=None):
    bg=Image.new('RGB',(a.shape[1]*Z,a.shape[0]*Z),(150,210,180)); im=Image.fromarray(a).resize(bg.size,Image.NEAREST); bg.paste(im,(0,0),im)
    g=ImageDraw.Draw(bg); X=lambda v:(v+.5)*Z; k=d['kop']
    g.rectangle([k[0]*Z,k[1]*Z,(k[2]+1)*Z-1,(k[3]+1)*Z-1],outline=(255,0,255),width=2)
    o=d['oog']; g.line([X(o[0])-2*Z,X(o[1]),X(o[0])+2*Z,X(o[1])],fill=(255,0,0),width=2); g.line([X(o[0]),X(o[1])-2*Z,X(o[0]),X(o[1])+2*Z],fill=(255,0,0),width=2)
    g.line([k[0]*Z,d['oor']*Z,(k[2]+1)*Z,d['oor']*Z],fill=(255,60,60))
    if pred:
        x,y,x0,x1,y0,y1=pred; g.rectangle([x0*Z,y0*Z,x1*Z,y1*Z],outline=(0,0,255),width=1)
        g.ellipse([X(x)-Z*.7,X(y)-Z*.7,X(x)+Z*.7,X(y)+Z*.7],outline=(0,0,255),width=3)
    return bg
xp=px(oh+dh['med'],kb-1); yp=py(ov+dv['med'])
A=teken(F,VF,4); B=teken(I,VI,8,(xp,yp,ki[0]+px(oh+dh['p25'],W)-ki[0],px(oh+dh['p75'],kb-1)+1,py(ov+dv['p25']),py(ov+dv['p75'])+1))
img=Image.new('RGB',(A.width+B.width+12,max(A.height,B.height)+40),(255,255,255)); img.paste(A,(0,40)); img.paste(B,(A.width+12,40))
ImageDraw.Draw(img).text((4,4),"viscacha: front 4x | icon_a2_af 8x. Paars = kop, rood kruis = oog nu; blauwe cirkel = voorspeld oogmidden, blauw kader = p25-p75",fill=0)
img.save('vel_viscacha.png')
