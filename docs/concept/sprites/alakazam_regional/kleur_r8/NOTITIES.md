# Charlatan-Alakazam: kleur r8 (pupil + beide handen, probeersels)

Basis: `basis_r7.txt` (= `../kleur_r7/raster.txt`, bevroren). Varianten staan als rijen in `var.py`; `python3 maak.py` bouwt alle `var_*.txt/.png` en bewijst de diff buiten de zones; `python3 vel.py` maakt `vel.png`. Bekijken: `zoom.py` (uitsnede met raster naast het model), `grid3.py`.

Jordi over r7: "hij kijkt niet naar ons, de positie van de pupil moet dus meer naar links. de hand op de rug is nog niet helemaal goed, je kan niet zien dat hij de kaart vast heeft. Sowieso zijn beide handen gewoon echt nog niet goed."

## Zones (alles daarbuiten pixeldiff 0, met `maak.py` bewezen; alpha-diff 0 in alle varianten)
- oog x31–36, y15–18 · linkerhand x3–20, y37–45 · rechterhand x46–59, y26–37

## Studie (graphics/pokemon/alakazam, kadabra, machoke, hitmonchan)
- Alakazam/Kadabra: de lepel is aan **beide kanten van de vuist** zichtbaar (kop erboven, steeltje eronder). Vingers zijn ronde buisjes met licht boven, scheidingslijnen zijn kort (2–3 px) en zwart. Soms piept één pixel van het voorwerp tussen de vingers door. Omlijning: selout aan de lichte kant, zwart aan de schaduwkant.
- Kadabra-oog: wit | pupil | wit, pupil onderaan tegen het lid (1 4 1). Daarop is pupil 1 px gebaseerd.

## Varianten
- **Pupil 1 px:** pupil (33,16–17) aan het lid, wit (32,17), (34–35,17), (33–34,18). **Pupil 2 px:** pupil (32,16–17), wit (33,16), (33–35,17), (33–34,18); geen wit meer links van de pupil. Oogwit en lid verder ongewijzigd.
- **Links A:** drie vingers liggen horizontaal over de rechterrand van de kaart, toppen verspringen (x10/x11/x12), kaartwit zichtbaar boven, tussen (10,41) en links van de toppen. Toon per vinger a/b boven, c onder.
- **Links B:** duim plat over de kaart (rij 39–40), daaronder kaartwit (rij 41), rechts een vuist met twee knokkellijnen.
- **Links C:** voorste vinger over de kaart, de kaarthoek steekt de hand in (wit rij 42 tot x13) en ligt over de twee achterste vingers.
- **Rechts A (model):** duim omhoog langs de linkerrand van de kaart, twee gekrulde vingers onder de kaart met één korte lijn ertussen.
- **Rechts B:** duim schuin plat op de kaart (top (53,29), wit rondom), vingers achter de kaart, vuist eronder.
- **Rechts C:** wijsvinger ligt op de kaart (x52–53, rij 29–31) met wit links en rechts, duim weggevouwen links onder.

## Beste combinatie: links A, rechts A, pupil 1 px (`raster.txt` = `var_beste_linksA_rechtsA_pupil1.txt`)
- 51 px gewijzigd, 0 buiten de zones. Open randen 0, losse o 0, alpha-diff 0.
- Clusters < 3 px: 9, waarvan 1 nieuw in de zones: de glans (11–12,39) op de voorste vinger. De rest staat ook al in r7 (krulvulling, snorstreng, (41,37), teenlijn, klauwen, selout (24,59)).
- Lijnkaart: 46 rood / 95 blauw (r7: 46 / 90). De 5 blauwe extra zijn vingerlijnen die het model niet heeft.

## Zwakke punten
- De hand is klein (±8×6 px). Drie vingers van 2 px met lijnen ertussen passen niet, dus links A scheidt de vingers alleen met toon (c-rij boven a/b-rij). Op 1× leest dat als een gestreepte vuist.
- In het model wijzen de vingers van links omlaag. Links A/B/C hebben ze horizontaal, omdat verticale strepen de kam van r7 terugbrachten.
- Rechts C leest het zwakst, want de wijsvinger is maar 2 px breed op een kleine kaart.
- Pupil 2 px heeft geen oogwit links van de pupil. Dat is een sterke zijblik, maar minder Kadabra.
