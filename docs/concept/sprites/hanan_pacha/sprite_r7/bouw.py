# r7 = r6 C + per-pixelcorrecties in de klauwzones naar wat het model r7 daar heeft (natief 2x2-blok per spritepixel via
# sprite_r4/kaart.py; notatie 'boven/onder' = de twee natieve rijen; # lijn, W/w wit, c ivoor, G/s goud, d donker goud).
# Buiten de klauwzones pixeldiff 0 met r6 C (assert). Kleuren C, klauwpunten ivoor, omlijning tegen de staart blijven.
import numpy as np; from PIL import Image, ImageDraw
PAL=[(152,208,160),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),
 (128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def opslaan(o,pad):
    im=Image.new('P',(64,64)); flat=[x for c in PAL for x in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.putdata([int(v) for v in o.ravel()]); im.save(pad,transparency=0)
r6=np.array(Image.open('../sprite_r6/sprite_C.png')).astype(int)
WISSEL=[ # (X,Y), nieuw, modelreden
 ((22,51),7,'linkerklauw: model "c#/w#" = ivoren klauwpunt onderaan de teen (vormt met (23,51) een punt van 2 px)'),
 ((28,49),1,'model "w#/##" = lijn (onderrand van de dij), geen klauw'),
 ((29,49),6,'model "WW/WW" = witte beenveren van de dij (schaduwtint 6 zoals de dij erboven), geen lijn'),
 ((29,50),6,'model "WW/WW" = zelfde beenveren, hoort bij de dij en niet bij een klauw (was los ivoor)'),
 ((33,50),7,'rechterklauw: model "Ws/Ws" = ivoren klauwpunt'),
 ((33,51),9,'model "#s/ss" = teen (goud), doorlopende streng van de voet naar beneden'),
 ((33,52),9,'model "sw/ss" = teen loopt door tot de onderkant; breekt de witte balk van 3 px (32-34,52) in twee klauwpunten'),
 ((33,53),1,'omlijning onder de teen tegen de staart (gesloten voorste vorm)'),
]
o=r6.copy(); regels=[]
for (X,Y),k,r in WISSEL:
    assert o[Y,X]>0; regels.append('(%d,%d) %d -> %d: %s'%(X,Y,o[Y,X],k,r)); o[Y,X]=k
Z=np.zeros((64,64),bool); Z[48:54,20:40]=True
assert not ((o!=r6)&~Z).any() and ((o>0)==(r6>0)).all()
opslaan(o,'sprite.png'); np.save('sprite.npy',o); open('wissels.txt','w').write('\n'.join(regels)+'\n')
print('\n'.join(regels)); print('anders dan r6 C:',int((o!=r6).sum()),'kleuren',len(set(o.ravel()))-1)
# vel: per klauw 16x: model (natief in spriteraster) | r6 C | r7 ; + 8x geheel + 1x/2x
import sys; sys.path.insert(0,'../sprite_r4'); from bron import B
def rgb(a,bg=(240,240,236)):
    x=np.array(PAL,'uint8')[a]; x[a==0]=bg; return Image.fromarray(x)
V=Image.new('RGB',(1600,1000),'white'); d=ImageDraw.Draw(V); y=0
for naam,(x0,x1,y0,y1) in (('linkerklauw',(19,32,46,55)),('rechterklauw',(30,41,46,55))):
    w,h=(x1-x0)*16,(y1-y0)*16
    M=Image.fromarray(B[2*y0:2*y1,2*x0:2*x1]).resize((w,h),Image.NEAREST)
    for i,(t,im) in enumerate((('model r7 (natief, zelfde schaal)',M),('r6 C',rgb(r6).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)),('r7',rgb(o).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST)))):
        V.paste(im,(i*(w+12),y+14)); d.text((i*(w+12)+2,y),naam+': '+t,fill=(0,0,0))
    y+=h+24
V.paste(rgb(o).resize((512,512),Image.NEAREST),(0,y)); x=530
for bg in ((240,240,236),(40,40,56)):
    for s in (1,2): V.paste(rgb(o,bg).resize((64*s,64*s),Image.NEAREST),(x,y)); x+=64*s+10
V=V.crop((0,0,1600,y+520)); V.save('vel.png')
