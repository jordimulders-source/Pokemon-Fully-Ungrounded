# Bewijs (alfa- en gezichtsdiff) + voor_na.png
from PIL import Image, ImageDraw
import os
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'../../../../../..')
v=Image.open(os.path.join(H,'../../../olinguito_v2/af/olinguito.png')); n=Image.open(os.path.join(H,'na.png'))
assert n.mode=='P' and n.size==(64,64)
vp,np_=v.load(),n.load()
alfa=sum((vp[x,y]==0)!=(np_[x,y]==0) for x in range(64) for y in range(64))
# gezichtszone: hele kop incl. masker, oog, snoet, neus en de lijn eromheen (x<=32, y<=43) + oor/kruin
gezicht=[(x,y) for x in range(0,33) for y in range(0,44)]
gd=sum(vp[x,y]!=np_[x,y] for x,y in gezicht)
diff=[(x,y) for x in range(64) for y in range(64) if vp[x,y]!=np_[x,y]]
kl=len(set(n.getdata())-{0})
print('alfadiff',alfa,'gezichtsdiff',gd,'pixels gewijzigd',len(diff),'kleuren',kl)
print('palet-index 5 voor',v.getpalette()[15:18],'na',n.getpalette()[15:18])
refs=['aipom','linoone','furret','kangaskhan']
ims=[v,n]+[Image.open(os.path.join(R,'graphics/pokemon/%s/anim_front_gba.png'%s)).crop((0,0,64,64)) for s in refs]
lab=['voor','na']+refs
z=6; W=len(ims)*(64*z+10)
o=Image.new('RGB',(W,64*z+64+40),'white'); d=ImageDraw.Draw(o)
for i,(im,l) in enumerate(zip(ims,lab)):
    a=im.convert('RGBA'); X=i*(64*z+10)
    o.paste(a.resize((64*z,64*z),Image.NEAREST),(X,14),a.resize((64*z,64*z),Image.NEAREST))
    o.paste(a,(X+64*z//2-32,64*z+30),a); d.text((X+4,1),l,fill=(0,0,0))
o.save(os.path.join(H,'voor_na.png'))
