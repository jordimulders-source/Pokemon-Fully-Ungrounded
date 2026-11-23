# toon.py in.npy out.png zoom : palet-render
import sys,numpy as np; from PIL import Image
sys.path.insert(0,'../sprite_r6'); from palet import PAL
a=np.load(sys.argv[1]); z=int(sys.argv[3]) if len(sys.argv)>3 else 8
Image.fromarray(np.array([(200,230,200)]+PAL[1:],'uint8')[a]).resize((a.shape[1]*z,a.shape[0]*z),Image.NEAREST).save(sys.argv[2])
