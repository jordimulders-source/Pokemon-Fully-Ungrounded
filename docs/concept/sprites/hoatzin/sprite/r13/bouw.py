# Hoatzin r13: DC-eindkeuring op r12 (alleen tinten binnen het silhouet, alpha-diff 0).
import os,numpy as np; from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(H+'/../r12/hoatzin_r12.png'); a=np.array(im).copy(); r12=a.copy()
def zet(lst,oud,nieuw,cat):
    for x,y in lst:
        assert a[y,x]==oud,(x,y,a[y,x]); a[y,x]=nieuw; log.append((cat,x,y,oud,nieuw))
log=[]
# Belijning: binnenlijnen (veerlijnen) in de opgeheven vleugel, geheel omringd door lijf: zwart -> donkerste eigen tint
zet([(40,16),(38,17),(42,17),(40,18)],1,2,'belijning')
# Schaduw vleugel: veerlijnen uit het model in de onderste helft (taps vanaf de schaduwsikkel naar binnen)
zet([(39,22),(38,24),(39,24),(37,27)],3,2,'schaduw')
# Schaduw vleugel: lichte voorrand doorgezet op de onderste veer (modelhelderheid 7-8)
zet([(32,26),(31,27),(30,28)],3,4,'schaduw')
# Hooglicht borst: druppel langs de borstbolling naar beneden (model x20-21, y33-34 helderheid 9)
zet([(20,33),(21,33),(20,34)],4,10,'schaduw')
assert ((a==0)==(r12==0)).all()
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.info['transparency']=0
out.save(H+'/hoatzin_r13.png',transparency=0)
w=np.array(out.convert('RGB')); w[a==0]=255; Image.fromarray(w).resize((512,512),0).save(H+'/hoatzin_r13_8x.png')
import collections; print(collections.Counter(c for c,*_ in log), 'diff',(a!=r12).sum(),'alpha-diff',((a==0)!=(r12==0)).sum(),'kleuren',len(np.unique(a))-1)
