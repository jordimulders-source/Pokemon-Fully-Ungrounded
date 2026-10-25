# Coathief: kleursprite ronde 4 (Jordi's feedback op 3b, nieuw silhouet `silhouet/ronde2.txt`)

Basis: ronde 3b. Alles buiten de vier zones is pixel voor pixel gelijk aan 3b. Studie en palet: `../ronde1/NOTITIES.md`; het palet is ongewijzigd sinds ronde 3.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `r3b_vs_r4_kop_poten.png`: kop, oren, mond, klauwen en voorpoten op 8×, ronde 3b naast ronde 4, op licht en op donker.
- `bron/`:
  - het blok "ronde 4" staat onderaan `reparaties.txt`. Een reparatie mag nu ook pixels toevoegen of weghalen (`.`); de alpha-controle gebeurt tegen het nieuwe silhouet;
  - `bouw.py` en `controle.py` werken met `silhouet/ronde2.txt`;
  - `diff_r3b.py` geeft per zone de verschillen met ronde 3b.

## Bewijs
```
controle.py: pixels 1319 | silhouet 1319 (ronde2.txt) | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r3b.py:
zone 1 oren                                  23 px
zone 2 mond                                   3 px
zone 3 klauwen opgetilde poot                35 px
zone 4 staande verre voorpoot                30 px
zone 4 losse teentjes y 62 (weg)              2 px
totaal 93 | buiten de zones: 0
```
In het totaal zitten 34 pixels die het silhouet zelf toevoegt of weghaalt.

## Per zone
1. **Oren:** klein en rond, met een crème rand (x waar het oor aan transparant grenst, c erbinnen) en een donkere binnenkant (m).
   - Nabij oor: rand x op y 31; `xccck` op y 32; `xmmmck` op y 33; de voet `zzmmzk` loopt over in de kop.
   - Ver oor: rand x op y 32, een donkere binnenkant en k aan de schaduwkant.
   - Op licht en op donker lezen ze als ronde oortjes, niet afgeknipt.
2. **Mond:**
   - de opgetrokken hoek op (12,45) is weg (weer z);
   - nieuw is een korte rechte lijn k (8–10,46), met m op (11,46) en een licht afhangend eind m op (12,47).
   - Neutraal, subtiel.
3. **Klauwen:**
   - y 56 is nu de voet (donker, met een lichtkant);
   - op y 57 zitten de aanzetten (c) met donkere teenvoegen;
   - twee lange haken naar linksvoor-onder (y 58–61). Elk heeft een crème kern c over de volle lengte, een glans w op (13,59) en (17,59), de schaduwkant n en een punt x.
   - De klauwen zijn 2 px breed en hebben geen binnenpixel. Daarom zit de glans aan de lichtkant; `controle.py` staat in de klauwzone n, c en w aan de rand toe.
   - Een versie met x als schaduwrand oogde op wit vaal. Met n zijn ze op 1× minstens zo licht en opvallend als de olinguito-klauwen.
4. **Staande verre voorpoot**, als cilinder in de schaduwtint:
   - Bovenarm (y 50–53, 6 breed): y-lichtkant links, z, m, k rechts. De overloop van de schouder (d/y) bovenaan is gebleven.
   - Onderarm (y 54–57): de lichtkant links.
   - Pols (y 57–58): een knik, want het licht verspringt naar rechts en de poot wordt 4 breed.
   - Platte voet naar voren (y 59–61): de bovenkant licht, donkere tenen vooraan en een k-onderrand op de grond.
   - De losse teentjes op y 62 zijn weg.

## Zelf bekeken (1×, 4× en 8×, licht en donker, naast 3b en de olinguito)
- De oren zijn rond en zichtbaar op beide achtergronden.
- De mond is rustig.
- De klauwen zijn lang en licht.
- De verre voorpoot draagt het lijf, met een pols en een voet.
- Het gezicht (oog, vlekken, muts) is ongewijzigd.
- Ik zie geen zwak punt.

## Lessen
- **Een oor van 2 rijen leest als een stompje.** Met een rand van 1 px x plus 1 rij c erbinnen en een donkere kern leest het als een rond coati-oor, ook op donker.
- **Een klauw van 2 px leest licht** als de schaduwkant n is (en niet x) en alleen de punt x krijgt.
- **Bij een gewijzigd silhouet:** laat de reparaties ook pixels toevoegen en weghalen. Tel de silhouetwijziging in de diff mee per zone, en sluit pixels die in beide versies transparant zijn uit.
