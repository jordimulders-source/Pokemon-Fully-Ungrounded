"""Blinde test: een verse Claude-sessie zonder projectcontext (cwd in de scratchpad,
geen CLAUDE.md) beoordeelt de rij. python3 run_blind.py <map met rij.png>"""
import os
import subprocess
import sys

d = os.path.abspath(sys.argv[1])
here = os.path.dirname(os.path.abspath(__file__))
prompt = open(os.path.join(here, 'blindprompt.txt')).read().strip()
prompt += ' The absolute path is %s.' % os.path.join(d, 'rij.png')
r = subprocess.run(['claude', '-p', '--allowedTools', 'Read'], input=prompt, cwd=d,
                   capture_output=True, text=True, timeout=900)
out = r.stdout + r.stderr
open(os.path.join(d, 'antwoord.txt'), 'w').write(out)
print(out)
