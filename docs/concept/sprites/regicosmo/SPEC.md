# Regicosmo (werknaam Jordi) – Cosmic-Regi

Besluiten (letterlijk Jordi):
- 27 nov: "De cosmic regi wordt een collectie van planeten en hemellichamen, die zitten los van elkaar, de middelste heeft de braille achtige stippen [...] we kunnen gaan voor esthetisch, verzin maar een cool idee."
- 27 nov: stippen = voorstel B ("kaart van zijn eigen lichaam": elke stip staat waar een losse planeet om hem heen hangt). Jordi: "B voor regicosmo".
- 27 nov: de losse hemellichamen "moeten idd een golem vorm maken".
- 27 nov: "stippen van regi's lichten altijd op".
- 27 nov: "Ze moeten echt passen tussen de andere regi's ook". Werkwijze: Gemini-modellen.

- 27 nov, typing: "ja ze zijn monotype" (= puur Cosmic).

Open: kleuren, aantal hemellichamen.
Prompt: `PROMPT.md`.

## Rondes
- r1 (`gemini/r1.png`, 27 nov): Jordi: "conceptueel goed, maar het zijn teveel planeten en veeeeel te veel stippen, dit vertaalt niet naar een sprite denk ik. Sowieso zijn er maar max 8 braille punten vgm".
- r2-prompt: torso + 6 losse hemellichamen (schouders, handen, voeten) = 6 stippen + 1 middenstip = 7 (Claude; zoals Regirock/Regice/Registeel met 7 stippen). Eigen invulling, schrappen als Jordi het anders wil.
- r2 (27 nov; afbeelding niet als bestand ontvangen): Jordi: "het is nu net iets te random en nog net niet goed genoeg golem"; "en misschien dat we de binnenste wat meer een mars kleur kunnen gevn".
- r3-prompt: vaste golembouw (schouders hoog en breed, arm = bovenarm + hand recht eronder, korte voeten onder de romp), paren gelijk (Claude, tegen "random"), romp Mars-rood, stippen in een kleur die tegen rood afsteekt (Claude: niet oranje/rood).
- r3 (`gemini/r3.png`, 27 nov): Jordi: "deze lukt nog niet goed, nu zit die juist weer teveel aan elkaar vast en de hemellichamen zijn te vergelijkbaar, de vorige was toffer". (De gelijke paren waren Claudes invulling: geschrapt.)
- r4-prompt: elk hemellichaam anders (zoals r2), duidelijke tussenruimtes, golemplaatsing zoals r3, Mars-romp.
- r4 (`gemini/r4.png`, 27 nov): Jordi: "ok de stippen kloppen niet en het zou beter zijn als de planeten die boven staan iets meer naar beneden gaan en die eronder ook iets meer" · "als in het zijn geen 7 stippen" (r4 heeft er 9) · "en de mars lijkt meer op een bloedmaan" · "dat is wel een issue" · "dus doe nog maar een nieuwe prompt". (Er is al een Lunatone-evolutie "bloedmaan".)
- r5-prompt: Mars herkenbaar via echte Mars-kenmerken i.p.v. kraters (voorstel Claude: witte poolkap, donkere vlekken, kloof Valles Marineris, oker-roestkleur), schouders en handen lager, 7 stippen met exacte plekken.
- r5 (`gemini/r5.png`, 27 nov): Jordi: "mars is nu een paasei" (ovaal, licht oker met vlekjes). Stippen: 7 (2-1-2-2). r6: Mars perfect rond met bolschaduw, dieper roest-oker. Jordi: "ik herken mars helemaal niet aan een poolkap" → poolkap eruit.
- Jordi (27 nov) stuurde een foto van Mars: "zo herken ik mars" (`referenties/mars_jordi.png`): verzadigd rood-oranje, lichtere gevlekte bovenhelft, brede donkere band over het midden, kleine kraters. Prompt r6 beschrijft de romp naar deze foto.
- r6 (`gemini/r6.png`, 27 nov): Jordi: "ok beter, op de stippen en planeet posities na" (11 plusvormige stippen).
- r7 (afbeelding niet als bestand ontvangen; 7 ronde cyaan stippen 2-1-2-2, Mars met donkere band): Jordi: "deze is nog beter" · "op de posities wederom na". Plan: Claude verschuift de hemellichamen zelf in het model (als assets, niets tekenen).
- Jordi (27 nov) over r7: "als de witte (uranus/neptunus) en saturnus wat lager kunnen zodat het een soort rayman armen lijken met de steen en maan samen dan is die goed".
- r7 bewaard (`gemini/r7.png`). Positievarianten (`positie/schuif.py`, alleen verplaatsen): ijsplaneet en Saturnus 10/14/18 modelpixels omlaag (A/B/C) en 5–6 naar buiten (anders raken ze Mars); `positie/vel.png` = r7 | A / B | C.
- Jordi (27 nov): "als deze klaar zijn komen ze op het sprite sheet onder een apart kopje 'Legendaries'" → nieuwe sectie "Legendaries" in `showcase/maak_vel.py` (SECTIES).
- Jordi (27 nov): "linksonder B, maar de voeten mogen iets meer naar het midden van het lichaam, vooral de rechtse". Voetvarianten op B (`positie/voeten.py`, `positie/vel_voeten.png`): links +1/+2/+3, rechts −3/−5/−7 modelpixels (V1/V2/V3).
- Jordi (27 nov): "V2" → model = `model.png` (= `positie/B_voeten2.png`: r7, schouders 14 modelpixels omlaag + naar buiten, voeten links +2/rechts −5). Sprite gestart (`sprite/`).
