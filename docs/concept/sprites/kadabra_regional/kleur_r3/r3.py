# r3.py: ronde 3 op basis_r2.txt. Elke variant is een lijst rijstukken (y, x0, letters; '=' = laten staan).
# Schrijft var_*.txt/.png (elk alleen die ene wijziging), raster.txt (beste combinatie) en bewijst de pixeldiff buiten de zones.
import pal,sys
from PIL import Image
B=pal.load('basis_r2.txt')
ZONE={'schoppen':(23,16,29,23),'oog':(21,19,33,25),'kaart':(0,14,12,33)}   # x0,y0,x1,y1 (x1,y1 exclusief)
V={}
# --- 1. voorhoofd: rode schoppen (t licht linksboven, r basis, s schaduw rechts, steel en voet) ---
WIS=[(18,25,'ab'),(19,25,'ab'),(20,24,'aabb'),(21,25,'ab')]          # klaver van r2 weg (a-strook x24-25, daarnaast b)
V['schoppen_1']=WIS+[(17,25,'t'),(18,24,'trs'),(19,24,'rrs'),(20,25,'s'),(21,24,'sss')]                       # 3x5: punt, 2 rijen lijf, steel, voet
V['schoppen_2']=WIS+[(17,26,'t'),(18,25,'trs'),(19,24,'trrrs'),(20,26,'s'),(21,25,'sss')]                     # 5x5: punt, 3, 5 (lobben), steel, voet
V['schoppen_3']=WIS+[(16,26,'t'),(17,25,'trs'),(18,24,'trrrs'),(19,24,'rrrrs'),(20,26,'s'),(21,25,'sss')]     # 5x6: lobben 2 rijen hoog
# --- 2. ogen. Ver oog in alle varianten gelijk: lid d (22,21), wit (22,22), pupil (23,22), wit (23,23) (Gen 3-Alakazam: pupil aan de neuskant) ---
VER=[(21,22,'d'),(22,22,'wo'),(23,23,'w')]
V['oog_1']=VER+[(22,28,'wow')]                            # 1 rij: wit-pupil-wit onder het lid (pupil 1 px, oogwit 2 px)
V['oog_2']=VER+[(20,30,'ddd'),(21,28,'ddww'),(22,27,'dwowd')]         # oog van de echte Gen 3-Alakazam pixel voor pixel: 2 rijen, schuin
V['oog_3']=VER+[(22,28,'wow'),(23,28,'dwwc')]              # 2 rijen: wit-pupil-wit met wit eronder (charlatan-Alakazam), oogwit 4 px
# --- 3. kaart (alle randen o; hand vanaf rij 25 ongewijzigd behalve de kaarthoek) ---
V['kaart_A']=[(19,0,'..oooo..'),(20,0,'.owwwwo.'),(21,0,'.owwowo.'),(22,0,'.owooowo'),(23,0,'.owooobo'),(24,0,'..owoddbo')]
V['kaart_B']=[(17,0,'.ooooo..'),(18,0,'owwwwwo.'),(19,0,'owwowwo.'),(20,0,'owooowo.'),(21,0,'owooowo.'),(22,0,'owwowwo.'),(23,0,'owooowo.'),(24,0,'owwwwowo'),(25,0,'oaaaaobbo'),(26,0,'.oooodobbo')]
V['kaart_C']=[(15,0,'.ooooooo.'),(16,0,'owwwwwwwo'),(17,0,'owwwowwwo'),(18,0,'owwooowwo'),(19,0,'owooooowo'),(20,0,'owooooowo'),(21,0,'owowowowo'),(22,0,'owwooowwo'),(23,0,'owwwwwowo'),(24,0,'owwwwowoo'),(25,0,'oaaaaobbo'),(26,0,'.oooodobbo')]
def maak(namen):
    R=[list(r) for r in B]
    for n in namen:
        for y,x,s in V[n]:
            for i,ch in enumerate(s):
                if ch!='=': R[y][x+i]=ch
    return [''.join(r) for r in R]
def diff(R,zones):
    buiten=[];sil=[]
    for y in range(64):
        for x in range(64):
            if R[y][x]!=B[y][x]:
                if not any(z[0]<=x<z[2] and z[1]<=y<z[3] for z in zones): buiten.append((x,y))
                if (R[y][x]=='.')!=(B[y][x]=='.'): sil.append((x,y,'erbij' if B[y][x]=='.' else 'eraf'))
    return buiten,sil
BESTE=sys.argv[1:] or []
if __name__=='__main__':
    for n in V:
        R=maak([n]); open('var_'+n+'.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,'var_'+n+'.png')
        bu,si=diff(R,[ZONE[n.split('_')[0]]]); print(n,'diff',sum(a!=b for ra,rb in zip(R,B) for a,b in zip(ra,rb)),'buiten zone',bu,'silhouet',si)
    if BESTE:
        R=maak(BESTE); open('raster.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,'kadabra_charlatan.png'); pal.rgb(R).resize((512,512),0).save('kadabra_charlatan_8x.png')
        bu,si=diff(R,list(ZONE.values())); print('BESTE',BESTE,'buiten de zones',bu,'silhouet',si)
