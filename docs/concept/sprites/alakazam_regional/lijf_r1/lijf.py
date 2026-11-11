# lijf_r1: herkleuropties voor de romp (x19-35, rij 25-45). Rijen beginnen bij x19, '=' = laten staan.
import pal,numpy as np
X0=19
O1={ # grijs als basis, wit borstplaat (Alakazam-borst), buik grijs, zwart flank/rug/platen
29:"kkmmmmmmwwaaawwao",
30:"kkmmmmmwwwwwwwwao",
31:"okmmmmmwwwwwwwwao",
32:"oommmmmwwwwwwwaoo",
33:"..ommmmcwwwwaaooo",
34:"..okmmmbcwaaaco..",
35:"oookmmbbbccccco..",
36:"kkokmmbbbbbbco...",
37:"kkokmbbbbbbbco...",
38:"kkoooobbbbbbco...",
39:"koobccdbbbbcco...",
40:"oobbccdbbbccdo...",
41:"oobbccdbbccdcco..",
42:"oobbccdcccdobbco.",
43:".obcccddddoobbcco",
}
O2=dict(O1); O2.update({ # als O1, flank vervaagt zwart -> grijs
29:"kkmmmmdcwwaaawwao",
30:"kkmmmdcwwwwwwwwao",
31:"okmmmdcwwwwwwwwao",
32:"oommmdcwwwwwwwaoo",
33:"..ommdccwwwwaaooo",
34:"..okmdcbcwaaaco..",
35:"oookmdcbbccccco..",
36:"kkokdcbbbbbbco...",
37:"kkodcbbbbbbbco...",
})
O3={ # Mr. Rime: zwart lijf, wit als ronde buikvlek (taille, ronde onderkant), grijs kruis
29:"kkmmmmmwwwaaawwao",
30:"kkmmmmwwwwwwwwwao",
31:"okmmmmwwwwwwwwwao",
32:"oommmmwwwwwwwwaoo",
33:"..ommmmwwwwwaaooo",
34:"..okmmmwwwwwaao..",
35:"oookmmmmwwwwaao..",
36:"kkokmmmmwwwwao...",
37:"kkokmmmmwwwwao...",
38:"kkoooommwwwaao...",
39:"koobccdmaaacco...",
40:"oobbccdcccccdo...",
41:"oobbccdbbccdcco..",
42:"oobbccdcccdobbco.",
43:".obcccddddoobbcco",
}
OPT={'O1':O1,'O2':O2,'O3':O3}
def bouw(basis,W):
    R=[list(r) for r in basis]
    for y,s in W.items():
        for i,c in enumerate(s):
            if c!='=': R[y][X0+i]=c
    return [''.join(r) for r in R]
def check(naam,rows,basis):
    A=np.array([list(r) for r in rows]); B=np.array([list(r) for r in basis])
    d=np.argwhere(A!=B); buiten=[(x,y) for y,x in d if not (19<=x<=35 and 25<=y<=45)]
    alpha=int(((A=='.')!=(B=='.')).sum())
    print(naam,'gewijzigd',len(d),'buiten zone',buiten,'alpha-diff',alpha)
if __name__=='__main__':
    import sys
    basis=pal.load('basis_r11.txt')
    from o4 import O4, BASIS4
    OPT['O4']=None
    for n in ['O1','O2','O3','O4']:
        rows=bouw(basis,OPT[n]) if n!='O4' else bouw(bouw(basis,OPT[BASIS4]),O4)
        open(f'opt_{n}.txt','w').write('\n'.join(rows)+'\n'); pal.topng(rows,f'opt_{n}.png'); check(n,rows,basis)
