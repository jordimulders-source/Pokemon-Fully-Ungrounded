"""Palet sprite r2: als v1, maar de bliksembasis Y (bijna gelijk aan licht y en oranje 1) is vervallen;
die plek is nu C = wangschaduw (Picapau heeft twee wangtinten). Bliksem = y licht + 1 schaduw."""
PAL = [
 ('.', (152, 208, 160)),  # 0 transparant
 ('k', (24, 20, 16)),     # 1 omlijning zwart (schaduwkant)
 ('1', (238, 150, 80)),   # 2 kastanje licht / bliksemschaduw
 ('2', (206, 104, 44)),   # 3 kastanje basis
 ('3', (150, 66, 30)),    # 4 kastanje schaduw = vleugel licht
 ('v', (116, 46, 20)),    # 5 vleugel basis / koord licht
 ('4', (78, 32, 16)),     # 6 donker kastanje: selout, binnenlijn, vleugel- en koordschaduw
 ('a', (252, 242, 212)),  # 7 crème licht (buik, stippen, snavel licht)
 ('b', (232, 210, 164)),  # 8 crème basis (ook oor-binnenkant)
 ('e', (190, 156, 108)),  # 9 crème schaduw / selout crème
 ('c', (226, 58, 46)),    # 10 wang
 ('y', (252, 230, 110)),  # 11 bliksem licht
 ('C', (168, 40, 36)),    # 12 wangschaduw (was Y)
 ('w', (255, 255, 255)),  # 13 glans
 ('g', (146, 138, 124)),  # 14 grijs licht (snavel midden, poot)
 ('G', (64, 62, 70)),     # 15 grijs donker (snavelpunt/-onderkant, poot schaduw, iris)
]
IDX = {c: i for i, (c, _) in enumerate(PAL)}
RGB = dict(PAL)
def lees(fn='raster.txt'):
    rows = [l.rstrip('\n') for l in open(fn) if not l.startswith('#')][:64]
    assert len(rows) == 64 and all(len(r) == 64 for r in rows), [len(r) for r in rows]
    return rows
