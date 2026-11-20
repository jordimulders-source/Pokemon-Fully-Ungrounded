# Hoatzin fase 2, ontwerp 2, s3 (20 nov): Gen 3-afwerking binnen de modelvormen

Jordi: "oog B, 6 rood, ga nu bouwen totdat er een goede versie staat, niet meer blurry" · "vleugelpennen kan je evt met 1 pixel ipv halve pixel doen en dan minder" · snavel: "hoe die er nu uit ziet is prima, alleen nog mooier afwerken" · poten: "vorm ook prima, alleen netter afwerken. Alleen de teen van de linkse poot is iets te bol".
`sh alles.sh` bouwt alles (reduceer → lijnen → skelet → kuifas → bouw3 → vel/check/los/afwijking). Keuzes in `keuze.json`.

## Wat er gebeurt (niets getekend; alles gemeten op MODEL.png)
- **Silhouet = s2**, behalve de linker voorteen: (19,55) (20,55) (21,55) eruit; daar is alpha 0,35–0,43, onder de gewone 0,45, en het model is slanker (`masker_uit`).
- **Zones**: rood alleen in het oog, grijs alleen in snavel/poten: kuifmengtinten die als oog/grijs telden zijn weer kuif. Hierdoor verdwijnen de zwarte streepjes in de kuif.
- **Pennen**: skelet van de zwarte modellijnen op 1024 px (`skelet.py`), per pad geprojecteerd als doorlopende 1-px-lijn. Gekozen: nabije vleugel 5 (paden 11, 25, 47, 83, 115), verre vleugel 3 (9, 10, 13; 27 lag te dicht bij 13 en gaf een klont), staart 2 (242, 251), plus de voorrand van de nabije vleugel (61) en de onderrand over het lijf (164). Boven elke penlijn 2 px lichte tint (nabij 2, ver 3): de lichte penrand van het model.
- **Verre vleugel** een tint donkerder (modelmidden x < 478, y < 470).
- **Tinten**: modus binnen de zone (3×3), tinteilandjes < 4 px weg; losse pixels opgeruimd.
- **Kuif**: middellijnen van de plukken (skelet van het bruine kuifvlak, `kuifas.py`) in de lichte kuiftint, de rest schaduw. Waar zo'n middellijn op een zwarte rand valt, wordt die rand kuifschaduw: de plukken eindigen in bruin. Tegen de vleugel blijft de zwarte lijn.
- **Snavel/poten**: grijs licht als vlak, nieuwe grijze middentint (13, was blauw-selout) als schaduw en selout, zwart aan de schaduwkant. De klauwen in crème komen uit het model.
- **Palet**: kuif (168,100,68)/(116,56,40), grijs midden (112,110,104); verder gelijk aan s2. 15 kleuren + transparant.
- **Oog** = s2 variant B, ongewijzigd.

## Controle en afwijking
dambord 0 · om-en-om 0 · klonten 0 · barcode 0. Losse tintpixels: nog 8, allemaal klauw-, snavel- of pootdetail (1 px, bewust) plus 2 in de staartpunt.
Afwijking van de onderlaag (671 van 1691 px): vleugel 461 (309 lijn, 152 tint: penranden + verre vleugel donkerder) · grijs 82 · crème 55 · kuif 45 · krop 19 · oog 5 · blauw 4. Anders dan s2: 378 px. Handpixels: 0 (de 6 oogpixels van s2 zijn die van Jordi).

## Nog zwak
- De kuif blijft een wigvorm met één hoge spits en 2–3 korte plukken naar rechts. De andere spitsen van het model zijn < ½ px breed en vallen buiten het silhouet.
- Het lijf onder de vleugel heeft lichte vlekken uit het model (glans); die lezen wat vlekkerig.
- De staartlijnen zijn subtiel. De klauwen zijn maar 1 px licht.
