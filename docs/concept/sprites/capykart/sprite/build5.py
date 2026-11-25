# r5: V2 (r4) met tanden pixel voor pixel uit een echte sprite (frame 1). Oude V2-tanden eerst terug naar V1 (= model zonder tanden),
# dan bronpixels (alleen tand-indices + hun zwarte lijn) geplakt onder de modelmond. Kleur: wit->W, lichtgrijs->9, donkergrijs->3, zwart->0.
import json, numpy as np
from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/sprite/'
v1=json.load(open(R+'r4/grid_V1.json')); v2=json.load(open(R+'r4/grid_V2.json'))
OX,OY=v2['OX'],v2['OY']
ref=Image.open(R+'r4/capykart_V2.png'); PALIMG=ref.getpalette(); IDX={}
# indexvolgorde van build4 (ORDER): lees uit V2: grid-teken -> index
a=np.array(ref)
for y,row in enumerate(v2['grid']):
    for x,c in enumerate(row): IDX[c]=int(a[OY+y,OX+x])
# bron, venster (x0,y0,x1,y1), indexmap, rijbeperking, plek (dx,dy): bron(x,y)->grid(x+dx,y+dy)
BRON={
 'T1':('bibarel/anim_front.png',(17,22,23,26),{3:'0',7:'9',8:'W'},None,(-1,8)),
 'T2':('bidoof/anim_front.png',(21,43,27,46),{5:'0',8:'W',12:'9',13:'3'},None,(-5,-13)),
 'T3':('raticate/anim_front.png',(12,41,17,45),{1:'W',13:'9',14:'3',15:'0'},{45:{15}},(4,-11)),
}
log=[]
for k,(p,(x0,y0,x1,y1),M,rowlim,(dx,dy)) in BRON.items():
    g=[list(r) for r in v2['grid']]
    # oude V2-tanden weg: alle cellen die in V2 anders zijn dan V1 in de tandzone
    for y in range(29,36):
        for x in range(14,24):
            if v2['grid'][y][x]!=v1['grid'][y][x]:
                log.append(f'{k} weg ({x},{y}) {g[y][x]}->{v1["grid"][y][x]}  oude V2-tand terug naar V1 (model)'); g[y][x]=v1['grid'][y][x]
    src=np.array(Image.open(G+p))[:64]
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            v=int(src[y,x])
            if v not in M or (rowlim and y in rowlim and v not in rowlim[y]): continue
            gx,gy=x+dx,y+dy
            if g[gy][gx]!=M[v]: log.append(f'{k} tand ({gx},{gy}) {g[gy][gx]}->{M[v]}  uit {p} ({x},{y}) index {v}')
            g[gy][gx]=M[v]
    img=np.zeros((64,64),'uint8')
    for y,row in enumerate(g):
        for x,c in enumerate(row): img[OY+y,OX+x]=IDX[c]
    im=Image.fromarray(img,'P'); im.putpalette(PALIMG); out=R+f'r5/capykart_{k}.png'; im.save(out,transparency=0)
    Image.open(out).convert('RGBA').resize((512,512),Image.NEAREST).save(R+f'r5/capykart_{k}_8x.png')
    json.dump({'OX':OX,'OY':OY,'grid':[''.join(r) for r in g]},open(R+f'r5/grid_{k}.json','w'))
    print(k); [print(y,''.join(g[y][12:26])) for y in range(27,37)]
open(R+'r5/log.txt','w').write('Capykart r5 = r4 V2 met tanden uit echte sprites (frame 1). Gridcoordinaten (beeld-x = grid-x + 1).\nAlles buiten de tandzone pixel-identiek aan V2.\n\n'+'\n'.join(log)+'\n')
