# Ronde 9: gezichtsreparaties uit r8/keuring.md op basis van welp_r8 (spritecoordinaten; keuring 64x64: x+7, y+18).
import numpy as np, sys
r8=np.load('welp_r8.npy')
CH='.KdSMLPQRgWCTGHU'; IX={c:i for i,c in enumerate(CH)}
a=r8.copy(); log={}
def zet(naam,pix,c):
    n=0
    for x,y in pix:
        if a[y,x]!=IX[c]: a[y,x]=IX[c]; n+=1
    log[naam]=log.get(naam,0)+n
TAND2=len(sys.argv)>1 and sys.argv[1]=='tand2'
# MOET 1 mondhoek zonder zwarte haak: mond loopt naar onder af
zet('mondhoek',[(10,16),(11,16)],'S'); zet('mondhoek',[(11,15)],'M'); zet('mondhoek',[(11,17)],'d')
# MOET 2 tong krult naar links over de poot: rand dicht, tip 3 px (x4-6), buitenlijn links van de tip
zet('tong',[(4,19),(3,21),(3,22)],'d'); zet('tong',[(4,21),(4,22)],'T')
# MOET 3 een glans in het oog (linksboven de pupil)
zet('oog',[(13,9)],'g')
# MAG binnenlijn band doortrekken naar rechts
zet('band_lijn',[(13,3),(14,3)],'P')
# MAG mondlijn taps naar de snuitpunt, neusrand een lijntype
zet('mondlijn',[(4,17)],'d'); zet('neusrand',[(2,14)],'d')
# MAG tweede ondertand (alleen als variant; zie rapport)
if TAND2: zet('ondertand2',[(10,20)],'W')
np.save('welp_r9.npy' if not TAND2 else 'welp_r9_tand2.npy',a)
print(log,'totaal diff r8:',int((a!=r8).sum()),'silhouet-diff:',int(((a>0)!=(r8>0)).sum()))
