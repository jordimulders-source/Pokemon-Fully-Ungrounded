# Pupilvarianten op de eindkeuring (Jordi: "hij kijkt naar rechts, dat is anders dan het model en ons principe").
# Model (natief): linkerpupil rechts in het linkeroog (sprite x27,9), rechterpupil links in het rechteroog (x33,8-34,2) -> kijkt naar binnen/de kijker.
# A: rechterpupil 1 naar links (x34 -> x33), wisselt met het oogwit. B: A + linkerpupil 1 naar links (x28 -> x27).
from PIL import Image; import numpy as np
im=Image.open('eindkeuring/sauna_yeti_ek.png'); a=np.array(im)
def zet(o,swaps,naam):
    o=o.copy()
    for (x1,x2,y) in swaps: o[y,x1],o[y,x2]=o[y,x2],o[y,x1]
    p=Image.fromarray(o,'P'); p.putpalette(im.getpalette()); p.save(f'eindkeuring/ogen/{naam}.png',transparency=0); return p
A=zet(a,[(33,34,24)],'ogen_A'); B=zet(a,[(33,34,24),(27,28,24)],'ogen_B')
W=Image.new('RGB',(3*16*18+40,16*8+30),'white')
for i,p in enumerate([im,A,B]):
    bg=Image.new('RGBA',(64,64),'white'); bg.alpha_composite(p.convert('RGBA'))
    W.paste(bg.crop((23,19,41,27)).resize((18*16,8*16),Image.NEAREST),(i*(18*16+20),0))
W.save('eindkeuring/ogen/vel_ogen.png')
V=Image.new('RGB',(3*(512+16),512),'white')
for i,p in enumerate([im,A,B]):
    bg=Image.new('RGBA',(64,64),'white'); bg.alpha_composite(p.convert('RGBA')); V.paste(bg.resize((512,512),Image.NEAREST),(i*528,0))
V.save('eindkeuring/ogen/vel_8x.png')
