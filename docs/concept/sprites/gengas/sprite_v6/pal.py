# v6: E/R/W op Gengars exacte waarden (komen alleen in het gezicht voor). H = Gengar 7 en 2, G = Gengar 3 (tandlijn).
# v4: r (selout 118,48,67) samengevoegd met m; w (kern lichtvlek) terug. Zie NOTITIES.md.
# Palet v3: v2 (alles gemeten in model_64_geschrapt.png) met één ruil (keuring v2, MOET 5):
# w (kern lichtvlek 220,172,176; 19 px) eruit -> v; u (gedempt mauve 121,70,91; mediaan Lab-cluster, de lichte wig
# boven/tussen de ogen en bij de linkerrand) erin. Gemeten verlies (heel model, 16 -> 15 tinten): zonder w gem. dE 2,84,
# zonder E 2,79 maar dat kost het oogrood; m als vervanger van u is slechter (gem. dE 33 vs 20 voor b).
PAL=[(0,255,255),    # . transparant
 (11,5,8),     # K omlijning
 (81,37,60),   # a schaduwband/schaduwkant
 (96,54,74),   # b donkere band / masker
 (220,172,176),# w kern lichtvlek (terug, v4)
 (140,49,85),  # m middentint
 (187,84,105), # l lichte band
 (196,128,139),# v lichtvlek
 (121,70,91),  # u gedempt mauve: wig boven/tussen de ogen, linkerrand
 (248,88,88),  # E oogrood donker (v6: exact Gengar idx 6)
 (255,144,144),# R oogrood helder (v6: exact Gengar idx 5)
 (62,62,61),   # g maan donker / grijze selout
 (100,99,98),  # G maan midden
 (136,135,132),# h maan licht
 (186,185,183),# H maanglans + tandschaduw
 (255,246,255)]# W tanden (v6: exact Gengar idx 1)
CH='.KabwmlvuERgGhHW'
