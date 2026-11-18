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
P['bunnelby']=dict(f=dict(kop=[24,26,44,40],oog=[37,32.5,2,4],oor=3,romp=[27,44],buik=54,vp=58,ap=58,staart=N),
                   i=dict(kop=[9,16,21,22],oog=[16.5,19,1,2],oor=5,romp=[11,21],buik=27,vp=29,ap=N,staart=N),
                   pose='frontaal staand; icoon idem', frontaal=True)
P['buneary']=dict(f=dict(kop=[20,24,41,38],oog=[33.5,33.5,2,2],oor=3,romp=[27,44],buik=50,vp=54,ap=54,staart=N),
                  i=dict(kop=[10,15,21,23],oog=[17,21,1,1],oor=9,romp=[13,20],buik=27,vp=29,ap=N,staart=N),
                  pose='zelfde 3/4 links, oor omhoog')
P['meowth']=dict(f=dict(kop=[14,21,44,38],oog=[36,28.5,3,4],oor=14,romp=[20,40],buik=46,vp=52,ap=53,staart=[44,39,53,52]),
                 i=dict(kop=[7,15,21,24],oog=[17.5,19.5,1,3],oor=10,romp=[11,17],buik=27,vp=29,ap=N,staart=[21,19,27,25]),
                 pose='frontaal staand; icoon idem', frontaal=True)
P['persian']=dict(f=dict(kop=[2,14,27,30],oog=[16,22,2,4],oor=9,romp=[24,50],buik=44,vp=59,ap=57,staart=[51,15,64,40]),
                  i=dict(kop=[4,17,17,26],oog=[11.5,22.5,2,2],oor=13,romp=[13,24],buik=25,vp=29,ap=27,staart=[18,9,25,16]),
                  pose='zelfde 3/4 links; lijf en poten sterk ingekort')
P['glameow']=dict(f=dict(kop=[11,21,37,34],oog=[27.5,29,1,2],oor=15,romp=[21,46],buik=50,vp=55,ap=54,staart=[30,5,57,20]),
                  i=dict(kop=[6,18,19,24],oog=[13,22,1,2],oor=13,romp=[12,19],buik=27,vp=30,ap=N,staart=[20,9,28,19]),
                  pose='zelfde 3/4 links, krulstaart rechtsboven')
P['purrloin']=dict(f=dict(kop=[25,22,47,34],oog=[38,29.5,3,3],oor=9,romp=[24,40],buik=47,vp=52,ap=52,staart=[9,28,22,50]),
                   i=dict(kop=[8,16,21,23],oog=[15.5,20.5,2,2],oor=9,romp=[11,18],buik=27,vp=29,ap=N,staart=[19,20,27,26]),
                   pose='3/4 zittend, staart links; icoon staart naar rechts', posewissel=True)
P['litten']=dict(f=dict(kop=[13,15,38,37],oog=[29,30,4,4],oor=13,romp=[24,42],buik=46,vp=50,ap=50,staart=[45,13,55,36]),
                 i=dict(kop=[6,12,19,21],oog=[14.5,18.5,2,2],oor=9,romp=[11,19],buik=26,vp=28,ap=N,staart=[20,14,28,24]),
                 pose='bijna frontaal; icoon idem', frontaal=True)
P['rockruff']=dict(f=dict(kop=[15,19,36,33],oog=[28,27,3,4],oor=15,romp=[22,44],buik=44,vp=52,ap=51,staart=N),
                   i=dict(kop=[7,13,18,21],oog=[13.5,18,2,1],oor=10,romp=[10,22],buik=23,vp=29,ap=27,staart=N),
                   pose='zelfde 3/4 links, rotskraag rechtsboven')
P['mudbray']=dict(f=dict(kop=[11,19,31,31],oog=[23.5,23,4,5],oor=7,romp=[22,52],buik=41,vp=56,ap=54,staart=[47,32,55,41]),
                  i=dict(kop=[5,13,16,22],oog=[12.5,17,2,4],oor=9,romp=[12,24],buik=23,vp=30,ap=28,staart=[22,18,25,22]),
                  pose='zelfde 3/4 links; poten sterk ingekort')
