import sys,numpy as np; from PIL import Image
sys.path.insert(0,'.')
PAL=[(0,0,0),(14,12,14),(40,38,40),(62,60,60),(96,92,88),(250,238,204),(214,186,128),(246,190,96),(206,130,52),(148,90,34),(90,50,16),(206,66,60),(128,30,32),(255,140,120),(0,0,0),(0,0,0)]
def save(o,fn,pal=PAL):
    im=Image.fromarray(o.astype('uint8'),'P'); p=[c for t in pal for c in t]; im.putpalette(p+[0]*(768-len(p))); im.save(fn,transparency=0)
if __name__=='__main__': save(np.load(sys.argv[1]),sys.argv[2])
