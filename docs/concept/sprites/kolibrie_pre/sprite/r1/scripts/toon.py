import sys,numpy as np; from PIL import Image
PAL=[tuple(map(int,l.split())) for l in open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/kolibrie_pre/af/normal.pal').read().split('\n')[3:19]]
def rgba(A):
    im=np.zeros(A.shape+(4,),'uint8')
    for i,c in enumerate(PAL):
        if i: im[A==i,:3]=c; im[A==i,3]=255
    return Image.fromarray(im,'RGBA')
if __name__=='__main__':
    ims=[]
    for f in sys.argv[2:]:
        im=rgba(np.load(f)) if f.endswith('.npy') else Image.open(f).convert('RGBA')
        ims.append(im)
    S=10; w=sum(i.width*S+10 for i in ims); h=max(i.height for i in ims)*S
    V=Image.new('RGBA',(w,h),(235,235,225,255)); x=0
    for i in ims: V.alpha_composite(i.resize((i.width*S,i.height*S),0),(x,0)); x+=i.width*S+10
    V.save(sys.argv[1])
