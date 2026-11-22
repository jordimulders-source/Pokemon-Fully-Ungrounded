import sys,numpy as np; from PIL import Image
sys.path.insert(0,'..'); from npy2png import save
PAL=[(152,208,160),(16,14,18),(42,40,44),(66,64,66),(104,100,98),(252,228,148),(206,162,88),
     (248,192,96),(210,134,52),(156,92,36),(96,52,20),(228,84,72),(180,36,44),(252,214,128)]
S=11.87; X0=138-0.5*S; Y0=107-1.2*S
def rgba(o,bg=(200,220,200,255)):
    im=Image.new('RGBA',(64,64),bg); px=im.load()
    for j in range(64):
        for i in range(64):
            if o[j,i]: px[i,j]=PAL[o[j,i]]+(255,)
    return im
def gezicht(o,z=16,box=(13,22,37,46)):
    return rgba(o).crop(box).resize(((box[2]-box[0])*z,(box[3]-box[1])*z),Image.NEAREST)
def modelgezicht(z=16,box=(13,22,37,46)):
    m=Image.open('../../referenties/model.png').convert('RGBA'); x0,y0,x1,y1=box
    return m.crop((int(X0+x0*S),int(Y0+y0*S),int(X0+x1*S),int(Y0+y1*S))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
if __name__=='__main__':
    o=np.load(sys.argv[1]); a=gezicht(o); b=modelgezicht()
    v=Image.new('RGBA',(a.width*2+10,a.height),(255,255,255,255)); v.paste(a,(0,0)); v.paste(b,(a.width+10,0)); v.save(sys.argv[2])
