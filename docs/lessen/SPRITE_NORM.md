# Sprite-norm (één pagina) – verplicht voor elke sprite-agent

Lees alleen dit + `SPEC.md`/`AFGEKEURD.md` van je Pokémon + de referenties in de map. Lange achtergrond (alleen bij twijfel): `FAKEMON_CHECKLIST.md`, `SPRITING.md`, `SPRITE_OPDRACHT.md`, `vormstudie/STUDIE.md`.

## Formaat
Gen 3: 64×64, anim_front 64×128 (2 frames), 16 kleuren, index 0 transparant, PNG met transparency=0. Fase 1: ±800–950 px, box ±40×40 (langnek/staart mag iets meer; vorm gaat vóór het getal). Fase 2 ≈ 1,5–1,7×, fase 3 ≈ 2,4×.

## Harde eisen (elk pass/fail; één fail = terug)
1. **Leest op 1× als een echte Pokémon** naast 10+ echte sprites van hetzelfde bouwtype; toets wat je **ziet**, niet wat er in de pixels staat.
2. **3/4 naar links-voor**; de kop draait meer naar de kijker dan het lijf. Lange snuit → één oog, neus vooraan; korte snuit → twee ogen, neus ertussen.
3. **Alle ledematen tellen op 1×** (viervoeter: 4 poten zichtbaar, verre in schaduwtint, kleiner/hoger), elk vast aan het lijf, elk in een eigen kolom met lucht ertussen, geen stokpoten (≥5–6 px dik), gewrichten (hak/elleboog). **Diagonaal lopen**, nooit telgang (uitzondering: kameelachtigen).
4. **Geen Escher**: overlap consequent (dichtbij over veraf), poten aan schouder/heup.
5. **Lijf over een echte sprite als skelet**, geleidelijke curven, geen doos-romp/doos-kop, geen rechte lijnen ≥ 4 px waar het dier rond is, niets symmetrisch.
6. **Kop**: fase 1 ±40–55% van de hoogte, kopoppervlak niet boven ±41%; geen te lange schedel.
7. **Ogen geïntegreerd**: donker bovenlid, iris donker boven/licht onder, glans; geen brilogen, geen zwevende wenkbrauw (boogje direct op de rand).
8. **Kenmerken op 1× leesbaar** (klauwen, staart, masker); geen klodders, streepjes of harken.
9. **Omlijning** per kleurgroep, zwart alleen aan de schaduwkant; licht van linksboven; geen open randen (ook schaduwkleur naast transparant).
10. **Geen "Chernobyl"**: geen misvormd gezicht, geen beige/crème vlakken uit het niets, geen losse/zwevende delen.

## Werkwijze
- **Goedgekeurd = bevroren**: pixeldiff 0 buiten je opdrachtzone (bewijs met script). Nooit herbouwen wat goed was; geen herschaling van de kop.
- **Referentie = specificatie**: wat Jordi aanwijst neem je over en meet je na.
- **Jordi's woorden** staan letterlijk in je opdracht; een nieuwe instructie vult aan, vervangt niet.
- **Zelfgenoemd zwak punt = fail**: "zwak", "twijfel", "leest eerder als…", "Jordi kan zeggen…" → repareren, niet opleveren.
- Met de hand tekenen (pixel-over/tekst-raster). Eén vergelijkingsvel (1× en 3× naast 3–6 referenties) + uitsneden van wat je keurde; niet meer.
- Lessen onder "Lessen" in je NOTITIES.md; niet committen tenzij gevraagd.
