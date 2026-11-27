# Palette swaps richting fase 2 v8: alleen paletwaarden per groep, pixels identiek aan kuiken_r1.png
import numpy as np; from PIL import Image
from lib import PAL, opslaan
S=np.array(Image.open('kuiken_r1.png'))
STEEN=[(76,70,64),(104,97,89),(176,168,154)]          # fase 2 v8 snavel
ANTR=[(40,40,44),(70,68,72),(108,102,100)]            # fase 2 v8 lijf
BEIGE=[(78,68,57),(148,129,105),(224,189,149)]        # fase 2 v8 poten
def pal(snavel=None,bruin=None,creme=None,poten=None):
    p=list(PAL)
    for idx,new in ((range(2,5),snavel),(range(5,8),bruin),(range(8,11),creme),(range(11,14),poten)):
        if new:
            for i,c in zip(idx,new): p[i]=c
    return p
SW={
 'sA':pal(STEEN,ANTR,None,BEIGE),                                          # steen + antraciet lijf, creme, beige poten
 'sB':pal(STEEN,[(40,40,44),(70,68,72),(158,111,90)],None,[(78,68,57),(148,129,105),(192,120,84)]),  # antraciet + roest-tan gezicht (licht bruin), roest-oranje tenen
 'sC':pal(STEEN,[(52,42,40),(82,66,58),(124,98,82)],[(150,104,82),(178,130,102),(214,172,138)],BEIGE), # donker umber + tan borst
 'sD':pal(STEEN,[(88,52,46),(126,72,58),(158,111,90)],None,[(78,68,57),(148,129,105),(192,120,84)]),   # roest overal (roest donker/rood-bruin/tan), creme borst
}
if __name__=='__main__':
    for k,p in SW.items():
        opslaan(S,'kuiken_r1_%s.png'%k,p)
        assert (np.array(Image.open('kuiken_r1_%s.png'%k))==S).all()
    print('swaps', list(SW))
