# Spriteklassen (index = paletindex). MODEL = gemeten k-means-centra (natief raster); GEN3 = de sprite-tinten.
NAMEN=['_','O','G1','G2','G3','G4','Y1','Y2','Y3','B1','B2','K1','K2','K3','W']
# k-means-klasse (km.py, K=22, op helderheid) -> spriteklasse
KL={0:'O',1:'G4',2:'Y3',3:'G4',4:'K3',5:'B1',6:'G3',7:'G3',8:'Y3',9:'G3',10:'G2',11:'G2',12:'K2',13:'G2',14:'Y2',15:'G1',16:'G1',17:'Y1',18:'K1',19:'Y1',20:'Y1',21:'Y1'}
MODEL={'_':(255,255,255),'O':(4,7,4),'G1':(88,181,104),'G2':(80,170,93),'G3':(56,141,75),'G4':(30,82,37),
       'Y1':(244,212,62),'Y2':(173,150,26),'Y3':(120,105,15),'B1':(56,92,166),'B2':(40,60,120),
       'K1':(242,162,174),'K2':(198,106,122),'K3':(140,65,76),'W':(252,252,252)}
# Gen 3-tinten (stappen ±30-40 in helderheid; licht linksboven). Roze = Gen 3 Oricorio-roze (zelfde als tango/cumbia).
GEN3={'_':(152,208,160),'O':(16,24,16),
      'G1':(136,216,112),'G2':(80,176,88),'G3':(48,128,64),'G4':(24,80,40),
      'Y1':(248,232,96),'Y2':(232,184,48),'Y3':(168,120,24),
      'B1':(80,120,216),'B2':(40,64,152),
      'K1':(255,166,181),'K2':(191,105,120),'K3':(115,63,72),'W':(252,252,252)}
def pal(v='gen3'):
    d=MODEL if v=='model' else GEN3
    return [d[n] for n in NAMEN]