P['sandshrew']=dict(f=dict(kop=[19,17,37,32],oog=[30.5,26,2,4],oor=15,romp=[21,44],buik=46,vp=50,ap=52,staart=[45,31,53,45]),
                    i=dict(kop=[6,13,18,23],oog=[12,18,1,2],oor=12,romp=[12,22],buik=25,vp=28,ap=27,staart=[21,15,26,21]),
                    pose='zelfde 3/4 links')
P['nickit']=dict(f=dict(kop=[3,23,30,40],oog=[15,34,3,3],oor=9,romp=[28,54],buik=46,vp=54,ap=51,staart=[44,42,57,52]),
                 i=dict(kop=[3,13,16,21],oog=[10.5,18.5,2,2],oor=5,romp=[16,26],buik=21,vp=25,ap=23,staart=[22,14,28,22]),
                 pose='zelfde 3/4 links, lijf laag')
P['dedenne']=dict(f=dict(kop=[17,24,43,49],oog=[32.5,30.5,2,2],oor=16,romp=N,buik=N,vp=N,ap=N,staart=[44,16,62,48]),
                  i=dict(kop=[8,18,22,28],oog=[14,21,1,1],oor=14,romp=N,buik=N,vp=N,ap=N,staart=[21,17,29,25]),
                  pose='frontaal, vrijwel alleen kop; icoon idem', frontaal=True)
P['pidgey']=dict(f=dict(kop=[19,16,34,27],oog=[28,23.5,3,3],oor=14,romp=[20,46],buik=42,vp=51,ap=50,staart=[42,30,50,43]),
                 i=dict(kop=[8,17,17,26],oog=[13.5,22,2,1],oor=13,romp=[16,25],buik=25,vp=28,ap=N,staart=[21,16,25,21]),
                 pose='zelfde 3/4 links (vogel; oor = kuif)', vogel=True)
P['taillow']=dict(f=dict(kop=[16,18,33,30],oog=[28,26,2,3],oor=N,romp=[17,40],buik=47,vp=51,ap=51,staart=[36,44,56,48]),
                  i=dict(kop=[9,16,17,23],oog=[14.5,19.5,2,2],oor=N,romp=[13,22],buik=25,vp=27,ap=N,staart=[19,21,26,23]),
                  pose='zelfde 3/4 links (vogel)', vogel=True)
P['starly']=dict(f=dict(kop=[17,20,40,35],oog=[29,29,2,4],oor=13,romp=[18,47],buik=46,vp=51,ap=51,staart=N),
                 i=dict(kop=[7,15,20,24],oog=[14,20,1,2],oor=11,romp=[8,23],buik=26,vp=28,ap=N,staart=N),
                 pose='bijna frontaal, rond (vogel; oor = kuif)', vogel=True, frontaal=True)
P['riolu']=dict(f=dict(kop=[27,17,42,30],oog=[36,25.5,2,4],oor=14,romp=[28,42],buik=40,vp=54,ap=54,staart=N),
                i=dict(kop=[11,15,20,22],oog=[14.5,19.5,2,2],oor=13,romp=[13,20],buik=26,vp=30,ap=N,staart=N),
                pose='tweevoeter, kop 3/4; icoon idem', tweevoeter=True, frontaal=True)
P['mankey']=dict(f=dict(kop=[18,20,46,43],oog=[35.5,31.5,2,2],oor=N,romp=N,buik=N,vp=N,ap=N,staart=[49,36,58,47]),
                 i=dict(kop=[9,13,22,27],oog=[15.5,20.5,2,2],oor=N,romp=N,buik=N,vp=N,ap=N,staart=[22,20,29,25]),
                 pose='bal (kop = lijf), frontaal; icoon idem', frontaal=True, tweevoeter=True)
