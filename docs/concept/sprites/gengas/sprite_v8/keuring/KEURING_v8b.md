# Keuring Gengas v8b (verse eindkeurder, 15 nov)
**Hoofdvraag: BIJNA.** Blind op 1×/2× naast Haunter, Koffing, Weezing en Gengar (`blind_1x2x_naast_gen3.png`) leest hij als één bol met een donkere wolkenband over het voorhoofd. Het gezicht ligt er niet in een kom en lijkt niet geplakt. Ogen en grijns zijn Gengars pixels op (x−6, y+5); de pupillen staan op Gengars plek (bijvoorbeeld (15,34)) en de tandlijn heeft exact Gengars tint. Buiten de gezichtszone en de krul is er geen verschil met v7, dus manen, linkeroor en het vlak onder het rechteroor volgen het model, zoals de v7-keuring al vaststelde. De krul loopt nu rond met trapjes van 1–2 px. Dat is opgelost. Op 8× is nog één plek aan te wijzen waar een apart gezichtsgebied begint (`vgl_gezicht_v8b_model_v8a_10x.png`).

## MOET
1. **Rechterrand van de gezichtszone** (x33|34, y30–38): de middentint 5 rond het rechteroog stopt op een kaarsrechte verticale naad van 9 rijen. Rechts daarvan begint een strook licht 6 van 3 px breed (x34–36). Dit is precies het "vlak om de ogen" waar Jordi over klaagt: de enige rechte rand in een sprite waar alle andere bandranden golven met trapjes. In het model loopt deze overgang schuin. Oplossing: de naad laten golven met trapjes van 1–3 px, zoals de onderrand van de band (y29–32), of schuin zoals in het model. Verder niets veranderen.

## MAG
- **Linksboven** (x8–13, y23–31): een grote egale vlek in tint 3. Dat komt door u → b. Op 1× valt het weinig op, maar het is het vlakste stuk van de bol.
- **Links van het linkeroog** (x8–12, y32–36): een effen strook in tint 5. De overgang naar 6 eronder loopt al met trapjes en is acceptabel.
- **Tandschaduw** (tint e, 186,185,183) is neutraalgrijs, terwijl Gengar 189,172,189 gebruikt. Tint 2/3 liggen maar ±15 helderheid uit elkaar. Beide zijn al bekend uit NOTITIES en v7.
- **v8a ter vergelijking:** daar ligt het gezicht weer in de donkere band (de "kuil" van het model). v8b is de betere keuze.
