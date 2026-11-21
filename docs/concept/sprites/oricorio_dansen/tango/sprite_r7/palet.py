# Paletten (index = klasse). MODEL = gemeten k-means-centra op het natieve raster. Roze = Gen 3 Oricorio (Pa'u/Pom-Pom-roze), wit = glimpje.
NAMEN=['_','O','D0','D1','D2','D3','D4','R1','R2','R3','K1','K2','K3','W']
VAST={'_':(152,208,160),'K1':(255,166,181),'K2':(191,105,120),'K3':(115,63,72),'W':(252,252,252)}
MODEL={'O':(2,2,4),'D0':(89,92,99),'D1':(66,68,74),'D2':(56,57,62),'D3':(42,43,48),'D4':(31,32,36),'R1':(158,78,93),'R2':(149,41,60),'R3':(90,20,30)}
VARIANT={
 # A: zo dicht bij het bijna-zwarte model als leesbaar is (blauwzwart zoals Umbreon/Murkrow, stappen ±14)
 'A_donker':{'O':(14,14,20),'D0':(104,106,126),'D1':(76,78,96),'D2':(62,63,80),'D3':(46,47,62),'D4':(32,33,44),'R1':(184,52,76),'R2':(150,34,58),'R3':(98,18,36)},
 # B: één stap lichter (Gen 3-leesbaarheid, Umbreon-niveau)
 'B_lichter':{'O':(16,16,24),'D0':(128,130,154),'D1':(96,98,120),'D2':(78,79,100),'D3':(60,61,80),'D4':(42,43,58),'R1':(208,72,96),'R2':(168,40,66),'R3':(104,20,40)},
}
def pal(v):
    d=dict(VAST); d.update(MODEL if v=='model' else VARIANT[v]); d['R1']=d.get('R1',(200,64,88))
    return [d[n] for n in NAMEN]
