"""Salticonda kleurronde 3e: kleur3 met exact dezelfde vorm (alpha-diff 0); alleen binnen de kuif de zouttextuur van 3b:
okernaden (g), lichte opstaande randen (a/b aan de lichtkant van een naad, c/d aan de schaduwkant) en korrels.
Omlijning, neus/snuit, oog, wenkbrauw, wang, halsband en lijf: pixel voor pixel kleur3 (check_kleur3e.py)."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'; I=CH.index
# rij -> (x0, tekens); ' ' = kleur3 laten staan
TEX={
 1:(19,"aabab"),               # korrels op de voorste top (rand 25-26 en 32-34 blijven)
 1.5:(27,"aabab"),
 2:(17,"aaabbbbbcgabbabbbb"),
 3:(15,"aaabbbabbbbcgabbbbbbcg"),
 4:(14,"aabbbbbbbbabbcgabbbbbcga"),
 5:(28,"cgabbbcgacd"),
 6:(31,"abbcgacd"),
 7:(34,"gaggde"),
 8:(34,"gbaagge"),
 9:(37,"cabd"),
 10:(37,"cbcde"),
 11:(37,"gccdde"),
 12:(37,"gccdde"),
 13:(37,"cgbcde"),
 14:(37,"cgbcde"),
 15:(37,"cgccde"),
 16:(37,"cgggde"),
 17:(37,"cgbbgg"),
 18:(37,"cgddce"),
 19:(37,"gddde e".replace(' ','')),
}
def kuifmasker(x,y): return y<20 and ((y<=5 and x>=13) or (6<=y<=9 and x>=21) or (y>=10 and x>=34))
def vast(x,y): return (21<=x<=33 and 7<=y<=9) or (23<=x<=30 and y==6) or (25<=x<=27 and y==5) or (20<=x<=33 and 10<=y<=15) or (33<=x<=36 and 9<=y<=19)
def build():
    K3=Image.open(D+'kleur3/salticonda.png'); P=K3.load(); out=K3.copy(); Q=out.load()
    for key,(x0,t) in TEX.items():
        y=int(key)
        for i,ch in enumerate(t):
            x=x0+i
            if ch==' ': continue
            assert P[x,y]!=0 and CH[P[x,y]] not in 'hKO', ('omlijning/leeg',x,y,CH[P[x,y]])
            assert kuifmasker(x,y) and not vast(x,y), ('buiten kuif',x,y)
            Q[x,y]=I(ch)
    return out
if __name__=='__main__':
    im=build(); im.save(D+'kleur3e/salticonda.png',transparency=0); Q=im.load()
    open(D+'kleur3e/salticonda_raster.txt','w').write('\n'.join(''.join(CH[Q[x,y]] for x in range(64)) for y in range(64))+'\n')
