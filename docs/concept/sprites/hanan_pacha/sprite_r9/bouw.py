# r9: klauwen in perspectief (SPRITE_KERN: verre poot hoger en achter, in schaduwtint). Nabije klauw (links in beeld) =
# Fearow-linkervoet zoals r8 fearow. Verre klauw (rechts), alleen hele-klauw-bewerkingen:
#  A = Fearow-rechtervoet gespiegeld, 1 px hoger, schaduwtint;  B = idem niet gespiegeld;
#  C = Fearow-rechtervoet uit frame 2 (andere teenstand), 1 px hoger, schaduwtint.
# Verre klauw ligt achter de dij (witte dijpixels en hun lijnen worden niet overschreven) en achter de nabije klauw.
# Opbouw vanaf r7 met dezelfde regels als r8; buiten de klauwzone (X 16-41, Y 47-57) pixeldiff 0 met r8 fearow (assert).
import numpy as np; from PIL import Image, ImageDraw
G='../../../../../graphics/pokemon/'
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
a=np.array(Image.open(G+'fearow/anim_front_gba.png'))
fpal=[tuple(int(v) for v in l.split()) for l in open(G+'fearow/normal_gba.pal').read().split('\n')[3:19]]
LICHT={5:1,7:10,8:9,13:8,4:1,3:7}          # zoals r8
SCHADUW={5:1,7:9,8:8,13:8,4:1,3:14}        # licht -> midden, midden -> schaduw, klauwpunt ivoorschaduw
NABIJ=((16,57,24,63),(20,57),(26,49),False,LICHT,0)
VER={'A':((27,57,35,63),(31,57),(35,48),True,SCHADUW,0),
     'B':((27,57,35,63),(31,57),(35,48),False,SCHADUW,0),
     'C':((22,51,30,57),(27,51),(35,48),False,SCHADUW,64)}
r7=np.array(Image.open('../sprite_r7/sprite.png')).astype(int)
r8=np.array(Image.open('../sprite_r8/sprite_fearow.png')).astype(int)
OUD=np.zeros((64,64),bool); OUD[49:53,21:39]=True; OUD&=r7>0; OUD[49:51,27:31]=False
DIJ=np.isin(r7,[6,7])&(np.arange(64)[:,None]<=50)       # witte dijveren (en de klauwpunten van r7 vallen eronder weg)
DIJ[49:53,21:39]&=~OUD[49:53,21:39]
Z=np.zeros((64,64),bool); Z[47:58,16:42]=True
def plak(o,bez,spec,achter):
    (x0,y0,x1,y1),(ax,ay),(dx,dy),spiegel,km,fo=spec
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            k=a[y+fo,x]
            if k==0 or k not in km: continue
            xs=(x0+x1-x) if spiegel else x; axs=(x0+x1-ax) if spiegel else ax
            Y,X=y-ay+dy,xs-axs+dx
            if not(0<=Y<64 and 0<=X<64): continue
            if achter is not None and (achter[Y,X] or (DIJ[Y,X]) or (o[Y,X]==1 and Y<=48)): continue
            o[Y,X]=km[k]; bez[Y,X]=True
uit={}
for var,spec in VER.items():
    o=r7.copy(); nabij=np.zeros((64,64),bool); ver=np.zeros((64,64),bool)
    plak(o,nabij,NABIJ,None)
    plak(o,ver,spec,nabij)
    nieuw=nabij|ver
    for Y,X in zip(*np.where(OUD&~nieuw)): o[Y,X]=r7[53,X] if X>=26 and r7[53,X]>0 else 0
    for Y,X in zip(*np.where(nieuw)):
        if o[Y,X]==1: continue
        for ddy,ddx in ((1,0),(0,1),(0,-1),(-1,0)):
            YY,XX=Y+ddy,X+ddx
            if 0<=YY<64 and 0<=XX<64 and not nieuw[YY,XX] and o[YY,XX] not in (0,1) and YY>=51: o[YY,XX]=1
    for Y,X in zip(*np.where(Z&(o>0))):
        if all(not(0<=Y+p<64 and 0<=X+q<64) or o[Y+p,X+q]==0 for p in (-1,0,1) for q in (-1,0,1) if p or q): o[Y,X]=0
    assert not ((o!=r8)&~Z).any()
    uit[var]=o; opslaan(o,'sprite_%s.png'%var); np.save('sprite_%s.npy'%var,o)
    print(var,'px anders dan r8 fearow:',int((o!=r8).sum()),'| nabij',int(nabij.sum()),'ver',int(ver.sum()),'| kleuren',len(set(o.ravel()))-1)
def rgb(o,bg=(240,240,236)):
    x=np.array(PAL,'uint8')[o]; x[o==0]=bg; return Image.fromarray(x)
V=Image.new('RGB',(1600,3*560),'white'); d=ImageDraw.Draw(V)
for i,(var,o) in enumerate(uit.items()):
    y=i*560; d.text((2,y),'r9 %s: klauwen 16x | geheel 8x | 1x/2x licht en donker'%var,fill=(0,0,0))
    V.paste(rgb(o).crop((17,44,43,58)).resize((26*16,14*16),Image.NEAREST),(0,y+14))
    V.paste(rgb(o).resize((512,512),Image.NEAREST),(430,y+14)); x=960
    for bg in ((240,240,236),(40,40,56)):
        for s in (1,2): V.paste(rgb(o,bg).resize((64*s,64*s),Image.NEAREST),(x,y+14)); x+=64*s+10
V.save('vel.png')
