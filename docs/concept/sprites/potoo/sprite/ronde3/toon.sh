cd "$(dirname "$0")" && python3 maak.py raster.txt && python3 palet.py raster.txt potoo.png && python3 ../controle.py raster.txt ../ronde2/raster.txt > controle.txt && python3 -c "
from PIL import Image
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/279ed44b-aa1d-54e2-8396-02fa8e081036/scratchpad/r3/'
im=Image.open('potoo.png').convert('RGBA')
W=Image.new('RGB',(512+20+128+20+64,512),(150,200,160))
W.paste(im.resize((512,512),Image.NEAREST),(0,0),im.resize((512,512),Image.NEAREST)); b=im.resize((128,128),Image.NEAREST); W.paste(b,(532,0),b); W.paste(im,(680,0),im)
W.save(S+'cur.png')"
