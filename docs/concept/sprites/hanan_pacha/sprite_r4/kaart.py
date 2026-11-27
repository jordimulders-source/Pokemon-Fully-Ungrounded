# Spritepixel (X,Y) -> natief 2x2-blok (linksboven) via dezelfde stappen als r3 (fase 1,1; figuurbox; geschrapte rijen/kolommen).
import numpy as np
H=np.load('../sprite_r3/half_11.npy'); ys,xs=np.where(H>=0); Y0,X0=ys.min(),xs.min(); FH,FW=ys.max()-Y0+1,xs.max()-X0+1
ROWS=[3,9,16,44,49,52,57,61,66,69]; COLS=[6,34,38,54,61,64]
kr=np.delete(np.arange(FH),ROWS); kc=np.delete(np.arange(FW),COLS)   # 64 elk
def blok(X,Y):
    hy=kr[Y]+Y0; hx=kc[X]+X0; return 1+2*hx,1+2*hy   # natieve x,y
