# Paletten r7 (index = klasse). Eén donkere reeks met stappen >=25-30 en koel-blauw (Gen 3-zwart = blauwzwart); idx 4 (D2) is samengevoegd met D3 en ongebruikt.
NAMEN=['_','O','D0','D1','D2','D3','D4','R1','R2','R3','K1','K2','K3','W']
VAST={'_':(152,208,160),'K1':(255,166,181),'K2':(191,105,120),'K3':(115,63,72),'W':(252,252,252)}
VARIANT={
 # r7: hooglicht ±128 / licht ±100 / midden ±67 / donker ±40 / lijn ±17; rood met grotere stappen, donkerste rood naar paars (±330°)
 'r7':       {'O':(16,16,28),'D0':(120,128,160),'D1':(92,100,132),'D2':(58,64,92),'D3':(58,64,92),'D4':(34,38,60),'R1':(216,76,100),'R2':(168,40,72),'R3':(100,22,62)},
 # r7_donker: zelfde reeks, ±12-14 donkerder
 'r7_donker':{'O':(10,10,20),'D0':(104,112,146),'D1':(78,86,118),'D2':(46,52,80),'D3':(46,52,80),'D4':(24,26,46),'R1':(204,66,92),'R2':(156,34,66),'R3':(90,18,56)},
}
def pal(v):
    d=dict(VAST); d.update(VARIANT[v]); return [d[n] for n in NAMEN]
if __name__=='__main__':
    for v in VARIANT: print(v,[(n,round(.299*c[0]+.587*c[1]+.114*c[2])) for n,c in zip(NAMEN,pal(v)) if n not in('_','D2')])
