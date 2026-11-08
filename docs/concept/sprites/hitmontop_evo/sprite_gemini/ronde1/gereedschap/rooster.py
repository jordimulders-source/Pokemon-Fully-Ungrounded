# rooster.py x0 y0 x1 y1 zoom uit.png : alleen het model (ingekort) met spritepixelrooster, labels op veelvouden van 5
import sys,json; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde1/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
if len(sys.argv)>7: k['model']=sys.argv[7]
mo=Image.open(G+k['model']); bg=Image.new('RGBA',mo.size,(152,208,160,255)); bg.alpha_composite(mo); bg=bg.convert('RGB')
x0,y0,x1,y1,z=map(int,sys.argv[1:6])
c=bg.crop((int(X0+x0*s),int(Y0+y0*s),int(X0+x1*s),int(Y0+y1*s))).resize(((x1-x0)*z,(y1-y0)*z),Image.LANCZOS)
d=ImageDraw.Draw(c)
for x in range(x0,x1+1): d.line([((x-x0)*z,0),((x-x0)*z,c.size[1])],fill=(255,0,0) if x%5==0 else (255,190,190))
for y in range(y0,y1+1): d.line([(0,(y-y0)*z),(c.size[0],(y-y0)*z)],fill=(255,0,0) if y%5==0 else (255,190,190))
for x in range((x0+4)//5*5,x1,5): d.text(((x-x0)*z+2,2),str(x),fill=(0,0,255))
for y in range((y0+4)//5*5,y1,5): d.text((2,(y-y0)*z+2),str(y),fill=(0,0,255))
c.save(sys.argv[6])
