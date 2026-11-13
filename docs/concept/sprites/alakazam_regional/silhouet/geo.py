# gedeelde geometrie: spritepixel (X,Y) <-> modelpixels van referenties/model_silhouet.png
import numpy as np
from PIL import Image
import os
D=os.path.dirname(os.path.abspath(__file__))+'/../'
S=851/62.5            # modelpixels per spritepixel
OX=163-4*S; OY=102-1*S
def model(): return np.asarray(Image.open(D+'referenties/model_silhouet.png').convert('RGB')).astype(int)
def blok(X,Y): return int(OY+Y*S),int(OY+(Y+1)*S),int(OX+X*S),int(OX+(X+1)*S)
