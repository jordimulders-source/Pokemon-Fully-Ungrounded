# Kopmasker in natieve coördinaten: vloedvulling vanaf het gezicht over niet-zwarte pixels, binnen ellips hd<1.12 (zodat de vulling
# niet via een bolletje dat zonder zwarte lijn tegen de kop ligt naar buiten lekt), plus de zwarte kopomlijning die eraan grenst.
import sys, numpy as np
sys.path.insert(0,'claydol_sprite_r1'); from klassen import klasse
def kopmasker(k):
    H,W=k.shape; yy,xx=np.mgrid[0:H,0:W]; hd=((xx-48.5)/24.0)**2+((yy-39.75)/16.5)**2
    ok=(k>0)&(k!=10)&(hd<1.12); m=np.zeros((H,W),bool); st=[(40,48)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and ok[y,x] and not m[y,x]: m[y,x]=True; st+=[(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    r=m.copy()
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
        r|=np.roll(np.roll(m,dy,0),dx,1)&(k==10)
    return r
if __name__=='__main__':
    k,a=klasse('claydol_sprite_r2/model_r2_s2.png'); m=kopmasker(k); s='.123456789KABR'
    for y in range(10,58): print('%2d '%y+''.join((s[k[y,x]].lower() if k[y,x]==10 else '#') if m[y,x] else s[k[y,x]] for x in range(12,88)))
