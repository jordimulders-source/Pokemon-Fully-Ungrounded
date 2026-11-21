# Dundragoon (Dunsparce-evolutie, Dragon/Normal)

## Jordi, letterlijk
- 8 nov: "een evolutie die ik als kind altijd imagineerde, een lome grappige dragon evolutie van Dunsparce, jaaaren voordat Dudunsparce bestond. Het was meer een Drampa achtige draak, ook jaaaren voordat die bestond."
- 8 nov: "het is een tweede vertakking naast dudunsparce en ik denk dat we hem ook ipv doen." (Dudunsparce is uit de ROM, `FU_DUDUNSPARCE`.)
- 20 nov: "Laten we Dundragoon doen"; over de oude testsprite (`ungrounded/`): "dit design is nog niet heel goed gelukt, maar daar kan gemini bij helpen".
- 20 nov: "Dundragoon wordt Dragon/Normal".

## Keuzes (20 nov, meerkeuzevragen)
- Oude testsprite gaat **niet** als bijlage mee naar Gemini; alleen tekst.
- Van de testsprite blijven: **grote vleugels**. Niet gekozen: lange hals, twee pootjes zoals in de test, vleugeltjes als oren.
- **Staart loopt over in de boor** (zoals Dunsparce): ja.
- Lijf: **Dunsparce-lijf, groter**.
- Poten: **twee korte**.
- Gezicht: "Lijkt op Dunsparce maar meer dragon vorm".

## Voorstel Claude (niet van Jordi)
- Kleuren en tekening van Dunsparce (geel, blauwe banden, blauwwitte vleugels) in de prompt, omdat het lijf en gezicht op Dunsparce lijken. Wil Jordi andere kleuren: aanpassen.
- Drampa niet bij naam in de prompt (les GEMINI.md: een genoemde Pokémon = Gemini kopieert hem).

## Rondes
- Prompt r1: `gemini/PROMPT.md`.
- r1 (`gemini/r1.png`) afgekeurd, Jordi: "niet gelukt, hoofd is nog hetzelfde, vorm heel raar, vleugels niet groot genoeg"; "en niet uniek genoeg de vleugels".
- Keuzes na r1 (Jordi, 20 nov): hoofd "1, 2 en 4" = **langere snuit, hoorntjes, oogring houden** (niet: snorharen/baard); houding **diagonaal**; vleugels "gewoon zoals dunsparce, maar iets groter, ze moeten vrij bizar zijn, niet typisch dragon".
- Prompt r2 (nieuw gesprek, geen bijlage): `gemini/PROMPT_r2.md`. Dunsparce minder bij naam (r1 kopieerde hem). Voorstel Claude: diagonaal = kop linksboven, boorstaart rechtsonder.
- r2 (`gemini/r2.png`), Jordi: "dit begint ergens op te lijken, al is het nu iets teveel een dragonite/dunsparce fusion".
- Na r2, Jordi: wat te veel Dragonite is: "De complete vorm, zet de sprite van dragonite maar ernaast en vergelijk zelf. Hij mag best een wat lompe vorm hebben zoals dragonite, maar dit is too much". Boorstaart: "Ja, duidelijke boor".
- Vergelijking Claude (`gemini/r2_vgl_dunsparce_dragonite.png`): Dragonite-trekken in r2 = rechtop staand bovenlijf, armpjes voor de buik, lichte buik met dwarsstrepen, gekrulde spriet op de kop, ronde Dragonite-snuit, vleugeltjes achter de schouders. Prompt r3 (`gemini/PROMPT_r3.md`, nieuw gesprek, geen bijlage) haalt die eruit; lompe vorm mag.
- Jordi bij r3: "nee we moeten een nieuwe prompt/gesprek"; "het is teveel dragonite, maar je prompt zat goed in de richting" (r3 = prompt r2 + anti-Dragonite + boor, nieuw gesprek).
- r3 (`gemini/r3.png`), Jordi: "staart, vleugels, hoofd goed, maar wil geen slang".
- Keuzes na r3: lijf **Dunsparce-romp, dik** (Dunsparces worstvormige romp, veel dikker en zwaarder, op twee pootjes, geen lange slangenhals); aanpak **nieuw gesprek, alleen tekst**; "al mag de drill naar verhouding nog wat groter". Prompt r4: `gemini/PROMPT_r4.md` (hoofd, vleugels, staart beschreven zoals in r3).
- r4 (`gemini/r4.png`), Jordi: "hij is te horizontaal en net wat te lang"; "hij mag in een soort vliegpose wel". Bijstuurprompt r5 in hetzelfde gesprek: `gemini/PROMPT_r5_bijsturen.md`.
- r5 (`gemini/r5.png`, bijsturen): Jordi "hij snapt het niet" (bijna hetzelfde als r4). Claude draaide r4 zelf 15/25/35° (`plak/r4_rot*.png`, vel `plak/r4_rot_vel.png`) als posevoorstel.
- Jordi na de gedraaide r4: "nee nieuwe prompt from scratch, geen bijlage" → `gemini/PROMPT_r6.md` (vliegpose bovenaan).
- r6 (`gemini/r6.png`), Jordi: "best prima, maar hij mag nog iets dikker"; "beetje chubby". Prompt r7 = r6 met lijf dikker + exact 2 poten (r6 had er 4).
- **r7 gekozen** (Jordi, 21 nov: "dit is hem"): `referenties/gemini_gekozen_r7.png` = bevroren model. Volgende stap: frontsprite (SPRITE_WERKWIJZE → "Gemini-model namaken").
- Jordi bij r7: "de drill is nog niet zo mooi, maar dat kunnen we in de sprite met kleurgebruik oplossen" (= toestemming voor kleurwerk aan de boor in de spritefase; vorm blijft het model).
