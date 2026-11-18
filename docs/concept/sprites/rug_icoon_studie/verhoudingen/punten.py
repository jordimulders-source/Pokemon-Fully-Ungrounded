"""Handmatig afgelezen herkenningspunten (pixelindexen; frame 1). Per soort 'f' = front 64x64, 'i' = icoon 32x32.
kop   = [x0,y0,x1,y1]  kopkader zonder oren (x0 = snuitkant, y0 = kopboven tussen de oren, y1 = kin)
oog   = [x,y,b,h]      middelpunt en maat van het (nabije) oog
oor   = y van de top van het hoogste oor (oorlengte = kop_y0 - oor)
romp  = [x0,x1]        lijf zonder kop/poten/staart; buik = y onderkant lijf
vp/ap = y onderkant voorpoot/achterpoot (pootlengte = vp - buik)
staart= [x0,y0,x1,y1]  kader van de staart (lengte = langste zijde)
pose  = korte notitie; None = niet zichtbaar/niet te bepalen"""
N=None
P={}
P['rattata']=dict(f=dict(kop=[19,29,35,45],oog=[25.5,36,2,3],oor=27,romp=[31,49],buik=46,vp=N,ap=47,staart=[33,13,50,33]),
                  i=dict(kop=[8,18,19,28],oog=[14.5,23.5,2,2],oor=15,romp=[17,24],buik=27,vp=N,ap=N,staart=[20,10,25,19]),
                  pose='front 3/4 links-voor; icoon meer profiel, kop groter')
P['raticate']=dict(f=dict(kop=[7,29,30,52],oog=[23,35.5,2,2],oor=27,romp=[30,52],buik=50,vp=57,ap=51,staart=[38,8,59,28]),
                   i=dict(kop=[5,13,18,24],oog=[13.5,15.5,2,2],oor=11,romp=[14,22],buik=27,vp=30,ap=29,staart=[23,11,28,24]),
                   pose='profiel links gehurkt; icoon 3/4, staart rechts omhoog, compacter')
P['zigzagoon']=dict(f=dict(kop=[4,25,26,44],oog=[17.5,36,3,3],oor=22,romp=[24,57],buik=45,vp=52,ap=N,staart=[44,17,58,36]),
                    i=dict(kop=[6,17,17,26],oog=[11,22.5,1,2],oor=15,romp=[16,26],buik=25,vp=28,ap=N,staart=[19,13,27,21]),
                    pose='zelfde profiel links')
P['sentret']=dict(f=dict(kop=[20,14,48,35],oog=[30,16.5,1,2],oor=1,romp=N,buik=N,vp=N,ap=N,staart=[19,41,40,62]),
                  i=dict(kop=[9,12,23,21],oog=[16,14.5,1,2],oor=6,romp=N,buik=N,vp=N,ap=N,staart=[10,22,18,31]),
                  pose='frontaal op de staart; icoon kop iets gedraaid', frontaal=True)
P['eevee']=dict(f=dict(kop=[19,24,38,37],oog=[28.5,32.5,2,4],oor=10,romp=[37,50],buik=46,vp=52,ap=51,staart=[37,26,50,38]),
                i=dict(kop=[7,15,17,23],oog=[12.5,21.5,2,2],oor=12,romp=[15,23],buik=26,vp=29,ap=27,staart=[18,14,24,19]),
                pose='zelfde 3/4 links')
P['pikachu']=dict(f=dict(kop=[18,20,38,34],oog=[31,24.5,3,3],oor=9,romp=[19,38],buik=50,vp=54,ap=55,staart=[35,20,57,47]),
                  i=dict(kop=[7,16,20,25],oog=[12,20,1,2],oor=10,romp=[11,20],buik=27,vp=29,ap=N,staart=[19,12,26,25]),
                  pose='zittend 3/4 links; icoon zelfde, kop veel groter, lijf klein')
