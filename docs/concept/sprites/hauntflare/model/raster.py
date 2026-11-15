# Toon een plaatje met rasterlijnen (elke 64 px) en labels, voor coordinaten
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGB'); x0,y0,x1,y1=map(int,sys.argv[3:7]) if len(sys.argv)>3 else (0,0,1024,1024)
im=im.crop((x0,y0,x1,y1)); s=float(sys.argv[7]) if len(sys.argv)>7 else 1
im=im.resize((int(im.width*s),int(im.height*s)),Image.NEAREST); d=ImageDraw.Draw(im)
st=int(sys.argv[8]) if len(sys.argv)>8 else 64
for x in range((x0//st)*st,x1,st):
    if x<x0: continue
    X=(x-x0)*s; d.line([(X,0),(X,im.height)],fill=(0,160,255)); d.text((X+2,2),str(x),fill=(0,0,255))
for y in range((y0//st)*st,y1,st):
    if y<y0: continue
    Y=(y-y0)*s; d.line([(0,Y),(im.width,Y)],fill=(0,160,255)); d.text((2,Y+2),str(y),fill=(0,0,255))
im.save(sys.argv[2])
