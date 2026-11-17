# r13: drie oogvarianten op eind/pitahaya2_eind2.png. Jordi: "zijn oog lijkt nu geen pupil te hebben".
# Doel (model_oog_zoom): dik zwart ooglid, wit | verticale zwarte pupil | wit (rechts breder), grijze schaduw bovenin het wit.
# Gen 3-bron: Feraligatr (anim_front, frame 1), oog x22-25 y14-17: lid, iris-pupil-iris met een pupil van 2 px hoog,
# grijs (J) bovenin. Overgenomen met onze kleuren: iris/glans -> W, pupil L/C -> K, grijs J -> v.
import numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
N='.KdrpPgGhHwWsv'; I={c:i for i,c in enumerate(N)}
src=Image.open(B+'eind/pitahaya2_eind2.png'); a0=np.array(src).astype(int)
V={'A':[((14,40),'K','W','wit links van de pupil (model)'),((15,40),'W','K','pupil: verticaal onder het lid, in het midden (model)')],
   'B':[((14,40),'K','W','wit links (model)'),((15,40),'W','K','pupil (model)'),((17,40),'r','W','groter wit rechts (model), oog 1 px breder'),
        ((16,39),'W','v','grijze schaduw bovenin het wit, onder het lid (model)'),((17,39),'r','K','lid loopt door boven het bredere wit (anders losse r)')],
   'C':[((14,40),'K','W','iris links (Feraligatr (22,16))'),((15,40),'W','K','pupil (Feraligatr L (23,16))'),((16,39),'W','v','grijs bovenin (Feraligatr J (22,15))'),
        ((14,41),'p','W','iris links (Feraligatr (22,17))'),((15,41),'p','K','pupil 2 px hoog (Feraligatr C (23,17))'),((16,41),'p','W','iris rechts (Feraligatr (24,17)); oog 1 px hoger')]}
EYE={(x,y) for x in range(12,19) for y in range(37,43)}
def dam(a): return {(x,y) for y in range(63) for x in range(63) if (q:=a[y:y+2,x:x+2])[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q}
def los(a): return {(x,y) for y in range(1,63) for x in range(1,63) if a[y,x] and all(a[y+dy,x+dx]!=a[y,x] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))}
out=[]
for k,lst in V.items():
    a=a0.copy()
    for (x,y),oud,nieuw,why in lst:
        assert N[a[y,x]]==oud,(k,x,y,N[a[y,x]]); a[y,x]=I[nieuw]; out.append(f'{k}\t{x}\t{y}\t{oud}\t{nieuw}\t{why}')
    chg={(x,y) for y,x in zip(*np.where(a!=a0))}; assert chg<=EYE and len(chg)==len(lst); assert ((a>0)==(a0>0)).all()
    print(k,'diff',len(chg),'(alle in het oog, x12-18 y37-42; erbuiten 0)','dambord nieuw',sorted(dam(a)-dam(a0)),'losse nieuw',sorted(los(a)-los(a0)))
    for y in range(37,43): print('  ',y,''.join(N[v] for v in a[y,10:21]))
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(src.getpalette()); im.save(f'pitahaya2_r13_oog{k}.png',transparency=0)
open('pitahaya2_r13_afwijkingen.txt','w').write('variant\tx\ty\toud\tnieuw\treden\n'+'\n'.join(out)+'\n')
