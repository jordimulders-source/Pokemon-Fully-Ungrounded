import sys, numpy as np; from PIL import Image
PAL=[16,32,64,96,112,144,208,248]  # r4: pak donker 32/64/96 + zwart 16; 4 = selout 112 (en hooglicht pak/hoed)
def rgb(C,bg=(152,208,160)):
    img=np.zeros(C.shape+(3,),'uint8'); img[:]=bg
    for i,t in enumerate(PAL): img[C==i]=t
    return img
if __name__=='__main__':
    C=np.load(sys.argv[1]); z=int(sys.argv[3]) if len(sys.argv)>3 else 8
    Image.fromarray(rgb(C)).resize((C.shape[1]*z,C.shape[0]*z),0).save(sys.argv[2])
