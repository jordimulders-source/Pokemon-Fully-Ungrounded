# Emolga-evolutie (wingsuit)

## Besloten (Jordi, 22 nov)
- "ik wil een emolga evolutie. gebaseerd op die extreme sport dat mensen in zo'n pak met vleugels naar beneden duiken en vliegen" (= wingsuit flying).
- "emolga evo blijft dezelfde type" → Electric/Flying.
- "moet echt op een wingsuit lijken"
- "emolga wordt groter, geen helm, geen bril"
- "De sprite wordt wat groter, wat stoerder, echt in een duikvlucht, adrenaline junkie"

## Open
- Naam, evolutiemethode, kleuren (prompt r1 houdt Emolga's kleuren aan; keuze Claude, niet van Jordi).

## Ronde 1 → 2 (Jordi, 23 nov, over Gemini r1)
- "dit is teveel emolga nog met een verkeerd kleurenpatroon. Hij mag groter met een super groot wingsuit, echt een evolution moet het zijn, iets meer aerodynamische look ook, en wat meer naar beneden duikend zoals het met een wingsuit werkt"
- Kleurenpatroon = Emolga's echte patroon (Jordi, keuze in vraag).
- r2 zonder Emolga-bijlage (die maakte hem te veel Emolga); kleuren in woorden.

## Ronde 2 → 3 (Jordi, 23 nov, over Gemini r2)
- "beter, maar het is nu wel gewoon emolga met langere vleugels, de oren mogen wat langer en puntiger, het lichaam wat langwerpiger en vastgegroeid aan de vleugels, de poten wat langer en op zijn buik een tof aerodynamisch patroon, rondom de ogen heeft die een soort van visor kleur zoals een helm zou hebben, ipv de wangen"
- Open: welke kleur de visor heeft, welk buikpatroon (niet ingevuld in r3).

## Ronde 3 (Jordi, 23 nov)
- Over r3: "totaal niet wat ik wil", "dit is emolga met een bril". r3 nam de meeste punten niet over (oren niet langer, vleugels kleiner dan in r2, lijf kort).
- Aanpak r4: r2 als bijlage, max. 2 wijzigingen per ronde (les GEMINI.md: bij veel wijzigingen tegelijk negeert Gemini ze). Volgorde Claude: r4 oren + lijf vastgegroeid; daarna poten + buikpatroon; daarna visor i.p.v. wangen.

## Ronde 4 → 5 (Jordi, 23 nov)
- r4 (Skinguin-opbouw): "oren niet lang genoeg, lichaam niet lang genoeg, vleugels niet lang genoeg, op zn ogen is het een bril, wat een patroon moest zijn".
- r5: zelfde startprompt + verhoudingen in maten + oogpatroon als vachttekening beschreven.
- Daarna: "is weer gewoon net emolga" → r5 noemt Emolga niet meer.

## Ronde 5 → 6 (Jordi, 23 nov)
- Over r5 (zonder de naam Emolga): "deze is wel al wat beter, maar jouw idee wil ik wel proberen" → r6 = r5 met colugo als anatomie (voorstel Claude; alternatieven reuzenvliegende eekhoorn, Draco-hagedis).
- Jordi: "ik heb stiekem nu wel inspiratie gekregen hoe we de fruitvampier in het hele verhaal kunnen betrekken, dat kan misschien een 3e vorm in de emolga lijn worden haha, vrij bizar maar waarom ook niet he" (zie IDEEEN.md).
- Over r6 (colugo): "ok dat is vrij ok, probeer nu die reuzen vliegende eekhoorn" → r7 = r5 met Petaurista.
- Over r7 (Petaurista): "deze is minder goed gelukt". Beste tot nu toe: r6 (colugo, "vrij ok") en r5 ("wel al wat beter").
- Jordi: "En als we voor een fase 3 fruitvampier gaan die op zijn kop hangt met de vleugels gesloten?" (vragen gesteld, zie chat 23 nov).

## Keuze fase 2 (Jordi, 23 nov)
- Over r6 (colugo): "dit is een prima design, beetje finetunen en dan doen we die, hij moet sowieso naar beneden duiken" · "en dan wordt de fruitvampier fase 3".
- Draaiproeven van r6 (45° en 65°, kop omlaag) in `model/r6_duikopties.png` (origineel links).
- Bijgestuurd r6 → `gemini/r6b.png` = model (`model/model.png`). Jordi: "ga maar bouwen met deze, vertaalt dit goed naar een sprite?"
- Proef 64 px (`model/test_64px_8x.png`): silhouet sterk; kop ±12 px, oog en poten nauwelijks leesbaar (vraag aan Jordi of de kop groter mag).
- r6c (kop 1,5× via Gemini, `gemini/r6c.png`): "dit werkt niet helemaal, ik denk dat je voor de gengas methode moet gaan".
- Bouw: model = r6b (`model/model.png`), Gengas-methode: model verkleinen door te schrappen (niets hertekenen), gezicht = Emolga's eigen spritepixels (`graphics/pokemon/emolga/anim_front.png`) 1-op-1 als blok, geschaald (±125%), op de kop van het model; visortekening uit het model, geen wangen (Jordi eerder: visor "ipv de wangen"). Maker-agent, sprite_r1/.
- Jordi: "en net als met de sunflora evolutie eerder, het is dan niet erg dat het hoofd een stuk lichaam overlapt" → kopopties `model/kop_opties/` (A: r6b-kop 1,4×, B: r6c-kop 1,15×, beide op het r6b-lijf; ruwe schets).
- Bouw r1 (maker): A0 = model, A = kop 1,4× (diff 0 buiten kopzone). Keurder r1: A0 BIJNA (zebra in gezicht 10–13,55–57), A PASS; optioneel vacht D lichter. r2 (Claude): zebra uit de kale reductie overgenomen, D (36,36,44) → (44,44,54).
- Eindkeuring (Dragonfly Cave) r2: A PASS, A0 BIJNA (oog); r3 met de reparaties (oog/pupil naar zwart, hand 1 px, tint d (68,68,80)): **beide PASS**. Af: `af/model.png` (A0) en `af/kop14.png` (A), met 8× en `af/vergelijk.png`. Keuze A0/A aan Jordi.
- Jordi (23 nov): "we gaan voor links" → `af/model.png` (A0) gekozen; vergelijking met het model in `af/naast_model.png`.
- Jordi: "ja het is puur dat de buik in onze sprite net wat teveel een diagonale lijn is, maak dat iets smoother" · "baseer je op het model" · "dus hele subtiele wijzigingen" → r4: 5 px buikonderrand naar het model (rij 44, 48, 49), diff 0 elders; `af/model.png` = r4.
- Jordi over r4: "nog niet goed, leg ze allebei op een raster" · "nu heb je sommige hoekjes te dik gepixeld" → raster `sprite_r5/raster_buik.png`; terug naar r3 ("prima aanpak"); Jordi wijst op het raster aan wat te recht is.
- Jordi (raster): "41, 40 mag zwart worden, 50, 31 lichtgrijs zoals in het model en 52, 28 donkergrijs zoals in het model, dus donkerder dan door wat die omringd wordt" (rij, kolom) → r6: (x40,y41) zwart, (x31,y50) zilver (8), (x28,y52) index 4; `af/model.png` = r6.
- Jordi (na r6): "ik denk dat onder de lichtgrijze pixel die ik heb toegevoegd nog een zwarte moet, maar die kan goed daarna weer verkleurd moeten worden, dus doe eerst maar de eindkeuring" → na de eindkeuring: (x31,y51) zwart overwegen.
- Eindkeuring r6: BIJNA (open rand onder (31,50)); reparatie = Jordi's eigen voorstel (31,51) zwart → r7, daarmee PASS. Ter info: L-hoek bij (40,41) (lijn daar 2 px; optie (41,41) → 8), keuze Jordi. `af/model.png` = r7.
- Jordi (na r7): "hijj lijkt nog steeds open te zijn? daarnaast klopt die echt al aan de kleurtinten? je mag afwijken van het model he" · "niet overfixen, gewoon eerlijk zijn" · "zwarte gedeelte van het hoofd en stuk waar de poten uit komen lijkt erg effen". Rand is dicht (`sprite_r8/rand_closeup.png`); kleur: grijze ramp te dicht op elkaar en zwarte zones vlak → kleurronde (alleen kop-zwart en lijf/schouder), silhouet bevroren.
- r8 (kleurronde, maker): donkere ramp 38/64/98 koel, kop + linkeroor + schouder verdeeld (56 px), rest niet aangeraakt; zwak volgens maker: onderkant lijf egaal, oor streperig, nabije gele vleugel 1 tint, donkere band boven buik egaal. Aan Jordi.
- Jordi: "ja totdat het goed is" → r9 (maker): punt 1–4 aangepakt, 39 px, palet = r8. Volgende: verse eindkeuring.
- Jordi over r9: bovenbuik "dit is nog steeds een effen vlak" (uitsnede). Eindkeuring r9 BIJNA (zilveren bovenbuik + gele vleugel effen, buikrand, flap, losse pixel); r10 = die 48 px, index 10 = (140,152,172). Close-up `sprite_r10/buik_closeup.png`.
- Jordi over r10: "ja het wit is nog iets teveel een streep, daar kan misschien nog iets beter met schaduw en tinten gespeeld worden, hij is wel al beter" → r11: korte brede glans + sikkel 10 rechts (31 px, alleen bovenbuik).
- Jordi over r11: "nu overlapt de bovenste poot wel iets teveel met de vleugel, dat was eerst niet toch" → vorm was gelijk (masker identiek sinds r3); oorzaak = donker zilver (10) onder het handje. r12: die 12 px 10→8.
- Jordi: "nee prima, commit r12 maar en push naar main" → `af/model.png` = r12, op het overzichtsvel ("Wingsuit-colugo (Emolga)"). Fase 3 in een nieuw gesprek.
