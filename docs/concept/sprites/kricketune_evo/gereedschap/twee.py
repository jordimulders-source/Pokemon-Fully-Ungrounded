# twee.py SPRITE.png UIT.png [ANDER.png]: sprite 10x naast het model (1024, zelfde hoogte) [en een tweede sprite]
import sys; sys.path.insert(0,'gereedschap'); from PIL import Image; from gemeen import *
sp=[rgb(laden(p),(255,255,255)).resize((640,640),Image.NEAREST) for p in [sys.argv[1]]+sys.argv[3:]]
M=Image.open(MODEL).convert('RGB'); px=lambda x:9.75+10.24*(U0+(x-X0)*75/56); py=lambda y:9.75+10.24*(V0+(y-Y0)*85/64)
m=M.crop((int(px(0)),int(py(0)),int(px(64)),int(py(64)))).resize((640,640),Image.LANCZOS)
W=Image.new('RGB',(650*(len(sp)+1),640),'white')
for i,s in enumerate(sp): W.paste(s,(i*650,0))
W.paste(m,(len(sp)*650,0)); W.save(sys.argv[2])
