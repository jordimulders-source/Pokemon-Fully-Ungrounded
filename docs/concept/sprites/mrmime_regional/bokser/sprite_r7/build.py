# r7: basis = r6 'meer'; per zone pixels (x0,y0, rijen; '_' = laat staan, '.' = achtergrond, 1-8 = palet)
import numpy as np, json, sys
from PIL import Image
sys.path.insert(0,'../sprite_r6'); from palet import PAL
B=np.load('../sprite_r6/var/meer.npy')
def zet(a,x0,y0,rows):
    for j,r in enumerate(rows):
        for i,ch in enumerate(r.replace(' ','')):
            if ch=='_': continue
            a[y0+j,x0+i]=0 if ch=='.' else int(ch)
Z={}
# 1 HOOFD ROND: koepel r2-r5 (links 36->34->33->32->31), bovenrand een rij hoger in het midden
Z['1_hoofd']=(33,2,['_ _ _ 1 1 1 1 1 _ _',
                    '_ 1 1 8 8 8 8 8 1 1',
                    '1 8 8 8 8 8 8 8 8 7',
                    ])
# 7 OOG: omlijning rond het oogwit (pupil links in het oog, zoals model); tint OOGT
OOGT='4'; OOGV='model'
OOGEN={'model':{32:[(32,9),(31,12)],36:[(36,9),(37,9),(38,10),(38,11),(37,12)]},
       'rechts':{32:[(33,9),(34,10),(34,11),(33,12)],36:[(37,9),(38,10),(38,11),(37,12)]},
       'ovaal':{32:[(32,9),(33,9),(34,10),(34,11),(33,12),(32,12)],36:[(36,9),(37,9),(38,10),(38,11),(37,12),(36,12)]}}
def oog(a,px):
    for (x,y) in OOGEN[OOGV][px]: a[y,x]=int(OOGT)
    return
    # model (natief): linkeroog alleen boven de pupil en linksonder; rechteroog ovaal rechts van de pupil
    pts=[(32,9),(31,12)] if px==32 else [(36,9),(37,9),(38,10),(38,11),(37,12)]
    for (x,y) in pts: a[y,x]=int(OOGT)
# 2 V groter: twee maten
V_M={18:(32,33),19:(32,38),20:(32,37),21:(33,37),22:(33,36),23:(34,36),24:(34,35),25:(35,35)}
V_L={18:(32,33),19:(32,38),20:(32,37),21:(32,37),22:(31,36),23:(32,36),24:(33,36),25:(33,36),26:(34,35),27:(35,35)}
def v(a,V):
    for y,(x0,x1) in V.items():
        for x in range(x0,x1+1):
            if a[y,x] in (5,6,7,8,3,4) and not (y==18 and a[y,x]==1): a[y,x]=3
# 6 SCHOUDER: bal op de aansluiting arm-romp (x23-30, r14-21), arm komt er links in
SCH=(22,11,['_ _ . . . . . . _ _ _',   # r11 x24-29 weg (oude bal)
            '_ _ . . . . . . _ _ _',   # r12
            '_ _ . . . . . . _ _ _',   # r13
            '_ _ . . . . . . _ _ _',   # r14
            '_ _ . . 2 2 2 2 . _ _',   # r15
            '. . . 2 5 7 7 5 1 1 _',   # r16
            '2 2 2 5 7 8 7 5 5 1 7',   # r17
            '_ _ 2 5 7 7 5 5 4 1 _',   # r18
            '_ _ 2 5 5 5 5 5 4 1 _',   # r19
            '_ _ 2 4 5 5 5 4 4 1 _',   # r20
            '_ _ 7 1 4 4 4 4 1 _ _',   # r21
            '_ _ _ 1 1 1 1 1 _ _ _',   # r22
            ])
# 4 BROEKKRUIS naar het model (Y-naad: linkerarm, lichte plooi rechts, steel naar de beensplit)
KRUIS=(33,36,['_ _ _ _ _ 2 5',     # r36 x38->2
              '2 _ _ _ 2 5 5',     # r37 x33->2, x37->2, x39->5
              '_ 2 1 2 5 5 _',     # r38
              '_ _ 2 1 _ _ _',     # r39
              '_ _ _ 2 1 _ _',     # r40
              '_ _ _ _ 1 2 _',     # r41
              ])
# 3 RECHTERBEEN: binnenrand schuin (40 -> 41), enkel smaller; verre been schuift mee
BEEN=(35,46,['_ _ _ _ _ _ _ _ _ _ _',   # r46
             '_ _ _ _ _ _ _ _ _ 7 1',   # r47 knie: buitenrand 1 px naar buiten (model)
             '_ _ _ _ _ _ _ _ _ 7 1',   # r48
             '_ _ _ _ _ _ _ _ _ 1 .',   # r49
             '1 8 8 7 1 1 _ _ _ _ _',   # r50 verre been schuift geleidelijk mee
             '. 1 8 8 7 1 8 8 7 1 _',   # r51
             '_ 1 8 8 7 1 8 8 7 1 _',   # r52
             '_ 1 8 8 7 1 8 8 7 1 _',   # r53
             '. . 1 8 8 7 1 8 7 1 _',   # r54
             '. . 1 8 8 7 1 8 7 1 _',   # r55
             ])
def maak(oogt='4',V=V_M,vuist=None,oogv='rechts'):
    global OOGT,OOGV; OOGT=oogt; OOGV=oogv
    a=B.copy()
    zet(a,*Z['1_hoofd']); oog(a,32); oog(a,36)
    zet(a,*SCH); v(a,V); zet(a,*KRUIS); zet(a,*BEEN)
    if vuist: vuist(a)
    return a
def save(a,naam):
    rgb=np.array([(0,0,0)]+PAL[1:],'uint8')
    im=Image.fromarray(a.astype('uint8'),'P'); pal=[c for t in PAL for c in t]; im.putpalette(pal+[0]*(768-len(pal))); im.info['transparency']=0
    im.save(naam+'.png',transparency=0); np.save(naam+'.npy',a)
if __name__=='__main__':
    import vuisten
    a=maak(vuist=vuisten.zet_vuisten); save(a,'bokser')
    for t in '35': save(maak(oogt=t,vuist=vuisten.zet_vuisten),f'var/oog_tint{t}')
    save(maak(oogv='model',vuist=vuisten.zet_vuisten),'var/oog_model_letterlijk')
    save(maak(V=V_L,vuist=vuisten.zet_vuisten),'var/v_groot')
