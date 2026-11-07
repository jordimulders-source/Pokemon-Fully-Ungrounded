# Ronde 2, stap B: kleur per onderdeel, per rij met de hand. Elke string begint op x_van van het bereik in pose.py
# (lengte wordt gecontroleerd). '_' = laten staan. Daarna losse pixels (EXTRA) en tot slot de bevroren delen.
from pose import PARTS, ORDER
K = {
 'F': {2:["ff","f999f"],3:"f1d9666779",4:"ff7677789",5:"f1d8778889",6:"fff888fff",7:"fff"},
 'L': {2:"f9999",3:"87769",4:"_f77769",5:"_f877769",6:"f8777769",7:"ff877669",8:"ff8776669",9:"f88777769",
       10:"ff8777669",11:"ff87776669",12:"f887766669",13:"ff88766669",14:"ff876666_",15:"ff87666_",16:"ff76__",17:"f8__"},
 'E': {1:["f","f"],2:"f1f1f",3:"fdfdf",4:"f9667f",5:"96677f",6:"f97778f",7:"f8888f"},
 'R': {8:"999f",9:"9778f",10:"967f",11:"9678f",12:"9778f",13:"9788f",14:"9678f",15:"_____f"},
 'P': {14:"7f",15:"67f888",16:"6777f88f",17:"677777f8f",18:"67777777f8f",19:"67777777788f",20:"6777777777 88f",
       21:"667777777788f",22:"66777777788f",23:"677777788f",24:"7777788f",25:"77788f",26:"778f",27:"8f"},
 'T': {23:"333",24:"53333",25:"5333333",26:"53333333",27:"5333333333",28:"5333333344f",29:"5333333334 44f",
       30:"533333333444f",31:"53333333334444f",32:"53333333334444f",33:"53333333334444f",34:"53333333333444f",
       35:"52333333333444f",36:"5233333333334444f",37:"5333333333334444f",38:"333333333344 44f",39:"3333333334 44f",
       40:"33333334 44f",41:"_______4f",42:"_______f"},
 'S': {41:"333333334",42:"33333333444",43:"3333334 44f",44:"f333444f"},
 'N': {38:"ff3",39:"4333",40:"4443333",41:"44433333",42:"44443333",43:"fffffff"},
 'W': {16:"5555",17:"523335",18:"52333335",19:"5334f3335",20:"5334f4334f",21:"5334ff44f",22:"aaab",23:"bbbb",
       24:"5334",25:"5334",26:"5334",27:"533",28:"53"},
 'Q': {20:"5555",21:"52333f",22:"5223333f",23:"5233333f",24:"5333334f",25:"5333344f",26:"f3344f",27:"ffff"},
 'H': {24:"ffffff"+"ff"+"fffff",
       25:"fff"+"c"*12+"aa"+"ccccc"+"f",
       26:"ff"+"ccc"+"e"*12+"ab"+"eeee"+"cef",
       27:"f"+"eeee"+"c"*12+"bb"+"ccc"+"ecef",
       28:"f"+"ccccc"+"e"*12+"ff"+"ee"+"cecef",
       29:"f"+"eeeee"+"c"*12+"e"+"f"+"cececef",
       30:"f"+"ccccc"+"e"*12+"e"+"f"+"cececef",
       31:["feeeeeee","eef"+"cececef"],32:"ceceff",33:"cecef",34:"ceff",35:"cef",36:"ff"},
 'K': {21:"ff",22:"f45f",23:"f345",24:"f3344f"},
 'G': {42:"f4333333444444f",43:"ff4444444ff",44:"fffffff"},
}
EXTRA = [  # (x,y,kleur): losse handpixels
 (41,23,'b'),(41,24,'b'),   # hangend eindje prajiad vrije arm (zwaartekracht)
]
def bouw():
    g=[['.']*64 for _ in range(64)]
    fout=[]
    for p in ORDER:
        for y,rs in PARTS[p].items():
            ss=K[p].get(y)
            if ss is None: fout.append((p,y,'geen kleur')); continue
            if isinstance(ss,str): ss=[ss]
            for (a,b),s in zip(rs,ss):
                s=s.replace(' ','')
                if len(s)!=b-a+1: fout.append((p,y,len(s),b-a+1))
                for i,c in enumerate(s):
                    if c not in '_.' and a+i<=b: g[y][a+i]=c
    for x,y,c in EXTRA: g[y][x]=c
    fr=[r.rstrip('\n') for r in open('bevroren.txt')]
    for y in range(64):
        for x in range(64):
            if fr[y][x]!='.': g[y][x]=fr[y][x]
    # linkeroog 1 px naar rechts (los van de buitenlijn); vorm = Hitmontops oog, ongewijzigd
    for y,x0,s in [(34,10,"33ff3"),(35,10,"3f1ff"),(36,10,"3ffff"),(37,10,"33ff3")]:
        for i,c in enumerate(s): g[y][x0+i]=c
    # grijs-witte polsband weg (huid zoals de arm erboven); opzij stekend prajiad-staartje weg
    for y in (53,54):
        for i,c in enumerate("5234f"): g[y][33+i]=c
    for x,y in [(38,47),(38,48),(39,48),(38,49),(39,49),(38,50)]: g[y][x]='.'
    return g,fout
if __name__=='__main__':
    g,fout=bouw()
    for f in fout: print('LENGTE',f)
    open('raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
