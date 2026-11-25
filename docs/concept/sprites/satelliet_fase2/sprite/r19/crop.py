from PIL import Image,ImageDraw; import sys
M=Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB'); k=12.703
x0,x1,y0,y1,s,out=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]),sys.argv[6]
box=(int(103+x0*k),int(143+(y0-7)*k),int(103+x1*k),int(143+(y1-7)*k))
c=M.crop(box); c=c.resize((int(c.width*s),int(c.height*s)),Image.NEAREST); d=ImageDraw.Draw(c)
for x in range(x0,x1+1):
  X=round((103+x*k-box[0])*s); d.line([(X,0),(X,c.height)],fill=(255,0,0) if x%5==0 else (0,200,0)); d.text((X+2,2),str(x),fill=(255,0,0))
for y in range(y0,y1+1):
  Y=round((143+(y-7)*k-box[1])*s); d.line([(0,Y),(c.width,Y)],fill=(255,0,0) if y%5==0 else (0,200,0)); d.text((2,Y+2),str(y),fill=(255,0,0))
c.save(out)
