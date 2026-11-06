cd "$(dirname "$0")" && python3 maak.py raster.txt && python3 palet.py raster.txt potoo.png && python3 -c "
from PIL import Image
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/279ed44b-aa1d-54e2-8396-02fa8e081036/scratchpad/pt/'
im=Image.open('potoo.png').convert('RGB'); r1=Image.open('../ronde1/potoo.png').convert('RGB')
W=Image.new('RGB',(512+20+128+64+40,512),(150,200,160))
W.paste(im.resize((512,512),Image.NEAREST),(0,0)); W.paste(im.resize((128,128),Image.NEAREST),(532,0)); W.paste(im,(680,0)); W.paste(r1,(680,80))
src=Image.open('/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/poppetje/ronde14_spritehoek.png').convert('RGB').resize((128,128),Image.LANCZOS); W.paste(src,(532,140))
W.save(S+'cur.png')"
