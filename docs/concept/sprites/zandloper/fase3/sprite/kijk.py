import sys, numpy as np; from PIL import Image; import maak_r1 as m, bewerk
def op_wit(im,s):
    im=im.convert('RGBA'); b=Image.new('RGBA',im.size,(255,255,255,255)); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST)
def model64():
    a=Image.open('../gemini/r5.webp').convert('RGB'); # zelfde uitsnede als sprite: natief (2..,8..) -> 1024
    x0=(0*3+2)*5.12-0.12; y0=(2*3+2)*5.12-0.12
    return a.crop((int(x0),int(y0),int(x0+64*15.36),int(y0+64*15.36))).resize((64,64),Image.BOX)
if __name__=='__main__':
    ims=[op_wit(Image.open(p),6) for p in sys.argv[2:]]+[op_wit(model64(),6)]
    c=Image.new('RGB',(len(ims)*390,384),'white')
    for i,im in enumerate(ims): c.paste(im,(i*390,0))
    c.save(sys.argv[1])
