# crop.py OUT x0 y0 x1 y1 schaal png...  (P-png's met transparantie, of RGB)
import sys; from PIL import Image
out,x0,y0,x1,y1,s=sys.argv[1],*map(int,sys.argv[2:7]); fs=sys.argv[7:]
w,h=(x1-x0)*s,(y1-y0)*s; O=Image.new('RGB',((w+6)*len(fs),h),(200,200,200))
for k,f in enumerate(fs):
    im=Image.open(f).convert('RGBA').crop((x0,y0,x1,y1)).resize((w,h),0); O.paste(im,(k*(w+6),0),im)
O.save(out)
