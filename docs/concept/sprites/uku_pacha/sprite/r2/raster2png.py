# tekstraster -> geïndexeerde png (index 0 = transparant)
import sys; from PIL import Image
PAL={'.':(255,255,255),'K':(16,20,28),'n':(36,50,76),'d':(66,78,102),'g':(77,87,98),'h':(130,164,200),'s':(82,102,132),
'm':(108,130,158),'b':(112,150,172),'l':(119,175,186),'p':(156,212,212),'w':(194,235,230),
'B':(75,108,148),'D':(44,73,111),'Y':(226,196,72),'P':(132,96,148),'W':(244,248,248)}
ORDE='.KndhsmblpwBDYPW'
def lees(f): return [l.rstrip('\n') for l in open(f)][:64]
def maak(R,pal=PAL):
    im=Image.new('P',(64,64),0)
    flat=[]
    for c in ORDE: flat+=list(pal[c])
    im.putpalette(flat+[0]*(768-len(flat)))
    for y,r in enumerate(R):
        for x,c in enumerate(r[:64]): im.putpixel((x,y),ORDE.index(c))
    return im
if __name__=='__main__':
    maak(lees(sys.argv[1])).save(sys.argv[2],transparency=0)
