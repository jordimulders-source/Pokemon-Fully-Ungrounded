"""r9 = kleur_r8/raster.txt + reparaties uit kleur_r8/KEURING.md §4 (index '0' = transparant) + optioneel (40,29),(40,30) A->8."""
import sys
A='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/blender/A/'
R={
 'buik':[((16,24),'2'),((17,24),'6'),((16,25),'2'),((17,25),'6'),((17,26),'2'),((18,26),'6'),((17,27),'2'),((18,27),'6'),
         ((17,28),'2'),((18,28),'6'),((19,28),'6'),((18,29),'2'),((19,29),'6'),((18,30),'2'),((19,30),'6'),((18,31),'2'),((19,31),'6'),
         ((21,38),'2'),((22,38),'6')],
 'verre poot':[((31,43),'9'),((32,43),'F'),((33,43),'1'),((31,44),'1'),((32,44),'1'),((33,44),'0'),((34,44),'0'),((35,44),'0')],
 'nabije poot':[((29,44),'1'),((30,44),'0'),((25,45),'0'),((26,45),'1'),((27,45),'1'),((28,45),'1'),((29,45),'0'),((30,45),'0')],
 'leeg':[((p),'0') for p in [(31,45),(32,45),(33,45),(34,45),(26,46),(28,46),(31,46),(33,46)]],
 'optioneel':[((40,29),'8'),((40,30),'8')],
}
if __name__=='__main__':
    g=[list(l.rstrip('\n')) for l in open(A+'kleur_r8/raster.txt')][:64]
    for k,l in R.items():
        for (x,y),c in l: g[y][x]='.' if c=='0' else c
    open(A+'kleur_r9/raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
    sys.path.insert(0,A+'kleur_r9'); import palet; palet.build(A+'kleur_r9/raster.txt',A+'kleur_r9/kolibrie_pre.png')
