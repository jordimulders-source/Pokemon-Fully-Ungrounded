# r5: Sigilyph-patroon op romp, bovenarmen, bovenbenen en kraag. Silhouet bevroren (r4). Onderarmen/onderbenen en kop ongemoeid.
# Werkt op 'materialen' (rollen van r4 + nieuwe patroonletters), kleurt daarna per variant P1/P2.
# Patroonletters: z/Z/x = ondergrond licht/midden/schaduw, W wit, C grijs (ring/schaduw wit), E oogmidden, G groen, H donkergroen,
#                 y/Y/u = kraag licht/midden/schaduw, k = lijn in het bedekte deel
import numpy as np
r4=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r4/rollen_hand.txt') if l.strip()]); H,W=r4.shape
o=r4.copy()
def bg(j,i): return not(0<=j<H and 0<=i<W) or r4[j,i]=='.'
def rand(j,i): return any(bg(j+a,i+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1)))
# --- bedekte zones (rij: kolommen)
zone=np.zeros((H,W),bool); kraag=np.zeros((H,W),bool)
for j in range(20,23):
    for i in range(14,22): kraag[j,i]= r4[j,i]!='.'
for j in range(20,25):                       # linker bovenarm (elleboog = rij 20)
    for i in range(0,13): zone[j,i]= r4[j,i]!='.'
for j in range(23,28):                       # romp
    for i in range(12,22): zone[j,i]= r4[j,i]!='.'
for j in range(25,31):                       # rechter bovenarm (elleboog = rij 30)
    for i in range(20,W): zone[j,i]= zone[j,i] or r4[j,i]!='.'
for j in range(28,42):                       # bovenbenen tot de knie (rij 41)
    for i in range(10,23): zone[j,i]= r4[j,i]!='.'
zone&=~kraag
# --- ondergrond met volume (licht/midden/schaduw uit de r4-tinten; bandpixels op hun kolom)
for j in range(H):
    for i in range(W):
        if not zone[j,i]: continue
        c=r4[j,i]
        if c in 'KS' or (c in 'bBrR' and rand(j,i)): o[j,i]='k'; continue
        if c=='K': o[j,i]='k'; continue
        o[j,i]={'L':'z','M':'Z','D':'x'}.get(c,'Z')
# romp: licht links, schaduw rechts (zoals de benen)
for j in range(23,28):
    for i in range(12,22):
        if zone[j,i] and o[j,i] in 'zZx': o[j,i]='z' if i<=13 else ('x' if i>=19 else 'Z')
# dijen: kolomvolume L M D
for j in range(28,42):
    for i in range(10,23):
        if zone[j,i] and o[j,i] in 'zZx':
            o[j,i]={11:'z',12:'z',13:'Z',14:'x',18:'z',19:'Z',20:'x',21:'x'}.get(i,o[j,i])
for j in range(20,23):
    for i in range(14,22):
        if kraag[j,i]: o[j,i]={'L':'y','M':'Y','D':'u','S':'S','K':'K'}.get(r4[j,i],r4[j,i])
# --- motieven (met de hand gezet; ogen pixel voor pixel uit Sigilyph)
def zet(j,i0,s):
    for k,ch in enumerate(s):
        if ch!='_':
            assert zone[j,i0+k], (j,i0+k); o[j,i0+k]=ch
# witte zigzaglijn onder de kraag (Sigilyph rij 26-28: wit hoog aan de zijkanten, laag in het midden, kraag erboven)
zet(23,13,"WWYYYYYWW")
zet(24,13,"ZCWWWWWCx")
# twee oogvlekken (Sigilyph: links kol 25-27 rij 34-36, rechts kol 36-38 rij 34-36), apex van de spleet ertussen
zet(25,13,"CWk_CWC")
zet(26,13,"WEW_WEW")
zet(27,13,"_WC_CWk")
# groene band aan de rechterkant van de romp (Sigilyph rij 27-31 rechts)
# dijen: groene band met witte zigzag (Sigilyph rij 28-31), knieband wit zigzag op donkergroen (Sigilyph rij 38-41)
for i0 in (12,18):
    zet(31,i0,"HHH")
    zet(38,i0,"W_W"); zet(39,i0,"HWH"); zet(40,i0,"HHH"); zet(41,i0,"HHH")
# groene band bovenaan de dijen met kleine witte zigzag (wit om en om per rij, zelfde ritme op beide dijen)
for j in (28,29,30):
    for i in list(range(13,15))+list(range(18,22)):
        if zone[j,i] and o[j,i] in 'zZx':
            o[j,i]='W' if (j in (29,30) and (i+j)%2==0) else 'G'

# ellebogen: witte band op de overgang naar de onderarm (zoals Sigilyphs witte lijn op een overgang)
zet(20,2,"WWWW"); zet(30,24,"WW")
# bovenarmen: volume (links: licht boven, schaduw onder; rechts: licht links)
for j in range(20,25):
    for i in range(0,13):
        if zone[j,i] and o[j,i] in 'zZx':
            o[j,i]='z' if o[j-1,i] in 'kW' or bg(j-1,i) else ('x' if o[j+1,i]=='k' or bg(j+1,i) else 'Z')
for j in range(25,31):
    for i in range(20,W):
        if zone[j,i] and o[j,i] in 'zZx': o[j,i]='z' if o[j,i-1]=='k' else 'Z'
np.save('mat.npy',o)
for j in range(18,44): print('%2d '%j+''.join(o[j]))
