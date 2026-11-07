# SPRITE-KERN: de enige pagina die je vóór spritewerk MOET lezen
Samengevat uit alle spritelessen (5 nov, Jordi: "vat de lessen echt enorm samen ... hij vergeet heel vaak lessen mee te nemen"). Geef dit bestand mee aan **elke** sprite-agent, ook bij kleine reparaties. Al het andere in `docs/lessen/` is naslag.

**BELANGRIJKSTE REGEL: een model van Jordi namaken (Jordi, 6 nov: "dit is de belangrijkste regel vanaf nu").** Levert Jordi een model (eigen ontwerp/afbeelding) om na te maken, dan zijn er precies twee eisen, en verder niets: (1) **lijkt hij heel accuraat op het origineel** (niets toevoegen, weglaten of herinterpreteren; het model is perfect); (2) **is het een Gen 3-sprite volgens al onze eisen** (deze pagina). Keurders toetsen alleen deze twee; "welk dier leest het", eigen ontwerpideeën of stijlwensen die het model veranderen tellen niet. Voorbeeld: poedelmot (`docs/concept/sprites/poedelmot/SPEC.md`). **Wat Jordi niet noemt is niet goedgekeurd** (Jordi: "als ik iets niet benoem betekent het niet dat het perfect is"): bevroren is alleen wat expliciet accuraat verklaard is.

**Ontwerp uit Gemini?** Volg `SPRITE_WERKWIJZE.md` → "Gemini-model namaken" (meetgereedschap poedelmot) en `docs/lessen/GEMINI.md`; die vervangen stap 1–3 hieronder (Gemini-keuze van Jordi = bevroren ontwerp; sprite = trouwe vertaling; keurder toetst trouw + techniek, niet het ontwerp).

## Volgorde (nooit overslaan)
1. **Ontwerp met Jordi**: pose + kenmerken, letterlijk in `SPEC.md` van de Pokémon. Foto's van Jordi direct in `referenties/` (komt een foto niet als bestand binnen: punt voor punt beschrijven).
2. **Bron voor de vorm** (Jordi, 5 nov: "blender model is geen vereiste, genoeg sprites zijn zonder blender ook gelukt"): kies wat werkt. **Foto in de juiste pose** (kolibrie-eindvorm, olinguito) of een **3D-poppetje/Blender-model** bij lastige 3/4-poses (kolibrie pre-evo, `docs/concept/sprites/kolibrie_pre/blender/kolibrie_pre.py`: één huid, geen losse bollen, eerst een rondom-vel). Nooit zelfgebouwde cirkels en driehoeken.
3. **Silhouet uit de bron** (foto-omtrek of render direct verkleind), de massa is heilig; met de hand alleen de dunne delen. Bij een model: toon het als **rode omtrek óver de render** en pas bij wijzigingen het **model** aan.
4. **Kleur** door één maker-agent: eerst kort bestuderen (Taillow/Starly/Fletchling of hetzelfde bouwtype op 8×, Dragonfly Cave-gids), dan met de hand als tekstraster. Met een model: toonkaart (model wit gerenderd, 4 tonen) als gids voor de schaduw.
5. **Claude kijkt zelf** op 8× naast Taillow, dan een **verse onafhankelijke keurder** (oordeelt eerst blind). Pas dan naar Jordi, met alleen de sprite.
6. Eerst alleen ontwerp + frontsprite. Frame 2, rug, icoon, shiny, naam en data komen **later voor alle soorten samen**.

## Harde regels (elke ronde controleren)
- **Goedgekeurd = bevroren**: pixeldiff 0 buiten de opdrachtzone, met script bewezen. Wat Jordi goedkeurde nooit herbouwen.
- **Jordi's woorden letterlijk** in SPEC en opdracht; nieuwe opmerking vult aan. Twijfelt Jordi: **eerst vragen wat hij ziet**, niet gokken. Bij twijfel over de omvang van een wijziging: vragen.
- **Model of keuze niet ongevraagd veranderen**; een idee = variant náást de gekozen versie.
- **Zelfgenoemd zwak punt = terug**, niet opleveren. Reparaties via de maker; daarna opnieuw keuren.
- **Toets de hoofdvraag eerst** (pose, kop, leest het als Pokémon op 1×?), pas daarna getallen (overlap, px). Groene getallen ≠ goed beeld.
- Een pose-probleem los je nooit op met kleurrondes.

## Hoe een Gen 3-sprite eruitziet (meetbaar)
- 3/4 naar links-voor, kop draait meer naar de kijker dan het lijf; ronde kop als eigen vorm; één oog bij een snavel/snuit opzij.
- **Netheid**: per kleurgroep ≤ 3 tinten + omlijning; geen tintvlakjes < 3 px (clusterscript) behalve glans; grenzen als vloeiende curven, geen trapjes, geen banding (tinten parallel aan de rand), geen pillow shading; licht linksboven, schaduw als sikkel die de vorm volgt.
- **Contrast**: helderheidsstappen meten tegen Taillow (±30–40 per tint).
- **Belijning**: buitenlijn 1 px; zwart alleen aan de schaduwkant, gekleurde selout aan de lichtkant; **nooit zwart en donkerlila om en om op één rand**; binnenlijnen alleen waar vorm over vorm valt, in een donkere tint van het vlak, taps; geen open randen, geen lichte kleur op de buitenrand.
- **Ogen**: neem een oog pixel voor pixel over van een echte sprite (zelf tekenen of opblazen geeft "geen Pokémon-oog"/"monster").
- **Pootjes/ledematen**: in perspectief (verre hoger en achter, nooit op één lijn naast elkaar), omlijnd, verre in schaduwtint; kleine vogelpootjes echt klein.
- **Vorm**: geen rechte stukken waar het dier rond is (buikrand!), geen knikken; snavel/dunne delen ≥ 2 px als het moet lezen.

## Zuinig
Eén maker per sprite (SendMessage), één keurder, kleine vellen, commit en push na elke ronde. Max 3–4 agents.
