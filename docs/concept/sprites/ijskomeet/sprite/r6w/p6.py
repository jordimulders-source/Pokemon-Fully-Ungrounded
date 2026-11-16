CH='KWLMDSabcdGeCrg'
# K W L M D S | a=P1 spike dark, b=P2 spike mid, c=P3 core, d=P4 core light, G lavender | e eye cyan, C eye core, r eye ring, g glow
PAL=[(30,30,74),(238,248,250),(206,228,238),(166,198,220),(128,164,194),(100,128,168),
     (50,46,102),(82,74,142),(124,100,186),(170,140,224),(208,206,242),(102,226,236),(196,255,255),(80,180,204),(178,236,242)]
import numpy as np
def to_txt(o,fn):
    with open(fn,'w') as f:
        for row in o: f.write(''.join('.' if v<0 else CH[v] for v in row)+'\n')
def from_txt(fn):
    rows=[l.rstrip('\n') for l in open(fn)]
    return np.array([[-1 if c=='.' else CH.index(c) for c in r] for r in rows])
def save(o,naam,s=8):
    from PIL import Image
    im=Image.fromarray((o+1).astype('uint8'),'P'); pal=[255,255,255]+[v for c in PAL for v in c]; im.putpalette(pal+[0]*(768-len(pal))); im.save(naam+'.png',transparency=0)
    r=Image.open(naam+'.png').convert('RGBA').resize((64*s,64*s),0); b=Image.new('RGBA',r.size,(255,255,255,255)); b.alpha_composite(r); b.convert('RGB').save(naam+'_%dx.png'%s)
