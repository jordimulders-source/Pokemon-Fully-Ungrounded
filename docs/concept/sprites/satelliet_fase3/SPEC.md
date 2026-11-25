# Ruimtestation (Cosmic/Steel-lijn, fase 3), SPEC

Basis (eerdere besluiten, `satelliet_lijn/SPEC.md`): fase 3 = ruimtestation uit gekoppelde modules waarin de satellieten herkenbaar blijven, groter en complexer (zoals Magneton); pure machine; fase 1 (bol met oog) is onderdeel van fase 2 en 3 en wordt een steeds kleiner deel van het geheel; hele lijn Cosmic/Steel; wit/paars à la Mewtwo, cyber.

Jordi letterlijk (25 nov):
- "tijd voor fase 3 van de cosmic/steel lijn, een ruimtestation"
- Formaat: "het ontwerp eerst proberen te maken, maar mag vrij groot"
- Ogen: "had ik nog niet direct bedacht, eerst de vorm van het ruimtestation zien"
- Vorm: Ring/wiel (keuze uit ISS-achtig / ring-wiel / compacte cluster / Gemini laten kiezen)
- "belangrijk is dat het echt als een evolutie leest en goed te vertalen is naar een sprite ook"

Open: aantal ogen, naam, evolutiemethode.

## Gemini-rondes
- r1: `gemini/PROMPT_r1.md` (nieuw gesprek, geen bijlage).
- r1 (`gemini/r1.png`), Jordi: "het leest nog niet echt als een ruimtestation" · "die cirkel is te prominent" · "ik wil meer een ruimtestation".
- r2: `gemini/PROMPT_r2.md` (ring klein en op de achtergrond, modules + grote panelen, kern = fase 2-capsule; uitwerking Claude).
- Jordi: "de bal moet geen losse bal meer zijn maar onderdeel van een groter geheel" · "en misschien moeten we meerdere ballen doen" → r3: `gemini/PROMPT_r3.md`.
- r3 (`gemini/r3a.png`, `r3b.png`), Jordi: "allebei niet groot genoeg, het leest niet als een evolutie" → r4: `gemini/PROMPT_r4.md` (oogbol klein deel van het geheel, centrale balk met 3 bollen, 4 panelen, vult het vak, ring weg).
- r4 (`gemini/r4.png`), Jordi: "dat is al wat beter, maar ik vind hem nog iets te simpel".
- Inspiratie Jordi (`inspiratie/`): "Deze komen dichter in de buurt, maar we moeten het wel zo maken dat het goed naar een sprite vertaalt" → r5: `gemini/PROMPT_r5.md` (kruisvorm, modules met banden, 3 paar lange panelen).
- r5 (`gemini/r5.png`), Jordi: "ok dit is qua vorm prima, de antennes vind ik wel lelijk, te groot. Zijn die nog nodig? En misschien kunnen we die ballen met ogen op alle hoeken zetten (waarvan je er 1 natuurlijk niet het oog ziet) Vertaalt het verder goed naar een sprite denk je?" Check op 64 px: `check/r5_64_8x.png`.
- Jordi: "antennes weg, ogen op alle vier, schrijf r6, het oog kleiner is niet erg, maar dan moeten we gewoon zorgen dat we slim designen, dus met wat minder detail dan fase 2 bijv" → r6: `gemini/PROMPT_r6.md`.
- Jordi: "iris en pupil blijven wel".
- r6 (`gemini/r6.png`), Jordi: "de panelen kloppen niet" → r7: `gemini/PROMPT_r7.md` (alleen panelen: 3 gespiegelde paren aan de lange arm, één vlak, parallel).
- Jordi: "linkeroog zit ook niet goed, rechts wel, maar rechts zou gespiegeld kunnen worden" → in r7 de zijbollen als spiegelbeeld.
- r7 (`gemini/r7.png`), Jordi: "nu zijn er teveel panelen weg" → r8: `gemini/PROMPT_r8.md` (paar panelen op elke arm, 8 totaal).
- Jordi over r7: "en dit is teveel sugimori art" · "ik wil een sprite" → pixel-art-eis in r8.
- r8 (`gemini/r8.png`), Jordi: "nee dit is geen ruimtestation meer". Voorstel Claude: stoppen met prompten, beste eerdere ronde als model (r5 of r6) en zelf bewerken.
- Jordi: "dan ligt het aan de prompt, de zijkanten moeten niet zo groot zijn als de voor en achterkant, doe nog even een sterke prompt maken" → r9: `gemini/PROMPT_r9.md` (basis r5 + alle besluiten erna).
- r9 (`gemini/r9.png`), Jordi: "ok deze vind ik goed op 2 dingen na, 1 paneel linksboven moet gespiegeld worden zodat er 2 zitten en het linkeroog heft weer een perspectief dat net niet goed genoeg is, kan je deze 2 dingen fixen?" · "ah en het onderste paneel is korter dan de bovenste" · "en vertaalt die goed naar een sprite?" (check: `check/r9_64_8x.png`; plaatsing tweeling: `check/r9_paneel_opties.png`).
- Jordi (25 nov, over r9-fixes): "het onderste paneel is in dit model echt korter, maar zal in de sprite onder een ander paneel vallen, maar je ziet hem net nog afkappen." · "Ik weet niet of het rechteroog naar links te spiegelen is vanwege de driekwart hoek. De ogen worden gewoon binnen de paarse cirkel alleen iris en pupil, niks wits erin, anders wordt dat een rotzooi." · "Het tweede paneel moet op rood, maar wel iets hoger, zodat die lijkt te verbinden." · "Daarnaast zie ik dat gemini elk paneel een andere lengte heeft gegeven. Dat moet ook gelijk worden. Rechtsvoor 5 vlakken, linksachterin 4, linksvoor zit niet eens goed verbonden dus dat lijkt 3, bovenop 3, onder 2. Zullen we voor en achter 4 doen en boven en onder 3? Dan moet linksvoor nog net even wat beter aansluiten"
- Claude: eens met voor/achter 4 en boven/onder 3. Model = r9 natief (`model/r9_natief.png`, 99 px, pitch 10,24), bewerkingen door een maker-agent in `model/`.
- r10 (maker-agent, `model/r10_natief.png` = linkeroog variant b, `r10a_natief.png` = variant a; echt raster r9 = 5,12 px pitch, `r9_natief200.png`): alle panelen 4/4/4/4 en mast 3/3, tweeling achter de rechter zijarm, LF met staafje, geen wit in de ogen. Canvas 231×159: op 64 px wordt hij 64×42 (`check/r10_b_a_64_6x.png`).
- Jordi (r10, met uitsnede linkeroog variant a): "wacht we kunnen ook de zijwaartse ogen dezelfde kant op laten kijken als het voorste oog, zodat je nu met links doet, bij deze" → r11: beide zij-ogen naar voren-links zoals variant a, bol/licht van r10.
- r11 (`model/r11_natief.png`): beide zij-ogen naar voren-links (oog van r10a), bol/licht van r10.
- r11, Jordi: "rechtse oog is nog niet netjes, het oog zou ook iets groter moeten zijn vanwege de pose, plus ik zie daar gekke zwarte pixels, je kan het niet zomaar kopieren" → r12: rechteroog opgebouwd uit het grote voorste oog, verkleind naar de bolmaat.
- r12 (`model/r12_natief.png`): rechteroog uit het voorste oog ×0,571 (13×14 px; links 13×12, voor 22×24), restpixels r9-oog weg.
- r12, Jordi: "rechtsboven paneel moet nog wat hoger" → r13a (+3 px) en r13b (+6 px) in `model/` (staafje valt nu achter de achterarm).
- Jordi: "maar nu is de stang weg, positie 6px is beter. Ga anders maar een sprite bouwen, dan passen we het daarna wel aan" → **model bevroren = r13b** (`model/model_gekozen.png`, 231×159, echt raster); open: stang van het tweelingpaneel weer zichtbaar maken (in de spritefase). Spritefase gestart 25 nov.
- Sprite r1 (`sprite/r1/`, maker): 63×42, 12 kleuren; Claude: nog niet naar Jordi (hobbelige buizen, banden half, vlekkerig wit, rommelige panelen) → r2.
- Jordi over r1: "prima schets, alleen de bol onderin is nog niet rond".
- Jordi: "nu beter maken" · "laat maar eindresultaat pas zien" → maker-rondes, keurder en Dragonfly Cave-eindkeuring eerst, daarna pas naar Jordi.
- Sprite r2 (`sprite/r2/`): bollen rond (≤0,5 px), banden/kragen over de hele buis; panelen nog vlekkerig → r3 (verse maker) op de panelen.
- Jordi: "maar niks opnieuw tekenen he?" → maker r3: panelen uit de modelreductie, alleen pixelreparaties. (Let op: r2 bouwde bollen/buizen uit gemeten modelgeometrie i.p.v. de pixels over te nemen.)
- Jordi: "model volgen" · "er wordt van alles opnieuw getekend" → r3 vanaf de kale modelreductie, alleen pixelreparaties, diffkaart verplicht.
- Jordi: "enige wat mag afwijken is wat we besproken hebben, maar dat kan prima zonder opnieuw te tekenen".
- Sprite r3 (`sprite/r3/`, vanaf kale reductie, 256 afwijkingen met reden in log): vorm volgt het model; ogen en paneelraster nog zwak → r4.
- Sprite r4 (`sprite/r4/`, 240 afwijkingen van kaal, alle besproken): ogen ring+iris+pupil, panelen 4/3 vakken, zwart alleen schaduwkant → keurder.
- Sprite r5 (`sprite/r5/`, 23 MOET-reparaties keuring_r4) → eindkeuring DFC r5 **PASS** (`eindkeuring_r5/`, 28 indexwissels, silhouet gelijk). Ter info: panelen donkerder dan fase 2; op 1× kleiner/luchtiger dan fase 2 (`check/lijn_fase1_2_3.png`); stang tweeling open. Naar Jordi.
- Jordi na eindresultaat r5: "is nog heel erg blurry" · "en dat komt denk ik door het model" · "dat die het vak niet vult" · "ben bang weer een niewue gemini ronde" → compacte modelvarianten A/B/C (maker) + reserveprompt `gemini/PROMPT_r10.md`.
- Jordi: "eindeloos fixen gaat meestal niet goed" → prompt r10 naar Jordi.
- r10 (`gemini/r10.png`), Jordi: "niet gelukt". → terug naar r13b met compacte varianten (maker).
- Compacte varianten (`model/compact_*`, alleen hele vakken weg): A 3/3 mast 3 → 64×46, B mast 2 → 64×42, C 2/2 mast 3 → 64×52 (oog ±8 px). Breedte begrenst overal.
- Jordi: "maar met 2 panelen is het niet echt ruimtestation meer he" · "maar gaat A wel echt beter worden dan?" · "ja, doe die kleurronde maar" → r13b/4 vakken blijft; kleurronde r6 (minder tinten, harder contrast, silhouet gelijk) in `kleur_r6/`.
- Kleurronde r6 (`kleur_r6/`): romp 6→3 tinten, kragen donkerder paars, panelen eigen vakkleur + helderder raster; alpha-diff 0. Naar Jordi (nog geen keurder).
- Jordi over r6: "ok er zijn eigenlijk 2 issues, de panelen lezen niet als panelen omdat ze te weinig gedefinieerd zijn en de bollen zijn niet groot genoeg, de bollen kan je simpel vergroten, maar wat te doen met de panelen? dat zijn gewoon blauwe vlakken met een paarse lijn, geen kleuren, geen schaduwen, niks, dat veroorzaakt pixelblur, plus dat de bovenste achter de linksachterste staat ipv ervoor" · welke bollen: "de 3 oogbollen met zichtbare ogen erin". Voorstel Claude: paneelrecept van fase 2 (3 vaktinten, lichte rand, lichtere rasterlijnen); bollen ×1,2 en ×1,3 in het model → r7 (`sprite/r7/`).
- r7 (`sprite/r7/`): bollen ×1,2 en ×1,3 (alleen het voorste oog wordt zichtbaar groter; zij-ogen ±gelijk), PB vóór PA, panelen in fase 2-kleuren (3 vaktinten, lichte rand). Naar Jordi.
- Jordi over r7: "rechts het beste, maar de twee kleinere bollen hebben nog steeds amper ogen en de panelen zijn allemaal net wat te smal denk ik" → r8 vanaf r7 ×1,3: zijbollen ×1,6/×1,8, panelen breder ×1,3/×1,5.
- r8 (`sprite/r8/`): 4 varianten s16p13, s16p15, s18p13, s18p15; zij-ogen nu ring+iris+pupil. Naar Jordi.
- Jordi over r8: "ze zijn allemaal nog niet super afgewerkt, dus het grootste kan gewoon, probeer de vormen goed te herstellen, rond rond, rechthoekig rechthoek, de panelen in het midden groeien niet mee, het oog netjes erin zetten, maar ik denk dat we er wel komen" → r9 vanaf s18p15 (verse maker).
- r9 (`sprite/r9/`): bollen rond (≤0,5 px), ogen ring 8/6 + iris + pupil 2×2, panelen als parallellogrammen met fase 2-recept; mast PB ×2,0 en PF ×2,5 (keuze maker, = ×1,5 zichtbare breedte). Naar Jordi.
- Jordi over r9: "weer een stap vooruit, oog rechts mag iets netter afgemaakt worden, de panelen mogen nog iets consistenter qua grootte, houd rekening met de hoek he" → r10.
- r10 (`sprite/r10/`): rechteroog 1 px naar rechts, ring gelijk; linkeroog zelfde vorm (niet gevraagd, terug te zetten); panelen in de ruimte even groot met gemeten perspectief (PE 1, PD 0,90, PC 0,89, PA 0,80), mast PB/PF 6,9 px breed; open: PA 25% korter (of 0,89 zoals PC). Naar Jordi.
- Jordi over r10: "de ogen zijn nu zwarte vierkanten, allemaal dezelfde grootte en zelfde blik, dit moet nog wat meer driekwart, vooral de zijwaartse ogen. Rechterbol is niet goed bol, het maakt niet uit dat die dan het paneel overlapt. Kijk naar hoe het model dat doet. Bovenste paneel is een beetje afgekapt, onderste moet ook nog net wat verder doorlopen" → r11 (verse maker).
- r11 (`sprite/r11/`): ogen uit het model (driekwart, ring links dun/rechts dik, pupil links), rechterbol rond vóór PC, PB +1 px, PF loopt onder PE door. Claude: zij-ogen lezen nu als smalle strookjes. Naar Jordi.
- Jordi over r11: "ik vind de ogen nu goed anders. Bovenste paneel moet alleen ietsje naar links, omdat het nu op een vlag lijkt, maar de stok moet in het midden zitten ipv helemaal links, zelfde voor onderste paneel. Verder lijkt onderste en rechtsboven allebei nog lichtjes afgekapt he. Ik snap dat ze overlappen, maar zijn nog een paar pixels leeg waar ze niet overlappen" → r12.
- r12 (`sprite/r12/`): PB/PF gecentreerd om de stok, PC/PE-punten compleet; PF nu bijna geheel achter voorbuis en PE (strook 3 px). Keuze Jordi: PF vóór de voorbuis?
- Jordi over r12: "rechtsboven paneel opgelost, boven is nu juist te ver doorgecschoven en onder heb je nu bijna helemaal weggehaald" → r13 varianten PB −1,5/−2, PF r11-positie/−1,5.
- Jordi over PF: "hij moet overlapt worden maar op een goede manier".
- r13 (`sprite/r13/`): varianten A–D (PB −1,5/−2; PF lang 61 modelpx, r11-plek of −1,5). Naar Jordi.
