# Werkwijze party-icoon (compact, verplicht)

Bewezen op de viscacha (19 nov, af: `docs/concept/sprites/viscacha/icoon/af/icon.png`). Volg dit stap voor stap; naslag en bewijs staan in `docs/concept/sprites/rug_icoon_studie/EISEN_ICOON.md`, `STUDIE.md` en `verhoudingen/STUDIE_VERHOUDINGEN.md`.

## Kern (Jordi)
- **Eis 0: hij lijkt op de front.** "dat is het belangrijkste van de hele eisenlijst, hij moet lijken op de echte pokemon". Het icoon is onze front in het klein: kopvorm, gezicht, oren, kenmerken en kleurverdeling overnemen, niets verzinnen.
- **Rekenen, niet schatten.** "de wiskunde is ontzettend belangrijk voor het icoon". Elke maat en plek volgt uit de front × de regels uit de meetstudie, binnen de marge p25–p75.
- **Niet koppig zijn en niet opnieuw tekenen.** Wat goed is blijft pixel voor pixel staan; repareer alleen de benoemde punten.
- **Jordi ziet alleen een af-versie:** geen losse pixels en geen blur, even goed als de iconen die al in de game zitten. Alleen echte keuzes (A/B) leg je eerder voor.
- **Paletten niet aanpassen** ("ik wil niet met de paletten gaan klooien"). Kies één van de 6 gedeelde paletten (`graphics/pokemon/icon_palettes/pal0–5`). Een kleur die er niet in staat wordt de dichtstbijzijnde; zo doen Wailord en Sinistcha het ook.
- **Wat niet werkt** (bewezen):
  - Gemini, ook met voorbeeld, chibi-model of bewerk-prompt: hij herontwerpt en glijdt naar Raichu of Dedenne.
  - De hele front in één keer verkleinen: dat geeft blur.
  - Een maker die de kop "vrij" tekent: dat geeft een verzonnen kop (v5).
  - Krabbels letterlijk rasteren.

## Stappen
1. **Onmisbare kenmerken opschrijven.** Noteer 2–4 per soort, met vorm én maat, bijvoorbeeld "lange rechtopstaande oren dicht bij elkaar". Ter vergelijking: Kadabra zonder lepel is geen Kadabra, Poliwag zonder roze neus is geen Poliwag. Leg ook de opbouw van het oog vast: wit met pupil, of donker met een glanspixel, plus ooglid en kleur.
2. **Onderlaag met de onderdelen-methode.**
   - Deel de front op in onderdelen (polygonen, zoals in `viscacha/icoon/onderdelen/delen.py`). De kopgroep is kop, oren en wangmotief.
   - Schaal per groep met een vaste factor rond het halsgewricht (`bouw.py naam s_lijf s_kop s_oren`). Bij de viscacha werkte a2: lijf 0,38, kop 0,50, oren 0,56.
   - Doelhoogte volgens de fronthoogte: 25→15, 35→18, 45→21, 54→22, 61→24 (±3). De onderkant ligt op y 27–30 en het midden op x 15.
3. **Meetstudie-regels toepassen.**
   - Verhoudingen ten opzichte van gewoon verkleinen: kop ×1,25, lijf ×0,95, snuit ×1,27.
   - Het oog verschuift niet binnen de kop.
   - Minimummaten in px (f = de maat in de front):

     | Onderdeel | Minimum |
     |---|---|
     | oog | 1,0 + 0,26 × f |
     | oor | 2,0 + 0,29 × f |
     | voorpoot | 1,2 + 0,28 × f, minstens 2 |
     | staart | 3,0 + 0,32 × f |

   - Bereken het aandeel van kleine kenmerken in de kop, bijvoorbeeld de wangpluk = 3,8% van de kop.
4. **Poetsen per zone (één maker-agent).** Geef de maker dit bestand, het EISEN_ICOON-lijstje "Lessen viscacha" en de doelgetallen mee.
   - **Oog:** dezelfde opbouw als in de front, alleen kleiner (4–5 px is genoeg, zoals bij Eevee). Op de plek uit de front, nooit het oog van een andere soort.
   - **Gepaarde kenmerken:** wat aan de verre kant achter de kop valt verdwijnt. In het icoon zie je bijvoorbeeld maar één wang.
   - **Dunne details (1 px in de front):** maak er korte stompjes van 1–3 px van, in de lijnkleur en alleen buiten het silhouet. Over het lijf vallen ze weg; Dragapult laat zijn Dreepy's ook weg. Alleen een onmisbaar kenmerk mag je dikker maken.
   - **Gekleurde vlekken binnen het silhouet:** geen donkere binnenlijn, 2–6 px groot.
   - **Binnenlijnen:**
     - Een bruine plooi in de front wordt de schaduwtint, geen omlijning.
     - Donkere binnenlijnen komen alleen waar in de front een deel over een ander deel ligt.
     - "Witter" betekent de lichte tint, niet puur wit.
   - **Schaduw en kleur:** niet plat. Licht valt linksboven, schaduw rechtsonder per deel. Verre delen zijn donkerder. De omlijning is boven index 15 en onder index 14.
   - **Vorm:**
     - Rond waar het dier rond is; punten blijven punten (45°-trapjes).
     - Geen losse pixels en geen blur.
     - Poten als stompjes van 2–3 px; de buik is naar verhouding kleiner.
     - Echt diagonaal, zoals Rattata en Dedenne.
   - **Gebaren boven verhoudingen:** neem over hoe iets krult, buigt en staat; de maat mag chibi worden.
5. **Controleren.**
   - Draai het script: `python3 docs/concept/sprites/rug_icoon_studie/icoon_check.py icon.png front.png`. Alle 17 checks moeten OK zijn; daarnaast `vorm_meet.py`.
   - Kijk zelf op 8× naast echte iconen (`front_icoon_8x.py`) en naast de front.
   - Toets eerst eis 0: zou je de soort op 1× tussen de buren aanwijzen?
   - Daarna een verse, strenge keurder, en pas dan Jordi.
6. **Feedback van Jordi.** Een krabbel voer je **pixel voor pixel** uit, en alleen wat hij aanwijst.
   - Registreer de krabbel op het icoon met template matching; kalibreer schaal en offset en gok niet.
   - Verander niets anders. Kleurwoorden letterlijk nemen: "de kleur van de buik" = de buiktint uit de front.
7. **Frame 2 ("een peulenschil zodra frame 1 staat").** Bouw frame 2 uit frame 1 door alleen te schuiven:
   - alles boven de poten 1 px omlaag;
   - één pootrij vervalt, de voeten blijven op dezelfde rij;
   - één klein gebaar, zoals een pluim of oor 1 px.
   - Er mag geen pixel verdwijnen en er mag geen rand openvallen. Vergelijk op 8× met in-game buren (`rug_icoon_studie/26_frame2_8x.gif`).
8. **Afronden.**
   - Lever `icon.png` (32×64, 2 frames, modus P, index 0 transparant) en `icon_anim.gif` in `<soort>/icoon/af/`.
   - Noteer het paletnummer (`.iconPalIndex`).
   - Maak een changelogsectie en voeg nieuwe lessen toe aan EISEN_ICOON.md.
