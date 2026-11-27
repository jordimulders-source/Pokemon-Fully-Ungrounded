# afstand.png = r10a en r9a op 1x en 2x naast elkaar (wit), plus 3x om het te kunnen bekijken
import sys; from PIL import Image
def w(f):
    a=Image.open(f); a.info['transparency']=0; a=a.convert('RGBA'); B=Image.new('RGBA',a.size,(255,255,255,255)); B.alpha_composite(a); return B.convert('RGB')
A=w('sprite_r10/guarana2_r10a.png'); B=w('sprite_r9/guarana2_r9a.png')
T=Image.new('RGB',(2*(64+8)+2*(128+8)+8,136),'white'); x=4
for im,s in ((A,1),(B,1),(A,2),(B,2)):
    T.paste(im.resize((64*s,64*s),0),(x,4)); x+=64*s+8
T.save(sys.argv[1] if len(sys.argv)>1 else 'sprite_r10/afstand.png')
