# Potoo eindkeuring 3 (7 nov): schaduw/kleur en past hij ertussen

Gekeurd: `eind_r3/potoo.png` (64×64, 12 kleuren, 1258 px). Vers en onafhankelijk; alleen uitvoering, geen herontwerp. Vorm, oog, muil, klauwen, snorharen en de grijze haartjes boven op de kop (model, zie eindkeuring2) zijn bevroren en niet als fout geteld. Bekeken op 8×, 14× (kop, onderlijf) en 1×/3× in `rij_1x.png`/`rij_3x.png`, plus de bronsprites in `graphics/pokemon/` (Noctowl, Xatu, Swellow, Drifloon, Dusclops, Swablu, Hoothoot, Altaria, Skarmory). Maatstaven: SPRITE_KERN, Dragonfly Cave-gids (shading, kleurkeuze, contrast, selout), FAKEMON_CHECKLIST E1–E3.

## Vraag 1: schaduw en kleurgebruik — volledig tevreden: JA

| Punt | Meting / oordeel |
|---|---|
| Tinten per groep | Veren 8/7/6, tekening 5/4/3, lijn 2/1, muil c/b/a + 9. Binnen de norm. |
| Helderheidsstappen | Wit/grijs L 250/220/189/155/126/94/53/10: stappen 29–43 (doel ±30–40; de laatste twee zijn lijntinten). Muil L 132/102/77/52: 25–30. Goed. |
| Kleurtemperatuur | Licht warm (crème 7), schaduw koel blauwgrijs; muil koel blauw/violet. Zoals de gids en Swablu/Dusclops. |
| Schaduwrichting | Licht linksboven klopt op kop, muil, flank en vleugel: linkerflank wit tot de selout, schaduw rechts en onder. Sikkel langs de vleugelrand volgt de vorm: 1 px (x46 y32–37 → x45 y38–42) en onderaan 2 px breed (x43–44 y45–47). |
| Banding / pillow | Geen pillow shading. Geen evenwijdige tintbanden meer (de dubbele 6/5-kolom uit eindkeuring2 is weg). |
| Tintclusters < 3 px | 147; vrijwel allemaal spikkels van de tekening (4 op 8) en diagonale lijnstukjes. Echte sprites met tekening zitten hoger (Xatu 168, Noctowl 254, Swellow 332). |
| Buitenlijn / selout | 1 px; zwart rechts en onder, selout 2 op de linkerflank, 9 langs de muil, 4 boven op de kop (lichtkant). Geen zwart/lila om en om. Enige niet-lijnpixels op de rand zijn de modelhaartjes (kop y1–3, (39,3)) en de snorharen. Aandeel donker 0,16 (Gen 3-band 0,10–0,20). |
| Vleugelboog (r3) | Schoon: rechterrand 45-46-47-46-45-44 loopt als bolle curve zonder knik, sikkel schuift mee, binnen de bolling rustig 6. Diff buiten de zone 0, palet gelijk (controle.txt nagerekend). |
| Vorige reparaties | Alle 16 wissels van eindkeuring2 staan erin ((37,3)=1, (42,9)=1, (22,40)=2, (34,21)=4, borstovergang met 7, vleugel-5 later en onderaan breder). Niets nieuws kapot. |
| 1× | Leest scherp op wit en op battle-groen: oog, muil, wit lijf en klauwen direct herkenbaar. |

Bewust niet als fout geteld: de donkere wig onder de kaak links (x20–22 y24–27) is slagschaduw van de vooruitstekende muil op de borst en leest op 1× zo; de klauwen als donkere massa zijn door Jordi goedgekeurd.

## Vraag 2: past hij tussen de andere sprites — volledig tevreden: JA

| Punt | Vergelijking |
|---|---|
| Contrast | Volle range 10–250 zoals Noctowl/Swellow; muil en oog geven het donkerste accent bovenin, net als Xatu's kop. |
| Lijngewicht | 1 px, zwart aan de schaduwkant en gekleurde selout aan de lichtkant: identiek aan Noctowl en Dusclops. Op wit niet dunner of zwaarder dan de buren. |
| Verzadiging | Laag (wit/grijs met één blauwviolet accent), in dezelfde familie als Dusclops en Swablu; vloekt niet met de verzadigder Xatu/Swellow, en wit tegen gras houdt genoeg rand. |
| Detail | Spikkeltekening op het lijf is vergelijkbaar met Noctowl's veertekening en Dusclops' banden; niet drukker, niet kaler. |
| Grootte / vulling | 1258 px in een box 31×63: in de orde van Noctowl (1204) en Xatu (1033), onder Swellow (1432). Smal en hoog past bij een rechtop zittende vogel (Noctowl 36×61). Hij gebruikt de volle hoogte (y1–63), net als Altaria/Skarmory (0–62). |
| Zelfde game? | Ja: in de rij op 1× en 3× valt hij niet op als "fan-sprite"; zelfde pixelgrootte, omlijning, schaduwlogica en kleurdiepte. |

## Ter info voor Jordi (geen fouten)
- De staart (x37–43 y54–62) heeft zijn lichtste strook net rechts van het midden en links een 5-schaduw, waardoor de staart iets van het licht af gedraaid leest; als veer met lichte schacht is dat prima. Wil je hem strikter "licht van links", dan is het 3–4 indexwissels.
- De staartpunt raakt de onderste rij (y63). Geen probleem in de sprite; de hoogte in het gevecht regelt later de y-offset in de data.

Oordeel: PASS