P['electrike']=dict(f=dict(kop=[9,26,28,42],oog=[20,32,3,2],oor=N,romp=[28,52],buik=44,vp=49,ap=50,staart=[46,19,53,30]),
                    i=dict(kop=[7,18,16,27],oog=[12.5,22.5,2,2],oor=N,romp=[15,25],buik=25,vp=28,ap=27,staart=[22,13,25,18]),
                    pose='zelfde profiel links')
P['poochyena']=dict(f=dict(kop=[10,20,33,35],oog=[23,26.5,3,4],oor=13,romp=[32,53],buik=44,vp=51,ap=50,staart=[50,27,57,43]),
                    i=dict(kop=[7,16,17,24],oog=[12.5,18.5,2,2],oor=13,romp=[16,26],buik=25,vp=29,ap=26,staart=[22,14,27,22]),
                    pose='zelfde 3/4 links')
P['linoone']=dict(f=dict(kop=[1,30,16,44],oog=[8.5,38.5,3,3],oor=27,romp=[16,48],buik=44,vp=50,ap=47,staart=[48,27,63,40]),
                  i=dict(kop=[4,17,12,27],oog=[8,25,1,1],oor=16,romp=[11,22],buik=26,vp=28,ap=N,staart=[18,10,26,24]),
                  pose='front lang profiel; icoon eigen pose: staart rechtop, lijf ingekort', posewissel=True)
P['furret']=dict(f=dict(kop=[26,12,47,26],oog=[37.5,19,2,2],oor=7,romp=N,buik=N,vp=N,ap=N,staart=[8,23,24,52]),
                 i=dict(kop=[6,13,15,23],oog=[11,17.5,1,2],oor=9,romp=N,buik=N,vp=N,ap=N,staart=[16,13,28,27]),
                 pose='front rechtop; icoon eigen pose: opgerold/liggend, staart rechts', posewissel=True)
P['raichu']=dict(f=dict(kop=[23,12,45,27],oog=[39,16,3,3],oor=4,romp=[22,47],buik=47,vp=60,ap=58,staart=[0,12,20,40]),
                 i=dict(kop=[4,14,13,23],oog=[10,18,1,1],oor=7,romp=[11,19],buik=27,vp=30,ap=N,staart=[22,10,29,22]),
                 pose='staand 3/4 links, staart links; icoon staart naar rechts, compact', posewissel=True)
P['pachirisu']=dict(f=dict(kop=[15,26,33,40],oog=[27.5,34,2,2],oor=20,romp=[21,33],buik=47,vp=51,ap=52,staart=[29,8,56,40]),
                    i=dict(kop=[5,16,17,26],oog=[12,20.5,1,2],oor=13,romp=[8,16],buik=28,vp=30,ap=N,staart=[14,8,27,24]),
                    pose='bijna frontaal, staart achter; icoon idem', frontaal=True)
# minccino overgeslagen: frontaal, oorlobben en kop niet eenduidig te scheiden
P['skwovet']=dict(f=dict(kop=[13,25,32,40],oog=[25,33,2,2],oor=22,romp=[17,38],buik=50,vp=52,ap=54,staart=[28,9,52,40]),
                  i=dict(kop=[5,17,18,26],oog=[12.5,19.5,2,2],oor=13,romp=[9,22],buik=26,vp=28,ap=N,staart=[16,8,27,21]),
                  pose='frontaal, staart achter; icoon idem', frontaal=True)
P['yungoos']=dict(f=dict(kop=[2,25,23,41],oog=[9,35.5,3,2],oor=N,romp=[22,57],buik=46,vp=51,ap=51,staart=[50,34,63,45]),
                  i=dict(kop=[4,17,14,25],oog=[10,22,1,1],oor=N,romp=[13,24],buik=25,vp=27,ap=28,staart=[21,14,29,21]),
                  pose='zelfde lang profiel links; icoon staart omhoog')
