# Lama fase 2, ronde 2: diagnose (maker-agent, 2 nov), nog niet getekend

Jordi (letterlijk): "de poten zijn nog net wat te hoekig he, plus 1 is een rechte lijn, plus ik vind het kleurgebruik nog niet helemaal pokemon like, vooral de vacht. Plus het is ook net niet genoeg een lama meer sinds de vertaling naar sprite"

Vel: `diagnose.png` (`diagnose_vel.py`).
- Rij 1: het poppetje (fase 2 uit `lijn_ronde2.png`), de onderlaag, foto 1, foto 3 en foto 4.
- Rij 2: de alpaca op 4×, ronde 1c op 4× en de diagnose in het kort.
- Rij 3: Stantler, Eevee, Ponyta, Furret, Girafarig en ronde 1c op 3×.
- Onderaan: de vachtrampen naast elkaar, met het voorstel.

## Wat de lama herkenbaar maakt, en waar het verloren gaat

### Kop en snuit
- **Bron (foto 1, 3, 4):**
  - een kleine, kortharige kop die bovenop een dikke wolhals zit en er duidelijk uitsteekt;
  - een **ronde schedel** met een bolle kruin tussen de oren;
  - grote ogen opzij;
  - een **lange, maar stompe snuit** met een ronde neuspartij en een zichtbare **splitlip**;
  - de kop wordt hoog gedragen en de snuit wijst naar de kijker.
- **Alpaca (fase 1):** dezelfde familie, met een blokkige, stompe snuit en een wolkruin.
- **Sprite 1c:** een **smalle wig met een puntsnuit** naar linksonder.
  - De schedel is plat; de voorrand loopt van voorhoofd tot neus bijna recht.
  - De mond is een donkere vlek onderaan, zoals bij een paard.
  - Naast Stantler en Girafarig leest hij als **hert, geit of paard**.
  - De familietrek van de alpaca (stompe, ronde snuit, wolkruin) is weg.
- **Oorzaak:** het poppetje heeft zelf al een smalle, puntige kop (zie het vel). Bij het verkleinen werd dat een wig, en de kleur (kop in schaduwtint, donkere mond) versterkt het paardengezicht.

### Oren
- **Bron:** lange **banaanoren**: aan de basis breed, in het midden iets uitgebogen, met de punten **naar elkaar toe** gekromd. Daarin de rode kwasten (foto 3).
- **Sprite:** twee **rechte sprieten** met een rode stip. Dat leest als hert- of geitenhoorn of -oor.

### Hals
- **Bron (foto 1!):** de hals is het meest lama-achtige onderdeel: **dik, wollig en ruig**, breder dan de kop, met plukken in de omtrek (voorkant en nek) en onderaan een wolkraag die in de borst overgaat. De kop steekt eruit.
- **Sprite:** een **gladde buis**, even breed als de kop, met rechte randen (voorkant x18–22 en achterkant x27–31 zonder enige pluk). De kop gaat naadloos over in de hals: een hertenhals.

### Lijf en wol
- **Bron:** een diepe, wollige romp. De wol hangt aan de buik en achter de dijen in franje; de wol is in plukken en strengen opgebouwd.
- **Sprite:** er zitten plukken in de omtrek van rug en achterwerk (ronde 1b), maar de vlakken zijn glad en dof. De buik is een strakke onderlijn zonder wolfranje. De romp leest als een kortharig dier met een dekentje.

### Poten
- **De rechte lijn = de verre dragende voorpoot (x30–34, y41–56):** een **paaltje** van 5 px breed en 16 px hoog, beide randen kaarsrecht, zonder knie of verloop. Dat is de rechte lijn die Jordi bedoelt.
- **Hoeken:**
  - de opgetilde nabije voorpoot is een "<" van **knikjes van 1 px** (knie x20 y46–47, pols y49–50: harde hoeken, geen boog);
  - de achterpoten hebben de hak als **1-px-uitsteeksel** (x53–54 en x46, y49–51) met trapjes erboven en eronder;
  - alle vier zijn het **donkere hertenpootjes** van gelijke dikte van boven tot onder.
- **Hoe een lamapoot loopt (foto 1, 3, 4):**
  - de **bovenkant zit in de wol**: de dij en de onderarm zijn wollig en breder, als een broek of mouw;
  - daaronder een **slank, kortharig onderbeen** met een **zachte** knie of hak (een bolling over 3–4 rijen, geen knik van 1 px);
  - onderaan een **brede, platte voet** met twee tenen;
  - het verloop is dik → dun → voet, in een vloeiende curve.

