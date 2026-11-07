# Nachtaap fase 3 – rugpatroon ronde 3 (5 nov)

Basis: `kleur/ronde7c/nachtaap_fase3.png` + `normal.pal` (bevroren, palet ongewijzigd).
Bestanden: `opties.py` (banden met de hand als spans per rij), `check.py` (bewijs), `vel.py` → `vel_opties.png`, `studie.py` → `studie_banden.png`.

## Studie (kort; `studie_banden.png`, 3× + 8×)
| sprite | breedte | kromming | einde | tinten |
|---|---|---|---|---|
| fase 2 | 4–6 px aan de rug | boog over de koepel, ')' (bol weg van de kop), evenwijdig | taps tot 1 px halverwege de flank | 1 eigen lichte tint, geen omlijning |
| Furret | 3–4 px, gelijk | ringen als boog om de cilinder (bol weg van het zichtbare uiteinde) | volle ring tot de contour | band + 1 schaduwtint aan de schaduwkant |
| Dusclops | 2–3 px | horizontale bogen om het ronde lijf | tot de contour | donkere band + licht randje |
| Linoone / Zigzagoon | 3–5 px | V-bogen over de rug, evenwijdig | tot de contour | 2 tinten |
| Raikou | 3–4 px | taps uit de rug, gebogen | punt in de flank | eigen tint |
| Sentret / Typhlosion | 3–5 px | ringen (staart) / brede vlakke rugzone | tot de contour, loopt onder ledematen door | band + schaduwtint |
Regel voor deze pose: de romp ligt horizontaal, kop naar de kijker → ringen zijn vanuit ons bijna verticaal en bollen als ')' naar de heup; de lichtkant volgt de massa's van 7c (5/4 → band licht, 3 → band schaduw).

## Tinten
Band = 13 (licht zilverblauw) waar de vacht 5/4 is, 14 waar de vacht 3 is. Zo is de band vlak en als geheel geschaduwd (lichtgrens van 7c loopt door), net als de lichte banden van fase 2. Omlijning (1/2) blijft staan; geen eigen omlijning binnen de vacht.

## Opties
- **A: 3 taps banden (taal van fase 2).** 4 px breed aan de rugkant (band 1 begint op de schouderrand, banden 2–3 komen onder de voorrand van het opgeheven been vandaan), ')' -boog, lopen taps uit tot een punt vlak boven de buik. 100 px gewijzigd.
- **B: 3 volle ringen (Furret).** Gelijke breedte 3 px, ')' -boog, van de rugrand tot de buikcontour; ringen 2–3 lopen onder de dijwortel van het onderbeen door (worden daar afgekapt, niet op het been gezet). 102 px gewijzigd. **Mijn voorkeur:** leest op 1× het duidelijkst als banden om het lijf.
- Weggegooid: (A-eerste versies) smalle taps banden die midden in het lijf begonnen → lazen als schuine krassen; (C) 2 brede ringen van 5 px → leest op 1× als een wit verband/vest.

Afstand tussen de banden ±3 px (gelijk aan de bandbreedte), evenwijdig. Schouder (x25–29) tot heup (x≤42); niets op het achterwerk (x≥43), de staart of de benen.

## Bewijs (`check.py`)
- Alpha-diff 0 (beide). Palet identiek aan 7c.
- Alle wijzigingen binnen de romp x25–42, r31–45, buiten de dijwortel van het onderbeen; 0 px op kop, armen, hand, gloed, staart, benen.
- Alleen tinten 13/14 gezet; 0 open randen (geen bandpixel naast transparant); 0 losse pixels.

## Eigen keuring (1× en 3×, licht/donker, naast fase 2, Furret, Dusclops)
- B: leest als drie ringen die om de romp buigen; het onderste stuk (14) zakt mee in de buikschaduw zoals bij Furret.
- A: leest als de taps strepen van fase 2; de ')'-boog is zichtbaar.
- Beide: geen kringen, geen mini-streepjes, niet op de kont.

## Lessen
- In een pose waarin het been de ruggengraat bedekt, beginnen taps banden midden in het lijf en lezen ze als krassen; laat ze dan vanaf de rand van wat ervoor ligt (been, schouder) over de hele hoogte doorlopen.
- Band = eigen lichte tint op 5/4 en eigen schaduwtint op 3 → de massa-shading van de basis blijft vanzelf leesbaar.
- Brede ringen (5 px) in een licht zilver lezen op een kleine romp als verband; 3–4 px is de grens.
