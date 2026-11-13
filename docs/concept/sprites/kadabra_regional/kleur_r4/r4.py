# r4.py: ronde 4 op basis_r2.txt (= kleur_r2/raster.txt). Rijstukken (y, x0, letters; '=' = laten staan).
# python3 r4.py pos_P2 oog_3 kaart_K2 -> var_*.txt/.png + raster.txt; bewijst pixeldiff 0 buiten de zones.
import pal,sys
B=pal.load('basis_r2.txt')
ZONE={'pos':(23,14,33,23),'oog':(21,19,33,25),'kaart':(0,14,12,33)}   # x0,y0,x1,y1 (eindes exclusief)
V={}
WIS=[(18,25,'ab'),(19,25,'ab'),(20,24,'aabb'),(21,25,'ab')]          # klaver van r2 weg
# --- schoppen op het hoofd: op de middellijn van de kop (midden oorbases (30,14) -> neusrug (25,22)); Kadabra vervormt de ster niet, dus de vorm blijft recht ---
V['pos_P1']=WIS+[(15,27,'t'),(16,26,'trs'),(17,25,'trrrs'),(18,25,'rrrrs'),(19,26,'as'),(20,26,'sss')]          # Kadabra-verhouding: as x27, y15-20, onderkant direct boven de lidrij (5x6)
V['pos_P2']=WIS+[(15,28,'t'),(16,27,'trs'),(17,26,'trrrs'),(18,28,'s'),(19,27,'sss')]                          # 1 px verder omhoog langs de middellijn: as x28, y15-19 (5x5, hoger past niet)
V['pos_P3']=WIS+[(16,26,'t'),(17,25,'trs'),(18,24,'trrrs'),(19,24,'rrrrs'),(20,26,'s'),(21,25,'sss')]          # 1 px lager langs de middellijn: as x26, y16-21 = precies de r3-plek (schoppen_3)
V['pos_P4']=WIS+[(16,25,'t'),(17,24,'trs'),(18,24,'rrs'),(19,25,'s'),(20,24,'sss')]                            # recht boven de neusrug: as x25, 3x5 (smaller door de draaiing)
V['pos_P5']=WIS+[(16,28,'t'),(17,27,'trs'),(18,27,'trrs'),(19,27,'s'),(20,26,'sss')]                           # plek van P1, meegekanteld en verre lob 1 px korter (4x5)
# --- ogen (uit r3) ---
VER=[(21,22,'d'),(22,22,'wo'),(23,23,'w')]
V['oog_1']=VER+[(22,28,'wow')]                                        # alleen de pupil: 4 px
V['oog_3']=VER+[(22,28,'wow'),(23,28,'dwwc')]
# --- kaart, schuin: 1 px opzij per 3 rijen (model: linkerrand 3 cellen over 9 rijen = 18 graden) ---
V['kaart_K1']=[(19,0,'...ooo..'),(20,0,'.oowwo..'),(21,0,'.owwowo.'),(22,0,'.owoooo.'),(23,0,'..owowo.'),(24,0,'..owwwoo'),(25,0,'..oaaowbo')]
V['kaart_K2']=[(16,0,'...oooo..'),(17,0,'.oowwwwo.'),(18,0,'owwwowwo.'),(19,0,'owwooowo.'),(20,0,'owwooowo.'),(21,0,'.owwowwwo'),(22,0,'.owooowwo'),(23,0,'.owwwwwwo'),(24,0,'..owwwooo'),(25,0,'..oaaowbo')]
V['kaart_K3']=[(16,0,'....ooooo..'),(17,0,'.ooowwwwwo.'),(18,0,'owwwwowwwo.'),(19,0,'owwwooowwo.'),(20,0,'owwooooowo.'),(21,0,'.owooooowwo'),(22,0,'.owwwowwwwo'),(23,0,'.owwooowwwo'),(24,0,'..owwwoowwo'),(25,0,'..oaaowbowo'),(26,0,'..oaadobboo'),(27,0,'...oo')]
def maak(namen):
    R=[list(r) for r in B]
    for n in namen:
        for y,x,s in V[n]:
            for i,ch in enumerate(s):
                if ch!='=': R[y][x+i]=ch
    return [''.join(r) for r in R]
def diff(R,zones):
    buiten=[];bij=[];af=[]
    for y in range(64):
        for x in range(64):
            if R[y][x]!=B[y][x]:
                if not any(z[0]<=x<z[2] and z[1]<=y<z[3] for z in zones): buiten.append((x,y))
                if B[y][x]=='.': bij.append((x,y))
                if R[y][x]=='.': af.append((x,y))
    return buiten,bij,af
if __name__=='__main__':
    for n in V:
        R=maak([n]); open('var_'+n+'.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,'var_'+n+'.png')
        bu,bij,af=diff(R,[ZONE[n.split('_')[0]]]); print(n,'diff',sum(a!=b for ra,rb in zip(R,B) for a,b in zip(ra,rb)),'buiten zone',bu,'silhouet +%d'%len(bij),bij,'-%d'%len(af),af)
    if sys.argv[1:]:
        R=maak(sys.argv[1:]); open('raster.txt','w').write('\n'.join(R)+'\n'); pal.topng(R,'kadabra_charlatan.png'); pal.rgb(R).resize((512,512),0).save('kadabra_charlatan_8x.png')
        bu,bij,af=diff(R,list(ZONE.values())); print('BESTE',sys.argv[1:],'diff',sum(a!=b for ra,rb in zip(R,B) for a,b in zip(ra,rb)),'buiten de zones',bu,'silhouet +%d -%d'%(len(bij),len(af)))
