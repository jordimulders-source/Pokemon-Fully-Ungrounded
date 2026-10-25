"""Bouwt de Spritewerkplaats als één HTML-bestand: editor_template.html + po_engine.js + assets.json.
Gebruik: python3 build_editor.py uit.html"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, 'editor_template.html')).read()
t = t.replace('/*__ENGINE__*/', open(os.path.join(HERE, 'po_engine.js')).read())
t = t.replace('/*__ASSETS__*/', open(os.path.join(HERE, 'assets.json')).read())
open(sys.argv[1], 'w').write(t)
print(sys.argv[1], len(t) // 1024, 'kB')
