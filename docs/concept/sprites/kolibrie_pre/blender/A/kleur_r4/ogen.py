"""Oogvarianten: bron-uitsnede (8x) naast het overgenomen oog in de kop van r4 (8x). -> ogen_8x.png + oog_<naam>_8x.png"""
import sys; sys.path.insert(0,'.')
from PIL import Image, ImageDraw
import palet
H='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/kleur_r4/'
G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
base=[list(l.rstrip('\n')) for l in open(H+'raster.txt')][:64]
# gezicht rond het oog in r4 (wordt eerst teruggezet, daarna het oog erover)
FACE={16:'5422',17:'54',18:'4',19:'4',20:'2',21:'2'}
def kop(eye):
    g=[r[:] for r in base]
    # leeg oogvlak x20-26, y16-21 vullen met gezicht (5 boven/voor, 4 achter, 3 onder)
    for y in range(16,22):
        for x in range(20,27):
            g[y][x]='5' if x<=21 and y<=19 else ('4' if y<21 else '3' if 22<=x<=24 else '4')
    for (x,y),c in eye.items(): g[y][x]=c
    return g
def blok(s,x0,y0):
    d={}
    for j,row in enumerate(s.split('/')):
        for i,c in enumerate(row):
            if c!=' ': d[(x0+i,y0+j)]=c
    return d
VAR={
 # Latias (graphics/pokemon/latias, x12-17 y17-22): rand 6->2, iris B->A, D->8, pupil 3->1, wit C: glans->7, oogwit->6, licht 4->6, schaduw 5->3, gezicht A->huidkleur
 'latias':  (blok('  222/ 2A66/ 7A86/2A186/2A186/2233 ',21,16), 'latias',12,17,6,6),
 # Combusken (x29-33 y18-22): rand 5->2, glans 9->7, iris 8->8, donker 4->A, pupil 2->1, 1->3
 'combusken':(blok('  22 / 28A /278A /f18A /f3A  '.replace('f','5'),21,17), 'combusken',29,18,5,5),
 # Skarmory (x9-14 y25-27): lid 3->2, 6->1, iris D->8, C->A (geen glans in de bron)
 'skarmory': (blok('   211/ A18A /281 8 '.replace(' 8 ','8'),20,18), 'skarmory',9,25,6,3),
}
def png(g):
    open(H+'_tmp.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
    palet.build(H+'_tmp.txt',H+'_tmp.png'); return Image.open(H+'_tmp.png').convert('RGBA')
Z=8; tiles=[]
for naam,(eye,src,sx,sy,w,h) in VAR.items():
    s=Image.open(G+src+'/anim_front.png').convert('RGBA').crop((sx-2,sy-2,sx+w+2,sy+h+2))
    s=s.resize((s.width*Z,s.height*Z),Image.NEAREST)
    k=png(kop(eye)).crop((14,12,33,26)); k=k.resize((k.width*Z,k.height*Z),Image.NEAREST)
    t=Image.new('RGBA',(s.width+k.width+24,max(s.height,k.height)+20),(235,235,235,255))
    t.alpha_composite(s,(0,20)); t.alpha_composite(k,(s.width+24,20))
    ImageDraw.Draw(t).text((2,4),f'{naam}: bron (8x)  ->  in de kop (8x)',fill=(0,0,0))
    t.save(H+f'oog_{naam}_8x.png'); tiles.append(t)
W=max(t.width for t in tiles); out=Image.new('RGBA',(W,sum(t.height+8 for t in tiles)),(200,200,200,255)); y=0
for t in tiles: out.alpha_composite(t,(0,y)); y+=t.height+8
out.save(H+'ogen_8x.png')
import os; os.remove(H+'_tmp.txt'); os.remove(H+'_tmp.png')
