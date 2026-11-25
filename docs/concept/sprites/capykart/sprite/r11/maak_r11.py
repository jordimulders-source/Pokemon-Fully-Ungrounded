"""Capykart r10 -> r11: eigen vacht-hooglicht (4e vachttint) als bolling; slot vrij via variant A of B."""
import os
from PIL import Image
D=os.path.dirname(os.path.abspath(__file__))
src=Image.open(os.path.join(D,'../r10/capykart.png')); W,H=src.size
base=[[src.getpixel((x,y)) for x in range(W)] for y in range(H)]
HL=(236,186,146)
BLOB={14:[27,28],15:[26,27,28],16:[25,26,27],17:[24,25,26],18:[20,21,22],19:[22,23]}
def blob(g,idx,log):
    for y,xs in BLOB.items():
        for x in xs:
            if g[y][x]==2: g[y][x]=idx; log.append(f'({x},{y}) 2->{idx:X} vacht-hooglicht')
            else: log.append(f'({x},{y}) overgeslagen (index {g[y][x]})')
def save(g,pal,name):
    o=Image.new('P',(W,H)); o.putpalette(pal); o.putdata([v for r in g for v in r]); o.save(os.path.join(D,name),transparency=0)
    o.convert('RGBA').resize((W*8,H*8),Image.NEAREST).save(os.path.join(D,name.replace('.png','_8x.png')))
L=[]
# A: groen-donker 11 -> gedeelde koele schaduw in 8; 11 = vacht-hooglicht
g=[r[:] for r in base]; pal=src.getpalette()[:]; la=[]
n=0
for y in range(H):
    for x in range(W):
        if g[y][x]==11: g[y][x]=8; n+=1
pal[8*3:8*3+3]=[64,104,112]; pal[11*3:11*3+3]=list(HL)
blob(g,11,la); save(g,pal,'capykart_A.png')
L.append(f'A: {n} px groen-donker 11 -> 8; 8 = (64,104,112) gedeelde koele schaduw (hoepels, morrillo, blauwe zijkant, tandschaduw, groen schaduwvlak); 11 = vacht-hooglicht {HL}')
L+=['   '+s for s in la]
# B: geel 14 vrij: geel voorvlak -> 9 (crème), 9 = crème
g=[r[:] for r in base]; pal=src.getpalette()[:]; lb=[]; n=0
for y in range(H):
    for x in range(W):
        if g[y][x]==14: g[y][x]=9; n+=1
pal[9*3:9*3+3]=[252,232,150]; pal[14*3:14*3+3]=list(HL)
blob(g,14,lb); save(g,pal,'capykart_B.png')
L.append(f'B: {n} px geel 14 -> 9; 9 = crème (252,232,150) = tanden + bevels + glans + geel voorvlak; 14 = vacht-hooglicht {HL}')
L+=['   '+s for s in lb]
# controle
r7=Image.open(os.path.join(D,'../../eindkeuring/capykart_r7.png')).load()
fz=[(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]+[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)]
r10=src.load()
for nm in ('capykart_A.png','capykart_B.png'):
    b=Image.open(os.path.join(D,nm)).load()
    L.append(f'{nm}: alpha-diff t.o.v. r7 {sum((r7[x,y]==0)!=(b[x,y]==0) for x in range(W) for y in range(H))}; bevroren index-diff t.o.v. r10 {sum(b[p]!=r10[p] for p in fz)}')
open(os.path.join(D,'log.txt'),'w').write('\n'.join(L)+'\n'); print('\n'.join(l for l in L if not l.startswith('   ')))
