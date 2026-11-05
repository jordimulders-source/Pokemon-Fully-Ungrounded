# Kleur ronde 6 (maker-agent, 2 nov): alleen de kop

Jordi: "neus apart, wenkbrauw mag buigen, buidel zo laten. Hoofd mag sowieso nog wat netter, wat korreliger dan andere pokemon sprites". Basis `ronde5.txt`. De kop (y 0–20) is opnieuw met de hand per rij geschreven in `rijen_ronde6.py` → `ronde6.txt`, `ronde6.png`, `ronde6.pal` (palet = ronde 5), vel `vel_ronde6.png` (`vel6.py`).

- **Silhouet en rest:** alpha-diff 0. 71 px gewijzigd, allemaal in de kop; 0 buiten y 0–20, dus buidel en lijf zijn gelijk aan ronde 5.
- **Netter:** rustige vlakken per tint. Schedel als één hooglichtvlak 3 met een band 7 eronder (geen trapjes 3/7/6). Oren crème zonder oker. Rechterwang in nette banden 6/5. Snuit a → 9 → 7 naar de keel, zonder oker 8 in de kop. Losse 1-px pixels weg (verre wenkbrauw 2 px, snuitschaduw, kin).
- **Losse pixels in de kop** (pixel zonder 8-buur met dezelfde index): ronde 5 = 14, ronde 6 = 9. Wat overblijft is bewust: iris e/f, glans a, neusglans 7 en een paar omlijningshoeken. Echte koppen (zelfde telling, vak van ±25x25): Teddiursa 13, Zigzagoon 16, Zangoose 33, Linoone 45. Doel gehaald (niet meer dan zij).
- **Neus apart:** eigen tint 4 met glans 7 en omlijning 1 onder (x 11–14, y 16–18). Een crème rand 9 (12–13, 15) ligt tussen neus en masker, zodat hij los van de verre maskerlob leest.
- **Wenkbrauw buigt:** boog over het nabije oog. Top y 8 (x 20–24), uiteinden een rij lager: (19,9) links en (25–26, 9–10) rechts. Geen rechte balk meer.
- **Ongewijzigd:** oog (lid 1111, iris e/f, glans), masker met 2 lobben en brug (16–17,10), buidel, lijf.

## Eigen zwakke punten (eerlijk)
- De wenkbrauwboog is op 1x vooral een lichte streep met afgezakte uiteinden; de boog leest pas op 2x.
- De neus (4) is op 1x nog donker naast het masker; het scheidingsrandje is 1 px en verdwijnt op 1x grotendeels.
- Het lid (1 op masker 2) blijft onzichtbaar; het oog leest door iris en glans, niet door het lid.
- De referentievakken voor de telling zijn met de hand gekozen (±25x25 rond de kop) en dus benaderend.
