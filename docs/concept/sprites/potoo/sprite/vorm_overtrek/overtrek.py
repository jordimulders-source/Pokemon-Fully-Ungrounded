"""Overtrek hele vorm op de gespiegelde leidraad (punten met de hand afgelezen op 3x met 10-px-raster, fotocoördinaten 640x720).
Lijnen: buitenomtrek (tot de stomp), bekrand (uit bekrand_overtrek), oog, wang/halsrand, rand nabije vleugel/schouder."""
import json, sys
sys.path.insert(0,'../bekrand_overtrek')
from overtrek import P as BEK, OOG, cr
from PIL import Image, ImageDraw
# buitenomtrek, met de klok mee vanaf de snavelpunt (bovenrand bek)
KOP=[(123,246),(126,236),(131,220),(141,200),(156,179),(173,157),(192,139),(212,126),(234,116),(257,111),(282,112),(308,117),
     (334,124),(358,133),(380,145),(398,157),(418,174),(440,199),(460,224),(480,247),(500,268),(512,288),(519,308),(526,333),
     (532,360),(535,387),(535,413),(537,447),(537,480),(536,513),(535,547),(533,572),(532,585)]
STOMP=[(500,582),(460,580),(430,586),(400,592),(375,598),(350,605),(327,611),(310,622),(300,630),(280,633),(262,633),(252,631)]
KIN=[(246,615),(243,600),(240,583),(237,567),(235,550),(233,533),(232,515),(232,500),(231,483),(231,468),(232,456)]
BUITEN=KOP+STOMP+KIN+BEK[26:]+BEK[:1]
# wang/halsrand: vanaf de mondhoek onder het oog langs de rechterkant van de muil, door de hals omlaag (grens donkere keel / lichte borst-schouder)
HALS=[(312,282),(322,300),(334,322),(343,345),(347,368),(346,390),(342,412),(338,435),(334,458),(330,482),(326,506),(322,530),(319,553),(320,575),(326,596),(332,608)]
# rand nabije vleugel/schouder tegen de borst
VLEUGEL=[(440,302),(458,298),(478,298),(498,301),(516,305)]
VLEUGEL2=[(440,302),(443,325),(447,350),(452,375),(458,400),(466,425),(475,450),(483,475),(490,500),(495,525),(498,550),(500,578)]
def schaal(pts,s,dx=0,dy=0): return [(x*s+dx,y*s+dy) for x,y in pts]
LIJNEN=[('buitenomtrek',BUITEN,True,(255,200,0)),('bekrand',BEK,True,(0,230,255)),('halsrand',HALS,False,(255,60,200)),
        ('vleugel_boven',VLEUGEL,False,(80,255,80)),('vleugel_borst',VLEUGEL2,False,(80,255,80))]
def teken(im,s,dx=0,dy=0,w=3,wit=False):
    d=ImageDraw.Draw(im)
    for n,pts,closed,col in LIJNEN:
        c=cr(pts,closed=closed)
        if not closed: c=c+[pts[-1]]
        c=schaal(c,s,dx,dy)
        if wit: col=tuple(int(v*0.75) for v in col)
        d.line(c+([c[0]] if closed else []),fill=col,width=w,joint='curve')
    ox,oy,rx,ry=OOG; d.ellipse([(ox-rx)*s+dx,(oy-ry)*s+dy,(ox+rx)*s+dx,(oy+ry)*s+dy],outline=(255,40,40),width=w)
if __name__=='__main__':
    json.dump({'fotocoördinaten':'gespiegelde linkerhelft van jordi_great_potoo_bek_open_duo.webp, 640x720',
               'buitenomtrek':BUITEN,'bekrand':BEK,'oog':OOG,'halsrand':HALS,'vleugel_boven':VLEUGEL,'vleugel_borst':VLEUGEL2,
               'opmerking':'onder de stomp (staart, onderlijf) staat de vogel niet op deze foto'},open('overtrek.json','w'),indent=1)
    foto=Image.open('../bekrand_overtrek/leidraad_gespiegeld.png').convert('RGB'); S=800/720
    F=foto.resize((int(640*S),800),Image.LANCZOS); a=F.copy(); teken(a,S)
    w=Image.new('RGB',F.size,(255,255,255)); teken(w,S,wit=True)
    W=Image.new('RGB',(F.size[0]*2+20,800),(235,235,240)); W.paste(a,(0,0)); W.paste(w,(F.size[0]+20,0))
    d=ImageDraw.Draw(W)
    d.text((10,770),'geel buitenomtrek (tot de stomp)  cyaan bekrand  rood oog  roze wang/halsrand  groen nabije vleugel/schouder',fill=(255,255,255))
    d.text((F.size[0]+30,770),'zelfde lijnen op wit; staart/onderlijf onder de stomp niet zichtbaar op de foto',fill=(0,0,0))
    W.save('vorm_op_foto.png')
    for i,(x0,y0,x1,y1) in enumerate([(110,90,400,270),(340,120,600,420),(200,380,460,660),(380,360,600,660)]):
        c=foto.crop((x0,y0,x1,y1)).resize(((x1-x0)*3,(y1-y0)*3),Image.LANCZOS); teken(c,3,-x0*3,-y0*3,w=2)
        c.save(f'/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/279ed44b-aa1d-54e2-8396-02fa8e081036/scratchpad/r3/v{i}.png')
    print(len(BUITEN),'punten buitenomtrek')
