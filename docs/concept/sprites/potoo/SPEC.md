# Great potoo (Ghost/Normal, losse soort): SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`. Stand: **terug naar stap 1 (ontwerp)**: drie richtingen in `ontwerp/concepten.png` + `ontwerp/ONTWERP.md`.

## Besloten (Jordi, 5 nov)
- Basissoort: **great potoo** (*Nyctibius grandis*): "ik wil sowieso een great potoo".
- **Eén stage** (single stage, zoals Sableye): "laten we 1 stage doen en gelijk met ontwerp gaan beginnen".
- Type **Ghost/Normal**: "Ik vind Ghost/Normal een leuke type, helemaal omdat we al een Ghost/Flying hebben en ik echt ontzettend veel ideeën heb voor vogels". (In de repo zijn alleen Zorua/Zoroark-Hisui Normal/Ghost.)
- **Geen tak of stomp in beeld:** "er is eigenlijk geen enkele pokemon sprite met een tak of iets anders in beeld, dus die camouflage kunnen we niet zo goed overbrengen". De vermomming zit in de sprite-frames (stilstaan ↔ bek open), in het lijf (schorsachtig verenpatroon) en in de data (ability, dex-tekst).

## Kenmerken (uit Jordi's foto's)
- Grote ronde kop, enorme zwarte kraalogen (great potoo: donkere iris, leest als zwart).
- Klein snaveltje, maar een gigantische roze muil als de bek opengaat.
- Licht grijswit met bruingrijs gespikkeld/geschubd verenpatroon (schors/korstmos).
- Rechtop zittend, peervormig lijf, lange vleugels en staart naar beneden.

## Achtergrond
- Guaraní-legende van de urutau: Ñeambiú verliest haar geliefde, verstomt van verdriet en wordt een urutau; de nachtelijke roep is haar klaagzang.
- Leefwijze: zit overdag stil als een afgebroken tak, vaak wekenlang op dezelfde plek; vliegt 's nachts korte stukjes vanaf die plek om grote insecten te vangen en keert terug. Vliegt dus weinig (past bij Ghost/Normal zonder Flying).

## Onderdelen
| onderdeel | bron / referentie | Jordi's woorden | status |
|---|---|---|---|
| pose | driekwart, licht vooruit hangend, **bek open**; kop/muil uit het drieluik (boven + linksonder); skelet: `jordi_great_potoo_tak_bek_open_volledig.png` (hele vogel, bek open, 3/4), voorover hangen uit `jordi_great_potoo_vooroverhangend_bek_open.webp` | "Ik wil de bek juist open, want dat is de sprite die men het meest gaat zien. het wordt uiteraard een driekwart pose met de vogel die licht vooruit hangt" | besloten |
| klauwen | nauwelijks zichtbaar op de foto's | "De klauwen zijn nauwelijks zichtbaar lijkt wel, wel lachen. Dat betekent dat we die prima in een sprite ook kunnen verbergen" | besloten: verborgen |
| neerzetten | optie 1: op een onzichtbare tak, zoals Swellow/Noctowl/Taillow (`vogels_neerzetten.png`) | "ja, optie 1, ga maar naar het silhouet" | besloten |
| frames | frame 1 = bek open (hoofdsprite); frame 2 nog open | idem | deels |

## Silhouet
- v1: omtrek van de takfoto, 10° voorover, gespiegeld: las als augurk (muil onzichtbaar).
- v2: muil-inkeping: te klein op 64.
- v3: onderkaak hangt verder open (drieluik), kop 15% groter (Pokémon-verhouding). 1023 px (Xatu 1033). Model = de foto zelf langs dezelfde omtrek (`silhouet/model_v3.png`).

## Afgekeurd (niet herhalen)
- **Silhouet v1–v4 (de foto overgetrokken):** "we gaan niet een potoo namaken", "we maken een pokemon". Eerst een Pokémon-ontwerp (stap 1), dan pas een silhouet. Gewenst: "geestachtiger", "grote ogen, grote mond".
- Tweede stage die met een tak/stomp versmelt (`concept_schets_2stages_afgekeurd.png`): tak in beeld past niet bij Pokémon-sprites.

## Referenties
- `referenties/jordi_great_potoo_bek_open_drieluik.webp`: bek open (3/4 en zij), voederen.
- `referenties/jordi_great_potoo_stomp_voor.png`: rechtop op stomp, bijna van voren.
- `referenties/jordi_great_potoo_wit_zijaanzicht.png`: lichte vogel, zijaanzicht, kop van dichtbij.
- `referenties/jordi_grijze_potoo_takhouding_nacht.webp`: andere soort (gele iris), takhouding.
- `referenties/jordi_great_potoo_tak_bek_open_volledig.png`: hele vogel op tak, bek open, 3/4 (skelet).
- `referenties/jordi_great_potoo_vooroverhangend_bek_open.webp`: voorover hangend, zijaanzicht, bek open, staart zichtbaar.
- `referenties/jordi_great_potoo_nacht_voor_volledig.webp`: hele vogel van voren, 's nachts (verenpatroon, kop).
- `referenties/jordi_great_potoo_illustratie_rug_staart.png`: illustratie rug/vleugel/lange staart.
