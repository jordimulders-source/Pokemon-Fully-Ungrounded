# Ronde 2, stap B: kleur per onderdeel, per rij met de hand. Elke string begint op x_van van het bereik in pose.py
# (lengte wordt gecontroleerd). '_' = laten staan. Daarna losse pixels (EXTRA) en tot slot de bevroren delen.
from pose import PARTS, ORDER
K = {
 'F': {1:"fff999f",2:"fc96667799",3:"f76777789",4:"fd87778889",5:"ff888ffff",6:"fff"},
 'L': {1:"999",2:"_7669",3:"_7769",4:"__f7769",5:"__f87769",6:"f8877669",7:"f8877669",8:"ff8877669",9:"ff8877669",
       10:"ff8877669",11:"ff88777669",12:"ff88777669",13:"ff88777669",14:"ff887776_",15:"ff88777_",16:"ff87__",17:"f8__"},
 'E': {1:"fff",2:"fcfdf",3:"f9667f",4:"96677f",5:"f97778f",6:"f9999f"},
 'R': {7:"9778f",8:"978f",9:"9778f",10:"978f",11:"9778f",12:"9778f",13:"9778f",14:"9778f",15:"_____f"},
 'P': {14:"7f",15:"67f888",16:"6777f88f",17:"677777f8f",18:"67777777f8f",19:"67777777788f",20:"6777777777 88f",
       21:"667777777788f",22:"66777777788f",23:"677777788f",24:"7777788f",25:"77788f",26:"778f",27:"8f"},
 'T': {23:"333",24:"33333",25:"5333333",26:"53333333",27:"5333333333",28:"5333333344f",29:"5333333334 44f",
       30:"_5333333 3444f",31:"_5333333334444f",32:"__533333334444f",33:"___5333333 4444f",34:"52333333333444f",
       35:"52333333333444f",36:"5233333333334444f",37:"5233333333334444f",38:"233333333344 44f",39:"3333333334 44f",
       40:"33333334 44f",41:"_______4f",42:"_______f"},
 'S': {41:"333333334",42:"33333333444",43:"3333334 44f",44:"f333444f"},
 'N': {38:"ff3",39:"4333",40:"4443333",41:"44433333",42:"44443333",43:"fffffff"},
 'W': {17:"555",18:"52235",19:"523335",20:"52333334",21:"523335444",22:"52334fff",23:"5234",24:"5234",25:"5234",
       26:"5234",27:"5234",28:"5234",29:"aaab",30:"bbbb",31:"523",32:"5234",33:"5233"},
 'Q': {21:"5555",22:"52233f",23:"5222233f",24:"5222233f",25:"5322333f",26:"5333334f",27:"f3334f",28:"ffff"},
 'H': {25:"fff____ffffff",26:"f4444____455555eaf",27:"f44444ffff5555eeeabf",
       28:"f4444555555e5555eeab4545f",29:"f4445555e55555eeeebb4545f",30:"f4555e555555eeeeeeff5e5ef",
       31:["fe5555ee","eee45ef"],32:"f45ff",33:"5ef",34:"ff"},
 'G': {42:"f4333333444444f",43:"ff4444444ff",44:"fffffff"},
}
EXTRA = [  # (x,y,kleur): losse handpixels
 (41,24,'f'),            # buitenrand vrije bovenarm tegen de achtergrond
 (39,30,'a'),(39,31,'b'),(39,32,'b'),   # hangend eindje prajiad vrije arm (zwaartekracht, over de borst)
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
    return g,fout
if __name__=='__main__':
    g,fout=bouw()
    for f in fout: print('LENGTE',f)
    open('raster.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
