# l2.py: linkerhand L2 (voorstel Claude, Jordi: "je voorstel kunnen we proberne"): ronde vuist ±1,5x naar de opbouw van de Alakazam-lepelhand,
# kaart steekt boven (links) en onder uit de vuist, vingers voor de kaart. Rijen x3..x20, op onderlaag_L1.txt
import pal,sys
L2="""
37|.dwwwwwao.occccccc|
38|.dwwwooaoooooccccc|
39|..dwwoooaabbbocccc|
40|...dwwoaabbbccoooo|
41|....owoaodbbcddcco|
42|.....oooabbcccccoo|
43|.....obbodccccco.o|
44|......oobbcccco..o|
45|.......obcccco==oo|
46|........ooooo=====|
47|.........dwwao====|
48|........dwwao=====|
49|........oooo======|
"""
def bouw(base,blok,x0=3):
    R=[list(r) for r in pal.load(base)]
    for l in blok.strip().split('\n'):
        y,s=l.split('|')[:2]; y=int(y)
        if len(s)!=18: print('LENGTE',y,len(s))
        for i,c in enumerate(s):
            if c!='=': R[y][x0+i]=c
    return [''.join(r) for r in R]
if __name__=='__main__':
    R=bouw('onderlaag_L1.txt',L2); open(sys.argv[1] if len(sys.argv)>1 else 'var_L2.txt','w').write('\n'.join(R)+'\n')
