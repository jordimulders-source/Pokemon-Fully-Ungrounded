# vel r2: r2 | r1 | model op 8x; kop 12x: r2 | r2 met Jordi's lijnen | model (vergroot gezicht) | Jordi's uitsnede; hele sprite 1x
import sys,re; sys.path.insert(0,'.'); from gemeen import *; from PIL import Image, ImageDraw
o=np.load('pachamama_r2.npy'); MY,MX=np.load('basis_map.npy')
def rgb(o,bg=(255,255,255)): return Image.fromarray(np.array([[bg if v==0 else PAL[v] for v in r] for r in o],np.uint8))
r2=rgb(o).resize((512,512),Image.NEAREST); r1=Image.open('../r1/pachamama_r1_8x.png').convert('RGB')
M=Image.open('../../referenties/gemini_gekozen_r7.png').convert('RGB'); PX,FX,PY,FY=5.704,5.16,5.692,3.088
md=Image.new('RGB',(int(192*PX),int(192*PY)),'white'); md.paste(M,(int(-(FX+MX*PX)),int(-(FY+MY*PY)))); md=md.resize((512,512),Image.LANCZOS)
y0,y1,x0,x1=8,34,17,44; S=12
kop=rgb(o[y0:y1,x0:x1]).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
lab=kop.copy(); d=ImageDraw.Draw(lab)
L=eval(re.sub(r'#.*','',open('lijnen.txt').read()))
KL={'oogkas L':(255,0,0),'oogkas R':(255,120,0),'neus':(0,160,255),'mond':(0,200,0),'wang L':(200,0,200),'wang R':(140,0,255)}
for n,pts in L.items():
  for (y,x) in pts: d.rectangle([(x-x0)*S+1,(y-y0)*S+1,(x-x0+1)*S-2,(y-y0+1)*S-2],outline=KL[n],width=2)
yy=4
for n,c in KL.items(): d.rectangle([2,yy,10,yy+8],fill=c); d.text((13,yy-1),n,fill=c); yy+=11
mg=Image.open('../natief_g1.png').crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize(kop.size,Image.NEAREST)
jc=Image.open('../../referenties/jordi_smokkelzone_hoofd.png').convert('RGB'); jc=jc.resize((int(jc.width*kop.height/jc.height),kop.height),Image.LANCZOS)
W=3*kop.width+jc.width+30
vel=Image.new('RGB',(max(W,1556),20+512+20+kop.height+200),(235,235,235)); dv=ImageDraw.Draw(vel)
for i,(im,t) in enumerate(((r2,'r2 8x'),(r1,'r1 8x'),(md,'model r7 (zelfde schaal)'))): vel.paste(im,(i*522,20)); dv.text((i*522+4,4),t,fill=0)
yk=552+14; dv.text((4,yk-14),"kop 12x | Jordi's lijnen benoemd | model met vergroot gezicht | Jordi's uitsnede",fill=0)
vel.paste(kop,(0,yk)); vel.paste(lab,(kop.width+10,yk)); vel.paste(mg,(2*kop.width+20,yk)); vel.paste(jc,(3*kop.width+30,yk))
y2=yk+kop.height+20
for i,bg in enumerate(((255,255,255),(248,248,240),(40,40,48),(0,0,0))):
  t=rgb(o,bg); vel.paste(t.resize((128,128),Image.NEAREST),(i*140,y2)); vel.paste(t,(600+i*80,y2+30))
dv.text((600,y2+10),'1x',fill=0)
vel.save('vel.png'); print(vel.size)
