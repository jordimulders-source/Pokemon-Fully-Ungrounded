# Project Grounded: muziek-merge-conflicten oplossen na `git merge <agent-commit>` (vanuit de hoofdmap draaien).
# midi.cfg 3-weg per sleutel, music_lint MAX_PER_SONG samenvoegen, rest beide kanten houden; daarna .align 2 in direct_sound_data.inc.
import re, subprocess, sys
files=subprocess.run(['git','diff','--name-only','--diff-filter=U'],capture_output=True,text=True).stdout.split()
special={'tools/grounded/music_lint.py'}
for p in files:
    s=open(p).read()
    if p=='tools/grounded/music_lint.py':
        def f(m):
            a,b=m.group(1),m.group(2)
            la=[l for l in a.split('\n') if l.strip()]; lb=[l for l in b.split('\n') if l.strip()]
            items=[]
            for l in la+lb:
                for it in re.findall(r"'[^']+\.mid': \d+", l):
                    if it not in items: items.append(it)
            return "".join("                %s,\n"%it for it in items[:-1]) + "                %s}\n"%items[-1]
        s=re.sub(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', f, s, flags=re.S)
    elif p=='sound/songs/midi/midi.cfg':   # 3-weg per sleutel: de kant die t.o.v. de basis veranderde wint
        def stage(n):
            r=subprocess.run(['git','show',':%d:%s'%(n,p)],capture_output=True,text=True).stdout
            return {l.split(':')[0]: l for l in r.split('\n') if ':' in l}
        base,ours,theirs=stage(1),stage(2),stage(3)
        def pick(k):
            if k in theirs and theirs.get(k)!=base.get(k): return theirs[k]
            return ours.get(k, theirs.get(k))
        def g(m):
            a=[l for l in m.group(1).split('\n') if l]; b=[l for l in m.group(2).split('\n') if l]
            keys=[]
            for l in a+b:
                k=l.split(':')[0]
                if k not in keys: keys.append(k)
            return ''.join(pick(k)+'\n' for k in keys if pick(k))
        s=re.sub(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', g, s, flags=re.S)
    else:
        s=re.sub(r'<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n', lambda m: m.group(1)+m.group(2), s, flags=re.S)
    assert '<<<<<<<' not in s, p
    open(p,'w').write(s); print('opgelost', p)
p='sound/direct_sound_data.inc'; L=open(p).read().split('\n'); out=[]
for l in L:
    if l.startswith('DirectSoundWaveData_') and l.endswith('::'):
        prev=[x for x in out if x.strip()][-1] if out else ''
        if prev.strip()!='.align 2': out += ['', '\t.align 2']
    out.append(l)
open(p,'w').write('\n'.join(out))
