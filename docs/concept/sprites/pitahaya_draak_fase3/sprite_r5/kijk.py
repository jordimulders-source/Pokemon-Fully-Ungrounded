# Snelle blik: sprites naast elkaar op 1x, 2x en 6x op lichtgrijs. Gebruik: kijk.py UIT.png A.png [B.png ...]
import sys; from PIL import Image
fs=sys.argv[2:]; ims=[Image.open(f).convert('RGBA') for f in fs]
W=len(ims)*(64*6+10)+64*3+20; out=Image.new('RGB',(W,64*6),(225,225,225))
for i,im in enumerate(ims):
    out.paste(im.resize((384,384),Image.NEAREST),(i*394,0),im.resize((384,384),Image.NEAREST))
    out.paste(im,(len(ims)*394,i*70),im); b=im.resize((128,128),Image.NEAREST); out.paste(b,(len(ims)*394+70,i*130),b)
out.save(sys.argv[1])
