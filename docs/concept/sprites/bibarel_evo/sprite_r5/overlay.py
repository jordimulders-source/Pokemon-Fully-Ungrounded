# overlay.py: modelomtrek van borststuk/bandjes (rood) en modellijnen zak/zoom (blauw) over de sprite (12x); afwijking per rand in px
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image, ImageDraw
o=laad(sys.argv[1] if len(sys.argv)>1 else 'sprite_r5/sprite.png')
BF=np.load('sprite_r5/bib_frac.npy'); ZF=np.load('sprite_r5/zak_frac.npy')
BIB=(BF>=0.5); BIB[:30]=False; BIB[43:]=False; BIB[:,:19]=False; BIB[:,41:]=False; LIJN=BIB&(ZF>=0.3)
BAND={19:38,20:38,21:39,22:39,23:41,24:42,25:43,26:43,27:43,28:43,29:43,30:43,31:42,32:42,33:41,34:40,35:40,36:40,37:41,38:41,39:42,40:42,41:42,42:44}
SP=np.zeros((64,64),bool)
for x,b in BAND.items():
    for y in range(30,b): SP[y,x]=o[y,x] in (6,7,15)
Z=12; x0,y0,x1,y1=14,26,46,48
im=Image.fromarray(rgb(o)).crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST); d=ImageDraw.Draw(im)
for y in range(y0,y1):
    for x in range(x0,x1):
        X,Y=(x-x0)*Z,(y-y0)*Z
        if BIB[y,x]:
            if not BIB[y-1,x]: d.line([(X,Y),(X+Z,Y)],fill=(255,0,0),width=2)
            if not BIB[y+1,x]: d.line([(X,Y+Z),(X+Z,Y+Z)],fill=(255,0,0),width=2)
            if not BIB[y,x-1]: d.line([(X,Y),(X,Y+Z)],fill=(255,0,0),width=2)
            if not BIB[y,x+1]: d.line([(X+Z,Y),(X+Z,Y+Z)],fill=(255,0,0),width=2)
        if LIJN[y,x]: d.rectangle([X+4,Y+4,X+Z-4,Y+Z-4],outline=(0,0,255))
        if SP[y,x]!=BIB[y,x]: d.line([(X,Y),(X+Z,Y+Z)],fill=(255,0,255),width=2)
im.save('sprite_r5/overlay_tuinbroek.png')
dif=SP!=BIB
print('borststuk+bandjes: model %d px, sprite %d px, afwijkend %d px'%(BIB.sum(),SP.sum(),dif.sum()))
for nm,m in (('bandjes y30-33',np.s_[30:34]),('borststuk y34-38',np.s_[34:39]),('borststuk onder y39-42',np.s_[39:43])):
    print('  %-24s %d px'%(nm,dif[m].sum()), [(int(x),int(y)) for y,x in np.argwhere(dif) if m.start<=y<m.stop])
LS=np.isin(o,(6,15))&LIJN
print('modellijnen (zak, zoom onder de bolletjes, zijlijnen, onderzoom): model %d px, in de sprite als 6/F: %d px; ontbrekend:'%(LIJN.sum(),LS.sum()),[(int(x),int(y)) for y,x in np.argwhere(LIJN&~LS)])
