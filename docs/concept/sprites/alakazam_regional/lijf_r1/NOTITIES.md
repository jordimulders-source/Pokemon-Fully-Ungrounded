# Charlatan-Alakazam: lijf r1 (romp minder als kleding)

Basis: `basis_r11.txt` (= `../kleur_r11/var_r11.txt`). Jordi: "Daarna is het tijd om het lichaam minder als kleding te laten maken. Het lijkt nu bijna een beetje een pinguin badpak met een strik" en "ik wil de tuxedo kleuren zoveel mogelijk verwerken in het lichaam, zodat het natuurlijk lijkt, zoals bij mr rime. maar ook niet te cartoony". Aanvulling: "passend bij wat we eerder besproken hebben" (SPEC: platen, zwarte zijkanten en rug, strikje als tekening, geen kleding).

Bouwen: `python3 lijf.py` (schrijft `opt_O1..O4.txt/.png` en bewijst de diff), daarna `python3 vel.py`. Romp-close-up op 10×: `python3 zoom.py uit.png`. Controle: `python3 controle.py opt_O2.txt`.

## Studie (Mr. Rime, Mr. Mime, Alakazam, Kadabra op 8–12×)
- Alakazam: het bruin is een **plaat** (schouders, borst) met een eigen zwarte lijn. De onderrand van de borst loopt als een ronde V naar het borstbeen. Daaronder is de buik gewoon lijfkleur (geel), met dezelfde kleur als de dijen.
- Mr. Rime: de donkere kleur is het lijf zelf. Het wit is een **sikkelvormige buikband** die de bolling van de buik volgt (bovenrand gebogen, niet recht). Het rood is een ovale vlek met een eigen donkere rand.
- Mr. Mime: het wit is één **ronde schijf** over de hele romp, met een donkere lijn eromheen. Het roze zit als ronde bollen op de gewrichten (schouders, heupen).
- Grenzen volgen dus een **lichaamsvorm** (plaat, buikbolling, gewricht), nooit een rechte verticale "knoopsluiting" tot in het kruis. Dat rechte witte strookje tot het kruis maakte r11 een badpak.
- Overgangen tussen materialen zijn **hard**: geen tussentinten, of één dunne lijn. Binnen een vlak wordt gewoon gearceerd (sikkel rechtsonder).
- Een plaat werpt een kleine schaduw op wat eronder ligt. Daardoor leest hij als iets dat óp het lijf ligt (anatomie), niet als stof.

## Opties (alleen kleur, x19–35, rij 25–45; vorm gelijk)
- **O1 (voorstel Claude):** grijs (b/c/d) is de lijfkleur, zoals het geel bij Alakazam.
  - Het wit is een borstplaat (rij 26–34) met een ronde V-onderrand en een sikkel `a` rechts en onder.
  - De buik en het kruis zijn grijs. De buik krijgt een slagschaduw `c` onder de plaat en een `d`-binnenlijn naar de linkerdij.
  - Zwart blijft op de schouderplaten, de nek/rug en de flank. De flank loopt taps naar de heup (4→2 px).
- **O2 (voorstel Claude):** als O1, maar de flank vervaagt van zwart naar grijs: k/m → d → c → b, schuin verspringend en zonder harde naad. Rond de borstplaat ligt een smalle d/c-rand tussen zwart en wit.
- **O3 (Mr. Rime-vertaling):** het zwart blijft het lijf. Het wit is een ronde buikvlek: breder ter hoogte van de ribben (x25), met een taille (x27) en een ronde onderkant (`a`-sikkel) boven het kruis. Het kruis is grijs, zoals de dijen.
- **O4:** O2 met een strikje van 5×3 (x30–34, rij 26–28) in plaats van 7×4, als rode tekening onder de kin. Rij 25 is kinschaduw `a` op de witte keel.
  - Het strikje is nog herkenbaar: twee lobben, een knoop `s` en inkepingen boven en onder.

## Controle (alle vier)
- Alpha-diff 0, 0 px buiten de zone x19–35 / y25–45. De r12-zone (x36–40), kop, handen, kaarten en armen zijn ongewijzigd.
- Open randen 0, losse o 0. Palet 13 kleuren + transparant, geen nieuwe kleuren.
- Clusters < 3 px: alleen de oude uit r11. O3 heeft één extra: `b` (26–27,41), 2 px in het kruis. O4 heeft één `t`-glanspixel op het strikje.

## Oordeel maker
- Het minst kleding leest **O2**: het lijf is één grijs dier met een donkere rug (tegenschaduw, zoals bij echte dieren), een witte borstplaat in Alakazam-vorm en geen randen die als zoom lezen.
- **O1** heeft een harde horizontale overgang zwart→grijs bij de taille. Die leest als de onderrand van een vest of jasje.
- **O3** is nog steeds een pinguïnpatroon: wit voor, zwart rond. Wel gebogen en niet meer tot het kruis.
- **Risico bij O1/O2/O4:** grijze buik + grijze dijen kunnen samen als "broek" lezen. Dat werkt hier minder sterk dan bij O1, omdat de flank in O2 doorloopt in het grijs.
