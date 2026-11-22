# r9: vijf kleurvarianten. Patroon: trap.txt (getrapt, V1-V4) en schuin.txt (V5), met de hand per pixel.
# Palet: 13 vaste kleuren (kop, ogen, creme ledematen, strepen) + max 2 nieuwe per variant (16 incl. transparant).
from variant import *
TERRA={'T':(160,52,44),'t':(104,34,36)}
V={
 'V1':('trap.txt',  dict(g=('R','T','t'),a=('M','D','S'),l=('1','1'),sel='t',bin='K'),TERRA),
 'V2':('trap.txt',  dict(g=('A','A','a'),a=('L','M','D'),l=('S','S'),sel='a',bin='K'),{'A':(164,94,64),'a':(110,56,46)}),
 'V3':('trap.txt',  dict(g=('b','2','1'),a=('Y','y','S'),l=('1','1'),sel='2',bin='K'),{'Y':(240,196,78),'y':(190,136,50)}),
 'V4':('trap.txt',  dict(g=('3','2','1'),a=('G','H','H'),l=('W','W'),sel=None,bin='K'),{'G':(56,160,72),'H':(40,104,56)}),
 'V5':('schuin.txt',dict(g=('R','T','t'),a=('M','D','S'),l=('1','1'),sel='t',bin='K'),TERRA),
}
if __name__=='__main__':
    for v,(f,pal,ex) in V.items():
        R,K2=bouw(lees(f),pal,ex); n=schrijf('astro_%s.png'%v,R,K2); print(v,f,n,'kleuren')
