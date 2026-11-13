# Charlatan-Alakazam: kleur r12 (rechterbovenarm grijs)

Basis: `basis_r11.txt` (= `../kleur_r11/var_r11.txt`). Jordi: "rechts dan ook he grappenmaker, bovenarm".

Bouwen: `python3 r12.py`, daarna `python3 vel.py`.

## Wijziging (alleen kleur, 8 px, zone x36–41, y28–34)
- Het hele armstuk tussen schouder en elleboog is nu grijs: (37–38,29), (38,30–31), (39,30–32), (40,33).
  - Vroeger was (37–38,29)/(38,30–31) de zwarte "rechterplaat" (n). In het model is dat D, het is dus deel van de arm.
- Tinten: b links (licht linksboven), c rechts en bij de elleboog. Het model heeft D links en B rechts. Die tinten zijn omgedraaid voor licht van linksboven, zoals bij de linkerbovenarm.
- De omlijning o rondom bestond al: (36,29), (37,30–31), (38,32), (39,33) naar de zwarte romp; (39,29), (40,30–32), (41,33) naar buiten; (39–40,34) naar de zwarte onderarm.

## Controle
- 8 px gewijzigd, 0 buiten de zone. Alpha-diff 0.
- Open randen 0, losse o 0. Clusters < 3 px: geen nieuwe.

## Zwak punt
- De arm is 1–2 px breed. Op 8× leest hij als een smalle grijze strook, smaller dan links. De vorm is niet veranderd.
