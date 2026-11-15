# Keuring welp r7 (onafhankelijke keurder, 15 nov)

**Oordeel: FAIL** (dichtbij; kleur, oog en korrels zijn opgelost, maar het gezicht heeft nog twee storende fouten: neus en voorhoofdsband, plus de pootteentjes en de elleboog).

Werkwijze: eerst blind beoordeeld; pas daarna `r6/keuring.md` gelezen. Vergelijkingen: sprite 8× naast het model, op bbox uitgelijnd (model x 97–942 / y 194–942 → sprite x 7–57 / y 18–63, schaal 0,059); kop en poot op 14×; 1× en 3× naast Growlithe, Vulpix, Skitty, Eevee (`anim_front_gba` + `normal_gba.pal`) en `af/steenjaguar.png`; clusterscript (vlakjes ≤ 2 px).

## Hoofdvraag
Pose, massa, facetten (gehakte steen, geen kussen) en de chocoladebruine ladder kloppen nu met het model; het 3D-idee staat er. Op 1× leest hij als een zittende welp die zijn poot likt. Maar wie op de kop inzoomt ziet een **neus die als een donkere balk naar links uitsteekt** (snavelachtig) en een **voorhoofdsband die rechts uiteenvalt in losse stippen**. Dat zijn precies de gezichtspunten waarop Jordi eerder afkeurde. Zo nog niet naar Jordi.

## Eis 1: trouw aan het model
| Onderdeel | Oordeel |
|---|---|
| Oren | OK |
| Voorhoofdsband | Vorm en lila OK, **maar rechtereinde is een dambord** (MOET 2) |
| Oog | OK: nu rondom gesloten (DDD op y30), iris grijsbeige (g/G), pupil + glans. Iets zwaar bovenlid, acceptabel |
| Ver oog | toegestaan; W op (11,27) blijft |
| Snuit | OK (lichte rug LLL x11–13 y29–30 zoals het model) |
| Neus | **AFWIJKING** (MOET 1): model = driehoek, breed boven, punt naar onder, punt bij x≈9; sprite = balk die onderaan verder naar links steekt dan boven |
| Mond / tanden | OK (tanden (12,36), (15,36), (16,38)) |
| Tong | OK als tong (twee roze, groef op x13); linkerrand wisselt (MOET 4) |
| Opgeheven poot | Vorm OK; **tenen als streepjescode** (MOET 3) |
| Onderarm / elleboog | **AFWIJKING** (MOET 5): model = brede, vlakke elleboog; sprite = hangende punt |
| Borst / nekplooi | OK |
| Romp / facetten | OK |
| Dij, voeten | OK |
| Staart met ring | OK in plek; zie MAG |
| Spiraalplekken | Plekken OK; ontwerp later; netheid zie MAG |

## Eis 2: Gen 3-techniek
- 15 kleuren, bruin 4 tinten (L als hooglicht, toegestaan), stappen ±30–40: OK.
- Geen pillow shading, facetten lezen. Losse korrels uit r6 zijn weg (r6 MOET 5 opgelost).
- Resterend: dambord in de band, kam-tenen, wisselende rand op de tong.

## Status r6-punten
1. Palet: **opgelost** (precies de voorgestelde ladder).
2. Neus: **niet opgelost**, alleen veranderd van hol doosje in balk (zie MOET 1).
3. Oog-onderrand: **opgelost**.
4. Tong: **grotendeels opgelost** (twee tinten, groef); randje zie MOET 4.
5. Korrels: **opgelost** (rug nu één d-lijn; kop en lijf schoon).
6. Spiralen: deels; (30,41)p staat nog los in de schouderspiraal; dijspiraal zie MAG.
- r6 MAG "band 2 px verder doortrekken" is uitgevoerd als losse pixels, waardoor het nieuwe dambord ontstond.

## MOET-reparaties
1. **Neus (x8–13, y31–33): driehoek zoals het model, geen balk.** Nu: (10,31)G, (11–13,31)#, (8–11,32)D, (12,32)#. Maak: y31 x9–13 donker (D, rechts #), y32 x10–12 donker, y33 x11 donker (punt naar onder, net boven de mondlijn). (8,32) wordt transparant (de buitenrand van de snuit loopt via x9). De grijze (10,31)G weg: wordt D, of 1 px glans in m/l op (10,31) als bovenkant van de neus, niet grijs.
2. **Voorhoofdsband rechtereinde (x20–24, y21–22): gesloten vlak, geen stippen.** Nu y21: (20)p (21)l (22)p (23)l; y22: (19)p (20–22)l (23)p. Maak een rond, gaaf einde: (21,21) en (22,21) → p, (20,22)–(21,22) → p, (23,22) → l. Daarbuiten geen lila stippen; de v-binnenlijn (18–19,21),(16,22),(15,23),(14,24) blijft.
3. **Tenen opgeheven poot (x7–15, y43–44): drie tenen van 2 px, geen kam.** Nu lijnen op x9 en x11 met 1 px-tenen op x8 en x10 en een brede teen x12–15. Zet de teenlijnen (D) op x10 en x13 (y43–44), tenen x8–9, x11–12, x14–15 in l/L; (9,43–44) en (11,43–44) worden l.
4. **Tong linkerrand (x11, y37–40): één randsoort.** Nu (11,38)D, (11,39)r, (11,40)D. Maak (11,39) D (of alle drie r als selout); niet om en om.
5. **Elleboog (x15–22, y48–51): brede vlakke onderkant zoals het model, geen hangende punt.** Nu 8→6→2 px naar een punt op (18–19,51). Model: onderste punt van de onderarm ligt rechts, ±5 px breed op y≈50–51 (x≈18–23). Maak y50 x17–21 vulling (d), buitenlijn y51 x17–21, rechts aansluiten op de lijn bij (22,49)–(22,50); linkerkant van de onderrand als rechte diagonaal vanaf de poot.

## MAG-punten
- Rug: band v-p-p, dan een 1 px d-lijn, dan #: oogt als dubbele rand langs de rug (35,33)–(38,36). Liever de lila tot de buitenlijn laten lopen op die 4 pixels.
- Staart (x53–55, y50–53) is egaal l en lichter dan het lijf; model heeft middenbruin met donkere rechterkant: rechterkolom x55 naar m.
- Staartring (52,53–54)c, (53,54–55)q staat schuin op de rand; in het model is het een band dwars over de staart.
- Dijspiraal (42–46,51) c-d-c-d-c en (44,51), (45,52) losse c: lijnen raken elkaar bijna; netter bij de spiraalronde.
- Schouderspiraal: losse p op (30,41).
- Mondlijn (11–16,35) 6 px kaarsrecht zwart; model licht gebogen.
- Oog: bovenlid (17–20,26) vier zwarte pixels op een rij maakt hem iets slaperig; in het model is het oog wijder open. Alleen als het na MOET 1–2 nog zo leest.
