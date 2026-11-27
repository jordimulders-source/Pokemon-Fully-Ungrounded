# Staryu-koekje r3 = DC-eindkeuring op r2: alleen uitvoering (lijn, outline highlights, 1-px chiprand, hue shift deeg).
# Bron: sprite_r2/staryu_r2.png. Silhouet bevroren (alpha-diff 0 wordt gecontroleerd). Elke pixel met assert op de oude waarde.
# Draaien: cd staryu_regional/staryu && python3 sprite_r3/bouw.py
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); import gemeen as g
o=np.array(Image.open('sprite_r2/staryu_r2.png')).astype(int); r2=o.copy()
def zet(pts,oud,nieuw,why):
    for x,y in pts:
        assert o[y,x]==oud,(x,y,o[y,x],oud); o[y,x]=nieuw
    print('%-55s %2d px'%(why,len(pts)))
# (b) lijn: zwart en selout om en om op de bovenrand van de rechterarm (s s s s s K s s s K): (46,25) -> selout. Model gem. 176 (licht).
zet([(46,25)],1,2,'(b) om-en-om bovenrand rechterarm K->selout')
# (b) outline highlights (gids: 'Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts';
#     'place pixels of the outline highlight color on the inside of the outline'); op de lichtste lijnpixels volgens het model (gem. >= 165),
#     binnenbuur licht deeg, >= 2 px van zwart; zoals Gen 3 Staryu (8 op de lichte lijn) en Gnomad r10.
zet([(28,16),(27,17),(27,18)],2,3,'(b) outline highlight bovenarm links (model 179/169/184)')
zet([(14,26),(15,25),(16,25)],2,3,'(b) outline highlight linkerarm boven (model 178/177/170)')
zet([(44,25),(45,25)],2,3,'(b) outline highlight rechterarm boven (model 168/177)')
zet([(17,45),(17,46)],2,3,'(b) outline highlight linkerbeen links (model 180/183)')
# (b) chiprand 1 px: chip rechts van het juweel had een 2x2-blok rand (38-39,35-36). Rij 35 binnen de boog -> chipmidden;
#     de boog loopt nu rechts (40,33-35) en onder (38-40,36). Model: chip loopt door tot rij 36 (gem. 66/66/95), dus vorm blijft.
zet([(38,35),(39,35)],6,7,'(b) chip 7: dubbele rand -> 1 px')
# (c) palet: schaduw en selout roder (hue shift naar het model, schaduw model (185,99,39) h25): 3 (200,120,48)->(198,112,50), 2 (150,80,32)->(146,74,34)
PAL=list(g.PAL); PAL[3]=(198,112,50); PAL[2]=(146,74,34); g.PAL=PAL
assert ((o>0)==(r2>0)).all(), 'silhouet veranderd'
print('pixels gewijzigd t.o.v. r2:',int((o!=r2).sum()))
g.opslaan(o,'sprite_r3/staryu_r3.png')
