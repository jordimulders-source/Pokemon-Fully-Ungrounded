# index: kleur (JASC-PAL volgorde). Teken in raster = hex van de index, '.' = 0 transparant
# r7: lijf-, crème- en staarttinten GEMETEN op het model (k-means op gemini_gekozen_ronde6.png)
PAL=[(152,208,160), # 0 transparant
 (40,20,12),    # 1 omlijning (model 8,1,1 -> donkerbruin-zwart)
 (150,86,48),   # 2 selout / binnenlijn (model 165,97,57)
 (206,124,72),  # 3 terracotta schaduw (model 207,124,72)
 (210,156,90),  # 4 lijf schaduw (model 208,157,91)
 (238,184,100), # 5 lijf (model 237,184,100)
 (222,194,136), # 6 creme schaduw (model 224,195,137)
 (244,232,196), # 7 creme (model 242,230,195)
 (176,132,24),  # 8 geel donker / selout
 (228,192,52),  # 9 geel (model 226,192,51)
 (252,232,98),  # A geel licht (model 252,230,97)
 (122,84,46),   # B bruin donker (model 125,86,46)
 (166,122,74),  # C bruin (model 166,121,74)
 (248,248,248), # D wit (oogglans)
 (168,100,66),  # E verre achterpoot/voet (model 165,97,57 / 169,100,73); pupil is nu 1
 (140,124,104), # F snorhaar: middentint (lijnkern model 107-126,96-116,85-107; per spritepixel gemengd met crème/vacht)
]
