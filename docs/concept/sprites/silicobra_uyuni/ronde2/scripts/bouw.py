# bouwt silicobra_uyuni.png uit rijen_x12.txt (handgetypt) + omgezette basis ('?')
import sys
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/silicobra_uyuni/ronde2/'
im=Image.open('/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/silicobra/anim_front.png')
d=list(im.get_flattened_data())
M={0:'.',10:'O',2:'K',3:'e',5:'a',6:'f',12:'g',7:'b',8:'d',1:'t',4:'c',9:'s',11:'r'}
rows=[[M[d[y*64+x]] for x in range(64)] for y in range(64)]
for l in open(D+'rijen_x12.txt'):
    y,s=l.split(); y=int(y)
    for i,ch in enumerate(s):
        if ch!='?': rows[y][12+i]=ch
P=[('.',(152,208,160)),('O',(40,36,40)),('K',(104,88,76)),('e',(146,128,104)),('d',(176,160,136)),('c',(204,192,170)),('b',(228,220,202)),('a',(248,244,232)),
   ('f',(220,204,170)),('g',(186,164,126)),('q',(184,244,228)),('r',(96,204,192)),('s',(44,148,152)),('t',(24,92,104))]
idx={c:i for i,(c,_) in enumerate(P)}
out=Image.new('P',(64,64)); pal=[]
for _,rgb in P: pal+=rgb
out.putpalette(pal+[0]*(768-len(pal)))
out.putdata([idx[rows[y][x]] for y in range(64) for x in range(64)])
out.save(D+'silicobra_uyuni.png',transparency=0)
open(D+'silicobra_uyuni_raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