### Staart
- **Bron:** kort, dik en wollig, opgeheven en iets naar achteren gekruld (foto 1, poppetje).
- **Sprite:** een klein knopje van 12 px (r21–24). Hij leest als pluim, maar is te klein en te strak voor de wolmassa.

## Vacht: Pokémon-kleurgebruik

| | tinten vacht | basis (licht/verzadiging) | aandeel licht + hooglicht | tintverloop (hue) | vlakken | omlijning |
|---|---|---|---|---|---|---|
| **Stantler** | 5 (ffffac, ffd573, e6b45a, b48331, 7b4100) | b48331 / e6b45a, s60–72, v70–90 | **±30%** (e6b45a 20% + hooglicht) | licht → geel (h48–60), donker → oranje-rood (h31) | grote spiervlakken | bruin 7b4100 aan de lichtkant, zwart onder |
| **Eevee** (karamel + crème kraag) | 4 karamel + 2 crème | c59452, s58, v77 | ±25% licht + **crème kraag** | licht geler, donker olijf-bruin | 3–4 grote vlakken | donkerbruin rondom, zwart onder |
| **Ponyta** | 4 crème/geel | ffee7b, v100 | ±45% | hue-shift geel → oranje | groot, rustig | lichte selout bovenop |
| **Furret** | 2 groepen × 2–3 | ffee94 / 9c624a | 33% licht | | banden als vlakken | bruin |
| **Girafarig** | 2 groepen × 4 | eeb431 / ffde41, v93–100 | ±26% licht | | vlekken als vlakken | |
| **Lama 1c** | 5 bruin (e2b47c, c88e55, a86a3a, 74401f + omlijning 2a161a) | c88e55, s57, v78 | **±6%** licht (e2b47c) + 6 px hooglicht | alles h23–32: **geen hue-shift**, de donkere tinten worden alleen grauw-rood | veel kleine vlakken en strepen | 14% bijna-zwart + 16% donkerbruin (d): **±30% donker** |

**Conclusie:**
- Bij GF is de **lichte tint een hoofdtint** (20–45% van de vacht). De basis is **helder (v80–93)** en **verzadigd**. Het tintverloop schuift naar **geel in het licht en oranje of rood in de schaduw**.
- Onze vacht is te donker: 23% schaduw, 16% donker en 14% omlijning tegen 6% licht. Hij is dof (geen hue-shift) en wordt in de schaduwen grauw. Daarom oogt hij "niet Pokémon".
- Ook de kop staat in de schaduwtint, wat het geheel nog donkerder maakt.

**Nieuwe vachtramp (karamel, iets donkerder dan de crème alpaca, maar helder en warm, met hue-shift):**

| letter | nu | voorstel | rol |
|---|---|---|---|
| h | f6dcae | **f8e2a8** (h43 s32 v97) | hooglicht op wolpunten, kruin, rug |
| l | e2b47c | **efc27a** (h37 s49 v94) | **hoofdtint licht**: bovenkant van wol, hals, rug, dij (±25%) |
| b | c88e55 | **d69a52** (h33 s62 v84) | basis karamel (±35%) |
| s | a86a3a | **a8683a** (h26 s65 v66) | schaduw (±20%), oranje-rood |
| d | 74401f | **6c3a20** (h22 s70 v42) | selout lichtkant en scheidingen, spaarzaam |
| k | 2a161a | 2a161a | alleen aan de schaduwkant (doel ≤ 10%) |

- **Optie wol licht:** foto 1 heeft lichte wolpunten en een lichtere borst. Voorstel: geen apart crème-vlak (dat is fase 3: bont, met crème hals en kop). In plaats daarvan krijgen de wolplukken in de omtrek en op de borst de lichte tinten h/l. Zo leest de wol als wol (plukken met lichte punten), zonder dat fase 2 bont wordt.
- **Kop niet meer in de schaduwtint**, maar in b/l met s alleen aan de schaduwkant. "Iets donkerder" (SPEC) wordt dan een snuitmasker: neuspartij s/d, niet de hele kop.
- Het palet blijft 16: dezelfde vijf vachtslots krijgen de nieuwe ramp. Kleding, ogen, rood, n en w blijven.

## Plan (wacht op Claude's keuring)

