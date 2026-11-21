# Palet (index = klasse). MODEL = k-means-centra gemeten op het natieve raster (km_c.npy, K=16); dicht bij elkaar liggende centra samengevoegd.
# L = donkergroene binnenlijn van het model (km 2+3), O = zwarte lijn (km 0+1).
NAMEN=['_','O','L','G1','G2','G3','G4','G5','K3','K2','K1','K0','Y2','Y1','W']
MODEL={'_':(152,208,160),'O':(16,22,20),'L':(33,82,50),
 'G1':(106,186,118),'G2':(84,160,100),'G3':(72,151,92),'G4':(62,141,79),'G5':(45,108,69),
 'K3':(140,62,76),'K2':(201,106,124),'K1':(239,154,171),'K0':(243,184,193),
 'Y2':(95,110,49),'Y1':(207,193,79),'W':(252,252,252)}
KM={0:'O',1:'O',2:'L',3:'L',4:'G5',5:'K3',6:'Y2',7:'G4',8:'G3',9:'G2',10:'K2',11:'G1',12:'G1',13:'K1',14:'Y1',15:'K0'}
FILL=['G1','G2','G3','G4','G5','K3','K2','K1','K0','Y2','Y1']
I={n:i for i,n in enumerate(NAMEN)}
# SPRITE: kleur mag van het model afwijken (Jordi 17 nov). Groenen gespreid naar Gen 3-stappen (helderheid ±178/146/119/97/75, lijn 52);
# volgorde en verhouding van het model blijven: lijf (G1) duidelijk lichter dan de waaier (G4/G5), zoals gemeten (model 172 vs 89-120).
SPRITE=dict(MODEL); SPRITE.update({'G1':(124,204,132),'G2':(92,172,104),'G3':(68,144,84),'G4':(52,118,70),'G5':(36,92,58),'L':(24,64,40),'O':(16,20,24),
 'Y2':(168,150,52)})
def pal(d=SPRITE): return [d[n] for n in NAMEN]
