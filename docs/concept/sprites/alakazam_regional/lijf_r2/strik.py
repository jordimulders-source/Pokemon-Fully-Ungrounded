# lijf_r2: vervangers voor het strikje. Rijen beginnen bij x26, '=' = laten staan.
import pal,numpy as np
X0=26
LEEG={ # strikje weg: witte keel met kinschaduw a onder de kinlijn en a langs de rechterrand
25:"===aaaaaaa", 26:"=wwwwwwwwa", 27:"=wwwwwwwwa", 28:"=wwwwwwwa=", 29:"=wwwwwww==",
}
OPT={
'S1':{ # keelwam: rode huidflap vast aan de hele kinrand, in het midden 1 rij, naar links en rechts lager uitwaaierend
25:"===trrrrrs", 26:"===ttsarss", 27:"===ssaaass", 28:"===aawwaa=",
},
'S2':{ # sleutelbeenvlekken: twee rode tekeningen vanaf de hals langs de sleutelbeenderen, in het midden samen
26:"=trwwwwwrs", 27:"=ttrwwwrss", 28:"==rrswrs==", 29:"===rrss===", 30:"====ss====",
},
'S3':{ # keelvlek (roodborstje): de hele keel rood, vast aan de kin, ronde onderkant op de bovenborst
25:"===rrrrrrs", 26:"=ttrrrrrss", 27:"=ttrrrrrss", 28:"=trrrrrss=", 29:"=arrrssa==", 30:"==asssa===", 31:"===aaa====",
},
'S4':{ # rode stropdastekening: smalle taps toelopende streep over het midden van de plaat
25:"===rrsaaaa", 26:"===rrs====", 27:"===rrs====", 28:"====rs====", 29:"====rs====", 30:"====rs====", 31:"====rs====", 32:"====s=====", 33:"====s=====",
},
'S5':{ # zwarte stropdastekening (koolmees) met rood accent onder de kin
25:"===rrsaaaa", 26:"===rss====", 27:"===nmk====", 28:"===nmk====", 29:"===nmk====", 30:"====mk====", 31:"====mk====", 32:"====k=====", 33:"====k=====",
},
'S6':{}, # geen rood: alleen de witte keel en plaat
'S7':{ # rode ruit (kaartsymbool) als lichaamstekening op het borstbeen, zoals de ster/tekens van Kadabra
27:"=====t====", 28:"====trr===", 29:"===trrrs==", 30:"====rss===", 31:"=====s====",
},
'S8':{ # zwarte stropdastekening zonder rood
25:"===nmkaaaa", 26:"===nmk====", 27:"===nmk====", 28:"====mk====", 29:"====mk====", 30:"====mk====", 31:"====mk====", 32:"====k=====", 33:"====k=====",
},
}
def zet(R,W):
    for y,s in W.items():
        for i,c in enumerate(s):
            if c!='=': R[y][X0+i]=c
def bouw(basis,W):
    R=[list(r) for r in basis]; zet(R,LEEG); zet(R,W); return [''.join(r) for r in R]
if __name__=='__main__':
    basis=pal.load('basis_O1r.txt'); B=np.array([list(r) for r in basis])
    for n,W in OPT.items():
        rows=bouw(basis,W); A=np.array([list(r) for r in rows])
        d=np.argwhere(A!=B); buiten=[(x,y) for y,x in d if not (26<=x<=36 and 24<=y<=38)]
        print(n,'gewijzigd',len(d),'buiten zone',buiten,'alpha-diff',int(((A=='.')!=(B=='.')).sum()))
        open(f'opt_{n}.txt','w').write('\n'.join(rows)+'\n'); pal.topng(rows,f'opt_{n}.png')
