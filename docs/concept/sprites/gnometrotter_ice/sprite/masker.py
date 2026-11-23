# masker.py: figuurmasker voor het Ice-model. De gedeelde regel (achtergrond = min(R,G,B) >= 235) faalt bij ijs:
# het ijswit van muts, zolen en baard is zelf >= 235. Daarom: achtergrond = het met de beeldrand verbonden, neutrale bijna-wit
# (min >= 236 en max-min <= 6); alles wat de modellijn omsluit is figuur. Verder geometrie exact als reductie_gedeeld.py.
import numpy as np; from PIL import Image; from scipy import ndimage as nd
def masker(path):
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    kand=(a.min(2)>=236)&((a.max(2)-a.min(2))<=6)
    lab,_=nd.label(kand); rand=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(rand))
    sub=lab[120:165,555:587]; k=np.bincount(sub[sub>0]).argmax()
    h=lab==k   # ingesloten gat tussen mutspunt-ijspegels en rugkam (x 555-586, y 120-164; in Rock r8 ook een gat)
    return a,~(bg|h)
if __name__=='__main__':
    a,fg=masker('../r3/gemini_r3_lijf.png'); ys,xs=np.where(fg); print('ice fg',fg.sum(),xs.min(),xs.max(),ys.min(),ys.max())
    r=np.asarray(Image.open('../../gnometrotter_rock/r8/gemini_r8.png').convert('RGB')).astype(int); rf=r.min(2)<235
    print('rock fg',rf.sum(),'xor',(rf^fg).sum(),'ice-only',(fg&~rf).sum(),'rock-only',(rf&~fg).sum())
    im=np.zeros(fg.shape+(3,),'uint8')+255; im[fg&rf]=(120,120,120); im[fg&~rf]=(0,120,255); im[rf&~fg]=(255,0,0)
    Image.fromarray(im).crop((260,30,760,530)).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/93a3c7c6-21cb-5271-8439-b80d956b7343/scratchpad/maskcmp.png')
