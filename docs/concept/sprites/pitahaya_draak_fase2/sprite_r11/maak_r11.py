# r11 op r10 (hoofd + plaatlicht): 14 px uit eindkeuring/KEURING_r10.md. Diff 0 erbuiten, asserts per pixel.
import numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
N='.KdrpPgGhHwWsv'; I={c:i for i,c in enumerate(N)}
JOB=[([(19,48),(18,49),(19,49),(17,50),(18,50),(19,50),(16,51),(17,51)],'p','r','verre lip p -> r (KEURING_r10)'),
     ([(19,43)],'p','r','mondhoek p -> r (KEURING_r10)'),
     ([(24,48),(25,48),(26,48),(27,48),(26,49)],'d','r','sikkelplak d -> r (KEURING_r10)')]
def dam(a):
    return {(x,y) for y in range(63) for x in range(63) if (q:=a[y:y+2,x:x+2])[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q}
def los(a):  # figuurpixel zonder enige 4-buur van dezelfde index
    return {(x,y) for y in range(1,63) for x in range(1,63) if a[y,x] and all(a[y+dy,x+dx]!=a[y,x] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))}
log=[]
for bron,uit in (('pitahaya2_r10.png','pitahaya2_r11.png'),('pitahaya2_r10_plaatlicht.png','pitahaya2_r11_plaatlicht.png')):
    im=Image.open(B+'sprite_r10/'+bron); a0=np.array(im).astype(int); a=a0.copy(); want=set()
    for px,oud,nieuw,why in JOB:
        for x,y in px:
            assert N[a[y,x]]==oud,(uit,x,y,N[a[y,x]]); a[y,x]=I[nieuw]; want.add((x,y))
            if uit=='pitahaya2_r11.png': log.append(f'{x}\t{y}\t{oud}\t{nieuw}\t{why}')
    assert {(x,y) for y,x in zip(*np.where(a!=a0))}==want
    assert ((a>0)==(a0>0)).all()
    print(uit,'diff',len(want),'dambord nieuw',sorted(dam(a)-dam(a0)),'losse px nieuw',sorted(los(a)-los(a0)))
    o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(im.getpalette()); o.save(uit,transparency=0)
    r=o.convert('RGBA'); bg=Image.new('RGBA',(64,64),(232,234,238,255)); bg.alpha_composite(r); bg.convert('RGB').resize((512,512),Image.NEAREST).save(uit[:-4]+'_8x.png')
open('pitahaya2_r11_afwijkingen.txt','w').write('x\ty\toud\tnieuw\treden\n'+'\n'.join(log)+'\n')
