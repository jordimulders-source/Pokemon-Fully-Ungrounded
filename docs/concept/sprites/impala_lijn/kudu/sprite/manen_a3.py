# Manen A, ronde 3: herstel van A2a op modelniveau (r2-keuring: "kaarsrechte verticale snede" (x430-500) en "rechthoekig blok"
# (x430-500, y640-790)). Alleen modelmateriaal, alleen verschuiven/spiegelen:
# 1 kopie van het halsdeel van de r3b-manen (+70,+30), alleen links van x455 (daar ligt hij over de oude manen/hals)
# 2 over de schouder: de keelfranje van r3b (x190-300, y520-770: lokken die naar links-onder in punten eindigen, met hun
#   eigen zwarte lijn) horizontaal GESPIEGELD, zodat de lokpunten naar rechts-onder over de schouder vallen; geplaatst x455-565, y480-730 (bron y520-770)
# 3 de kamlokken van r3b (y<530, x>440) weer bovenop, zodat de bovenkant van de gespiegelde lokken onder de kam verdwijnt
# Geen ingesneden boog, geen strook, geen rechte snede. Uit: r3/model_A3.png, r3/model_A3_crop2x.png, r3/manen_A3.npy
import numpy as np
from PIL import Image
from scipy import ndimage as nd
from reduce import fgmask
from zones import pixzones
Ld=lambda n:np.asarray(Image.open(n).convert('RGB')).astype(int)
M=Ld('../referenties/model_r3b.png'); fg=fgmask(M); Zp,lum=pixzones(M,fg)
hb=np.load('haar_r3b.npy'); Hh,Ww=hb.shape; yy,xx=np.mgrid[:Hh,:Ww]
out=M.copy(); haar=hb.copy()
# 1 kopie halsdeel
kam=hb&(xx>440)&(yy<530)
DX,DY=70,30; XMAX=455
S=np.zeros_like(hb); S[DY:,DX:]=(hb&~kam)[:-DY,:-DX]; SV=np.zeros_like(M); SV[DY:,DX:]=M[:-DY,:-DX]
S&=fg&(xx<XMAX)
out[S]=SV[S]; haar|=S
# 2 gespiegelde keelfranje
SX0,SX1,SY0,SY1=190,300,520,770; TX=455; TY=480
asset=fg&((Zp==1)|(Zp==-1))
asset[:, :SX0]=False; asset[:, SX1+1:]=False; asset[:SY0]=False; asset[SY1+1:]=False
lab,n=nd.label(asset); asset=lab==np.bincount(lab[lab>0]).argmax()   # alleen de samenhangende franje (geen losse lijnstukjes van kin/borst)
ys,xs=np.nonzero(asset)
tx=TX+(SX1-xs); ty=TY+(ys-SY0)
ok=(tx<Ww)&(ty<Hh)&fg[ty,tx]
out[ty[ok],tx[ok]]=M[ys[ok],xs[ok]]; A_m=np.zeros_like(hb); A_m[ty[ok],tx[ok]]=True; haar|=A_m
# 3 kam weer bovenop
out[kam]=M[kam]
np.save('r3/manen_A3.npy',haar)
Image.fromarray(out.astype('uint8')).save('r3/model_A3.png')
Image.fromarray(out[380:800,360:600].astype('uint8')).resize((480,840),Image.NEAREST).save('r3/model_A3_crop2x.png')
print('kopie',int(S.sum()),'gespiegelde franje',int(ok.sum()))
