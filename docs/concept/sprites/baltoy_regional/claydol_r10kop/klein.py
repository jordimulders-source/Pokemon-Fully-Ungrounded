# tintvlakjes < 3 px (4-buren) binnen de kopzone
import sys, numpy as np; from PIL import Image
from lagen import masks
def klein(S):
    kop,kin,bol,punt=masks(); seen=np.zeros(S.shape,bool); out=[]
    for y,x in zip(*np.where(kin)):
        if seen[y,x]: continue
        v=S[y,x]; st=[(y,x)]; comp=[]; seen[y,x]=True
        while st:
            a,b=st.pop(); comp.append((a,b))
            for c,d in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if 0<=c<64 and 0<=d<64 and not seen[c,d] and S[c,d]==v: seen[c,d]=True; st.append((c,d))
        if len(comp)<3: out.append((int(v),[(int(a),int(b)) for a,b in comp]))
    return out
if __name__=='__main__':
    for v,c in klein(np.array(Image.open(sys.argv[1]))): print(v,c)
