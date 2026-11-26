# Vergroot een uitsnede met rasterlijnen elke 10 px en coördinaatlabels.
import sys; from PIL import Image, ImageDraw
src,dst=sys.argv[1],sys.argv[2]; x0,y0,x1,y1,s=map(int,sys.argv[3:8])
im=Image.open(src).convert('RGB').crop((x0,y0,x1,y1)); im=im.resize((im.width*s,im.height*s),Image.NEAREST)
c=Image.new('RGB',(im.width+30,im.height+14),'white'); c.paste(im,(30,14)); d=ImageDraw.Draw(c)
for x in range(x0,x1+1):
    if x%10==0: X=30+(x-x0)*s; d.line([(X,14),(X,c.height)],fill=(255,0,0) if x%50==0 else (0,160,255)); d.text((X+1,1),str(x),fill='black')
for y in range(y0,y1+1):
    if y%10==0: Y=14+(y-y0)*s; d.line([(30,Y),(c.width,Y)],fill=(255,0,0) if y%50==0 else (0,160,255)); d.text((1,Y+1),str(y),fill='black')
c.save(dst)
