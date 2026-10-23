# Cuyby ronde 4: kleine punten uit de keuring

Basis: `../ronde3` (goedgekeurd). Voorstellen uit `checklist_keuring/KEURING.md` §1; Jordi is het ermee eens. Palet ongewijzigd, transparency=0. Frame 2 = dezelfde wijziging 1 rij hoger (zoals ronde 3).

| Punt | Wat | Waar (frame 1) | Pixels |
|---|---|---|---|
| A5/B3 verre oog smaller | kolom x24 van het linkeroog wordt vacht: (24,29) `a` (glans zwart, zoals de buurman), (24,30–32) crème `3`. Het oog is nu 4 breed, het rechter blijft 5. Glans (21–22) en weerkaatsing blijven. | x24, y29–32 | 4 |
| B5 zwart oor 1 px hoger | nieuwe toprij omlijning (21–23,15), rij y16 wordt `1 a b b 1` (kopie van y17). Oortoppen nu y15 (zwart) en y16 (oranje). | x20–24, y15–16 | 8 |

Totaal 12 px per frame (24 samen). **Pixeldiff buiten deze zones: 0** (`bron/` bevat `cuyby.py` + `lib.py`, die het bewijs uitrekenen). Geen open randen: alle nieuwe randpixels zijn omlijning `1`.

**Niet toegepast:** C6 (linker voetkussen 1 px hoger, ±6 px). Geprobeerd; op 3× werd het voetje een platte zwarte balk met een roze vlek erop, slechter dan ronde 3. Ronde 3 houden.
**Zelfcheck** (1× en 3× naast ronde 3, `checklist_keuring/TOEGEPAST.png`): gezicht even schattig; de ogen zijn geen kopieën meer en het gezicht draait leesbaar naar links. Het oor valt op 1× nauwelijks op, op 3× net.

## Jordi (23 okt)
Oogwijziging teruggedraaid ("oog is nu onafgemaakt"); alleen het zwarte oor 1 px hoger blijft. anim_front.png is met de hand teruggezet; `bron/` bouwt nog de versie mét oogwijziging.
