# Muziekpreviews: gedeelde instrumentenset + vijf schetsen (23 okt)

Opgenomen uit een echte test-ROM (`batchrec.py`: HQ-mixer, 21 kHz), mp3 128 kbps. Alle zes nummers zijn origineel
en gebruiken één gedeelde instrumentenset (`tools/grounded/fu_samples.py`, voicegroup `fu`). Ze zijn nog niet aan
kaarten gekoppeld: songs 611–616 (`MUS_FU_*`), noten in `tools/grounded/fu_themes.py`.
Metingen: overal 0 overlopen (geen knapperen), piek 72–102/127, max. −5 tot −7,6 dB.

## fu_demo.mp3: instrumentendemo (611, 58 s)
Elk instrument los. Per instrument: **goed / bijna / opnieuw**, en wat er niet klopt (te dof, te nep, verkeerd register).

| s | instrument | | s | slagwerk |
|---|---|---|---|---|
| 0,0 | quena | | 38,4 | bombo + aro (rand) |
| 3,2 | zampoña (2e maat in kwarten) | | 40,0 | cajón (bas + slap) |
| 6,4 | charango, tokkel | | 41,6 | bongó |
| 9,6 | charango, rasgueo (huayno) | | 43,2 | conga slap/open + tumba |
| 12,8 | nylongitaar | | 44,8 | güiro + shaker |
| 16,0 | accordeon (musette) | | 46,4 | claves + cowbell |
| 19,2 | trompet (vanilla Emerald) | | 48,0 | dembow: kick, snare, clap, hihat |
| 22,4 | trombone | | 49,6 | surdo laag/hoog |
| 25,6 | tuba (vanilla Emerald) | | 51,2 | tamborim + caixa |
| 28,8 | 808-bas met slide | | 52,8 | agogô + apito + crash |
| 32,0 | supersaw (stabs, lead) | | | |
| 35,2 | cuíca (met pitch bend) | | | |

Kanttekeningen: de rasgueo is één sample met een kwintakkoord (grondtoon, kwint, octaven; geen terts), dus één
kanaal per slag en bruikbaar onder mineur en majeur. Cavaquinho in de samba = deze rasgueo een octaaf hoger.

## fu_altiplano.mp3: route op de altiplano (612, 112 bpm, A-mineur pentatonisch, huayno)
0 s intro (wind, quena solo) · 8,6 s A: zampoña solo · 25,7 s A2: quena + zampoña's in kwarten · 42,9 s B: relatief
majeur, lange quena met vibrato, charango-tremolo, lichte groove · 60 s A3: tutti · 77 s terug naar A.
Instrumenten: quena, 2 zampoña's, charango (rasgueo + tremolo), bas, gitaar-bordoneo, bombo + aro, chajchas (PSG), wind (PSG).
**Beoordelen:** voelt het als een open hoogvlakte en een reis die begint (tred, licht melancholisch)? Is de wind te veel/te weinig?
Is de zampoña-melodie pakkend genoeg om vaak te horen?

## fu_vs_wild.mp3: wild gevecht in de Andes (613, 160 bpm, E-mineur)
0 s intro (koperstoten, chromatische loop) · 3 s A: hook op de quena · 15 s A2: trompet mee · 27 s B: fanfare
(diablada-mars, trompet + trombone) · 39 s B2: quena voorop, trompetten in tertsen · 51 s C: zampoña-hoquetus
(ira/arca: links/rechts om en om) · 57 s opbouw · 63 s terug naar A.
Instrumenten: quena, trompetten, trombone, zampoña's, charango, octaafbas, bombo, caixa, PSG-arpeggio's (Pokémon-gevoel), shaker.
**Beoordelen:** werkt het als Pokémon-gevechtsmuziek (energie, herkenbare hook) en hoor je toch de Andes? Hoquetus: leuk of rommelig?

## fu_la_paz.mp3: La Paz (614, 116 bpm, G-majeur, caporales/saya)
0 s intro: teleférico (charango-arpeggio omhoog, quena) · 8,3 s A: fanfare (trompet, trombones in tertsen, tuba) op
een saya-ritme (bombo, caixa, platillos) · 24,8 s B: boven de stad, quena + charango-tremolo, zachte saya ·
41,4 s A2: tutti met charango-rasgueo · 58 s terug naar A.
**Beoordelen:** druk, hoog, feestelijk genoeg voor de startstad? Is de fanfare niet te 'mars'?

## fu_bende.mp3: reggaeton-bende (615, 96 bpm, D-mineur)
0 s intro (stabs, 808-val, riser) · 5 s A: dembow, 808 met slides, supersaw-stabs, hook op de zampoña (panfluit zoals
in Latin-pop-producties) · 25 s couplet: nylongitaar-ostinato (tresillo), dreigend PSG-motief, halve kick ·
45 s A2: hook + PSG-lead, drukkere stabs · 65 s terug naar A.
**Beoordelen:** dreigend maar catchy? Is de 808 vet genoeg zonder alles te overstemmen? Past de panfluit-hook bij een bende?

## fu_samba.mp3: samba/batucada (616, 120 bpm, G-majeur)
0 s apito-signaal + tamborim-chamada · 4 s A: volle bateria (surdo's, caixa, tamborim telecoteco, agogô, ganzá),
cavaquinho, 7-snarige baslijn, fluitmelodie · 20 s paradinha (surdo's stil, tamborim + caixa unisono, cuíca),
26 s virada · 28 s A2: fluit + trompet in tertsen · 44 s C: bateria met trompetriff (gafieira) · 60 s terug naar A.
**Beoordelen:** de proef uit `docs/concept/MUZIEK.md` (samba op de GBA): klinkt de batucada als een échte bateria of als
rommel? Welke trommel mist of is te veel? (Agogô en cuíca vallen in de volste stukken soms even weg: stemverdeler.)
