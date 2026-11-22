"""Linkerhelft (x0-15, kolom 15 = midden) spiegelen naar rechts (x' = 30 - x) -> symmetrisch aanzicht.
Invoer: regels 'y aaaaaaaa bbbbbbbb' (16 kolommen). Rechts: licht valt linksboven, dus 7/6 -> 5 in de
buitenste kolommen (afstand tot midden >= 4) en 7 -> 6 elders; daarna optionele correcties 'R y x c' en 'Z y x pixels' ('_' = laten staan).
Gebruik: spiegel.py in.half uit.txt"""
import sys,os,numpy as np
sys.path.insert(0,os.path.dirname(__file__)); from ow_pal import totext
def maak(p):
    a=np.zeros((32,32),np.uint8); fix=[]
    for l in open(p):
        if not l.strip() or l.startswith('#'): continue
        if l.startswith('R'): _,y,x,c=l.split(); fix.append((int(y),int(x),int(c,16))); continue
        if l.startswith('Z'):   # Z y x pixels: na het spiegelen zetten (asymmetrische delen, bv. de staartpluim)
            _,y,x,st=l.split()
            for i,c in enumerate(st):
                if c!='_': fix.append((int(y),int(x)+i,0 if c=='.' else int(c,16)))
            continue
        y,*b=l.split(); r=''.join(b); assert len(r)==16,(y,len(r)); y=int(y)
        for x,c in enumerate(r):
            if c=='.': continue
            v=int(c,16); a[y,x]=v
            if x<15:
                m=v
                if 15-x>=4 and v in (6,7): m=5   # buitenste kolommen rechts = schaduwkant
                elif v==7: m=6
                a[y,30-x]=m
    for y,x,c in fix: a[y,x]=c
    return a
if __name__=='__main__':
    a=maak(sys.argv[1]); open(sys.argv[2],'w').write(totext(a)+'\n')
