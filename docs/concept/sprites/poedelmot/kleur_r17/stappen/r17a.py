# r17a: onderkant links (poot A, B, B2, middenstuk, middenpootje), x14-34, y47-57; gemeten op het model
ROWS={
47:"..337AAA7A77333399AAA",
48:"..3A3AA77773AAAA39388",
49:".3AAA377773AAAAA39388",
50:".3AAAA3373AAAAAA73883",
51:".3AAAA7223AAAAA773933",
52:".3AAAA7727AAAAA772999",
53:"..3AA777277AAA7329993",
54:"..2277332377777239993",
55:"....242.2423333322333",
56:".....22..223777882343",
57:"......2....278883.233",
}
W={y:[(14,s)] for y,s in ROWS.items()}
W.setdefault(46,[]).append((28,"A"))
for s in ROWS.values(): assert len(s)==21
