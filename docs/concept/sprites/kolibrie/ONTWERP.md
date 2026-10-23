# Kolibrie: ontwerp stap 1 (23 okt)

**Richting (Jordi):** de **zielenbode**, Ghost + Fairy *of* Flying (nog open). Basis: Guaraní *mainumby* (voedt de schepper Ñamandu, bode van de dag; zou zielen uit bloemen naar Tupã brengen) en de torpor van de Andes-hillstar (lijkt 's nachts dood, herleeft bij zonsopgang). Bronnen en betrouwbaarheid: `referenties/README.md`. Let op: "zielen keren terug *als* kolibrie" is Azteeks/Costa Ricaans; in Zuid-Amerika is de kolibrie de **bode** van de zielen (Guaraní, Quechua q'enti).

**Vaste kenmerkencombinatie (Jordi):** "lange dunne snavel, de typische kolibrievleugels en een lange staart met een mystiek kleurpatroon."
- **Lijf en basispalet: Andes-hillstar** (foto 1): grijsbruin, witte borst met roestbruine middenstreep, smaragdgroene keelkraag met donker randje. Geest-versie mag bleker/ijler.
- **Snavel + vleugels: foto 2** (zwevend, vleugels opgeheven als V, lange rechte dunne snavel schuin omhoog; regenboog-irisatie groen → magenta → blauw).
- **Staart: langstaartsylfe** (foto 3, `referenties/jordi_langstaartsylfe.png`): twee extreem lange, smalle, gevorkte staartveren. **Dit is het dominante silhouetkenmerk** (A2): ze breken de omtrek naar rechtsonder en geven tegenwicht aan de snavel linksboven (A3).
- **Palet-optie: fluweelkolibrie** (foto 4, *Boissonneaua jardini*): fluweelzwarte kop, iriserend violet lijf, blauwgroene schouders, oranje vlekje aan de vleugelrand.

**Vel:** `concepten.png` (eindvorm-schets in een 64-box, daaruit fase 1, en 3 skelet-sprites; script `concepten_schets.py`). Ruwe vlakken, geen pixelsprite.
**Types in de repo:** Ghost/Fairy alleen Mimikyu en Flutter Mane; Ghost/Flying Drifloon/Drifblim en Oricorio-Sensu. Beide zeldzaam.
**Geen dubbeling:** geen Nazca-lijnen of zonneschijf (Xatu-regional form); geen sterrenbeelden (nachtaap).
**Pose (alle drie, Jordi):** hangend/zwevend met de **vleugels wijd naar de kijker**, zoals Butterfree, Zubat, Zapdos en Moltres (bovenste rij van `referenties/contactvel.png`). Lijf licht 3/4, kop iets links van het midden, lange snavel schuin naar links-voor (één oog, B2), nabije vleugel groter en lager dan de verre (A5, C6), de lange staart hangt eronder en maakt de box hoog. Geen grondlijn (Ghost).

## De drie variaties (verschil: staartpatroon, palet, hoe Ghost erin zit)

### A. Regenboogrook — 3 fasen
- **Idee:** de staartveren beginnen iriserend (groen → blauw → magenta) en vervagen naar de punten tot bleke rook: de zielen die hij meedraagt lossen op in de wind. Overdag de kleuren, 's nachts (torpor) alleen nog rook.
- **Ghost in het lijf:** de staart en het onderlijf lopen uit in rook (geen pootjes). **Fairy:** de regenboogglans als charme; nectar drinken = Draining Kiss. **Flying:** zelfde vorm, nadruk op de V-vleugels.
- **Kleuren:** hillstar-grijsbruin + wit + smaragd; staart groen → blauw → magenta → bleek.
- **Fasen:** 1 = rond kuiken met één korte staartsliert; 2 = één lange sliert; 3 = twee gekruiste slierten.
- **Skelet:** Butterfree (gespreide vleugels, hangend lijf), Moltres (vogelkop met snavel schuin links-voor, gespreide vleugels), Flutter Mane (Ghost/Fairy zonder poten, slierten).

### B. Zielenringen (fluweelpalet) — 2 fasen
- **Idee:** een nachtvogel in fluweelzwart en violet; op de staartveren zitten witte ringen, één per ziel die hij naar de andere wereld brengt (meer ringen = ouder). De blauwgroene glans aan de punten is de dageraad waarin hij uit zijn torpor ontwaakt.
- **Ghost in het lijf:** de fluweelzwarte kop met bleek oog en de zielenringen. **Fairy:** de violette glans en de dageraadpunten. **Flying:** idem met nadruk op de vleugels; het oranje vlekje (foto 4) blijft het warme accent.
- **Kleuren:** fluweelzwart, violet, blauwgroen (+ oranje vlekje).
- **Skelet:** Zubat (lijf + gespreide vleugels, slank), Zapdos (frontale vleugels, snavel links), Misdreavus (zwevende Ghost met slierten).

### C. Nabeeld (ajayu) — 2 fasen, **expliciet Ghost/Flying**
- **Idee:** volgens het Aymara-geloof kan je *ajayu* (ziel) bij schrik uit je lijf vallen; een yatiri roept hem terug. Deze kolibrie flappert zo snel dat zijn ajayu achter hem aan blijft hangen: vleugels en staart laten bleke, iriserende kopieën achter. Hij brengt verloren ajayu's terug.
- **Ghost in het lijf:** de nabeelden zijn zijn eigen ziel. **Flying:** het flapperen is het hele ontwerp; in de animatie verschuift het nabeeld (frame 2).
- **Kleuren:** hillstar-palet; nabeelden bleek magenta/blauw.
- **Skelet:** Ninjask (vegen-vleugels), Zapdos (gespreide vleugels), Cutiefly (fase 1: ronde zwever).
- **Risico:** doorschijnendheid kost kleuren (één palet van 16); nabeelden als 1–2 bleke tinten met omlijning, zoals de Ninjask/Yanma-vleugels. Met de lange staart erbij wordt het druk: misschien alleen de vleugels als nabeeld.

## Open voor Jordi
1. Welke variatie (mix mag: bijv. A's regenboogstaart op B's fluweellijf)?
2. Palet: hillstar-grijsbruin, regenboog, of fluweel?
3. Ghost/Fairy of Ghost/Flying; lijnlengte 2 of 3 fasen.
