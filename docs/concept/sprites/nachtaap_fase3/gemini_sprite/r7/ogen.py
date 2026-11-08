from PIL import Image, ImageDraw; import numpy as np
CH='.123456789abcdef'
src=Image.open('../r6/R2.png'); PAL=src.getpalette()[:48]; P=np.array(PAL).reshape(16,3); A0=np.array(src)
def oog(L,R,y0=37):
    a=A0.copy()
    for r,s in enumerate(L):
        for k,c in enumerate(s): a[y0+r,5+k]=CH.index(c)
    for r,s in enumerate(R):
        for k,c in enumerate(s): a[y0+r,12+k]=CH.index(c)
    return a
def rgb(a,s,bg=(255,255,255)):
    r=np.zeros((64,64,3),int); r[:]=bg; m=a>0; r[m]=P[a[m]]
    return Image.fromarray(r.astype('uint8')).resize((64*s,64*s),Image.NEAREST)
O={
 'huidig':(["9f","fa","ef"],["9ff","faa","fef"]),
 'A Xatu':(["66","9f","6a"],["666","9f9","6a6"]),
 'B Mewtwo':(["66","af","f6"],["666","9af","9f6"]),
 'C Absol':(["66","fa","a9"],["666","ffa","fa9"]),
 'D Darkrai':(["66","ae","fa"],["666","aea","faf"]),
 'E iris+wit':(["66","fa","9f"],["666","9fa","9af"]),
 'F smal gloed':(["66","ea","66"],["666","eea","666"]),
}
import sys
v=Image.new('RGB',(len(O)*300,420),'white'); d=ImageDraw.Draw(v)
for i,(n,(L,R)) in enumerate(O.items()):
    a=oog(L,R); Image.fromarray(a,'P').save('tmp.png')
    k=rgb(a,16).crop((0,30*16,18*16,44*16))
    v.paste(k,(i*300,20)); d.text((i*300+4,4),n,fill='black')
    v.paste(rgb(a,2).crop((0,40,64,120)),(i*300,260)); v.paste(rgb(a,1),(i*300+150,260))
v.save('kandidaten.png')