Pose, verhoudingen en kleding (halsband, aguayo, MMA-handschoenen, oorkwasten) blijven. Het silhouet wijzigt in kop, oren, wolomtrek van hals en lijf, poten en staart. Daarna volgt een volledige herkleuring van de vacht op het nieuwe silhouet; de kleding wordt overgenomen van 1c en waar nodig verschoven.

| # | Onderdeel | Silhouet? | Wat | Schatting |
|---|---|---|---|---|
| 1 | **Oren** | ja | Banaanvorm: basis 3–4 breed, licht uitgebogen, punten 1–2 px naar elkaar toe; de rode kwast aan de punt blijft. | ±12 px |
| 2 | **Kop: kruin en snuit** | ja | Ronde kruin tussen de oren (1–2 px bolling, wolkuifje als familietrek van de alpaca). Snuit stomp en rond: de neuspartij 1–2 px breder en ronder, met een splitlip-inkeping onderaan vooraan (een donkere naad van 2 px), het neusgat erboven. Geen wig meer; de onderkaak loopt in een boog naar de keel. | ±25 px |
| 3 | **Hals: wolhals** | ja | De hals wordt **breder dan de kop**: wolplukken aan voorkant (keel) en nek, 1–2 px naar buiten, in 3–4 rustige plukken. Onderaan een wolkraag waarin de halsband zit. De kop steekt uit de wol (een naad onder de kaak). | +35 / −5 px |
| 4 | **Lijf: wolfranje** | ja | Onder de buik 2–3 hangende wolplukken (1–2 px) tussen de poten, zonder de ruimte onder de buik dicht te maken. Achter de dij een wolrand. De rugplukken blijven. | ±20 px |
| 5 | **Verre voorpoot (het paaltje)** | ja | Bovenaan een wolmouw (1 px breder tot ±y46). Daaronder een slank onderbeen van 4–5 px dat licht schuin loopt, met een zachte knie (bolling over 3 rijen op ±y49–51). Geen twee rechte randen meer. | ±25 px |
| 6 | **Opgetilde voorpoot** | ja | De 1-px-knikjes worden een boog: een wolmouw aan de bovenkant, de knie als ronde bolling (rijen y45–48 in een curve 1-1-2), de pols geleidelijk naar de handschoen. | ±15 px |
| 7 | **Achterpoten** | ja | Een **wolbroek** op de dij (breder, plukrand achter tot de hak). De hak als zachte bolling over 3–4 rijen in plaats van een uitsteeksel van 1 px. Het onderbeen slank en licht schuin, de voet breder (2 tenen). De verre poot blijft kleiner en hoger. | ±40 px |
| 8 | **Staart** | ja | Groter en wolliger (±18–20 px in plaats van 12), opgeheven en iets naar achteren gekruld, met 2 plukken. | +8 px |
| 9 | **Vacht (kleur)** | nee | Nieuwe ramp (zie boven). Licht als hoofdtint op de bovenkanten; grote rustige vlakken. Wol als plukken met lichte punten: de omtrek in h/l met d-selout aan de lichtkant, de schaduwgrens gekarteld in de haarrichting. Zwart alleen aan de schaduwkant. Kop in b/l met een snuitmasker in s. Hals als wolcilinder; romp met een kernschaduw; dijen als bol. | herkleuring van ±900 vachtpixels |
| 10 | **Kleding** | nee | Halsband (1c) verschuift mee met de wolkraag; aguayo, handschoenen en oorkwasten blijven zoals in 1c. Alleen verschuiven waar het silhouet verandert. | ±20 px |

**Formaat:** ongeveer +80 tot +120 px netto (1188 → ±1280). Dat zit dichter bij de norm voor fase 2 (1,5× fase 1 = ±1530) en het lijf blijft slank.

**Werkvolgorde (zuinig, met keuring tussendoor):**
1. Eerst het **silhouet ronde 2** (punten 1–8) als één vel naast de bron en ronde 1b. Claude keurt het silhouet.
2. Daarna de **kleur** (punten 9–10) op het goedgekeurde silhouet, in één ronde.

Zo herhaal ik de fout "één punt los repareren" niet: kop, hals, poten en wol veranderen samen, en pas daarna de kleur.

**Risico's** (vooraf gemeld):
- De kop moet "lama" worden zonder alpaca te worden. De lange snuit blijft het verschil met de alpaca; alleen de punt wordt stomp.
- De wolhals mag het poppetje niet verdikken tot een boomstam. De bovengrens is de breedte die foto 1 toont, met de kop als kleinste deel bovenop.
