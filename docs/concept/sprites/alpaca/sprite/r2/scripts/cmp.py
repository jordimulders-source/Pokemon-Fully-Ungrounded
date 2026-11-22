# Snelle vergelijking: natief model (zelfde schaal) | onderlaag | sprite, alle 8x
import numpy as np; from PIL import Image
oy,ox=np.load('plaats.npy'); Z=np.load('zones_nat.npy'); ys,xs=np.nonzero(Z!='.')
N=Image.open('natief.png').convert('RGB')
H,W=np.load('zone_t.npy').shape; s=(ys.max()+1-ys.min())/H
cx=(xs.min()+xs.max()+1)/2; bx=cx-W*s/2
M=N.crop((int(round(bx)),ys.min(),int(round(bx+W*s)),ys.max()+1)).resize((W*8,H*8),Image.LANCZOS)
O=Image.open('../onderlaag.png').convert('RGBA'); bg=Image.new('RGBA',O.size,(200,220,255,255)); bg.alpha_composite(O); O=bg.convert('RGB').resize((W*8,H*8),0)
S=Image.open('../palpaca.png').convert('RGBA').crop((ox,oy,ox+W,oy+H)); bg=Image.new('RGBA',S.size,(200,220,255,255)); bg.alpha_composite(S); S=bg.convert('RGB').resize((W*8,H*8),0)
v=Image.new('RGB',(W*8*3+20,H*8),(255,255,255)); v.paste(M,(0,0)); v.paste(O,(W*8+10,0)); v.paste(S,(W*16+20,0)); v.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/11438012-dfd6-59c7-8830-95f8039ed825/scratchpad/cmp.png')
