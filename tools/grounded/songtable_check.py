import re,sys,subprocess
def load(ref):
    get=lambda p: subprocess.check_output(['git','show',f'{ref}:{p}']).decode() if ref else open(p).read()
    tab=[]; f=0
    for l in get('sound/song_table.inc').split('\n'):
        if l.startswith('gSongTable:'): f=1; continue
        if f and re.match(r'\s*song ',l): tab.append(l.split()[1].rstrip(','))
    bad=0
    for m in re.finditer(r'#define (MUS_GROUNDED_\w+)\s+(\d+)',get('include/constants/songs.h')):
        name,n=m.group(1),int(m.group(2)); exp=name.lower()
        if n<len(tab) and tab[n]!=exp and tab[n] not in ('mus_dummy','mus_rg_vs_legend') and not exp.startswith(tab[n]):
            print(ref or 'werk',name,n,'->',tab[n]); bad+=1
    return bad
for r in sys.argv[1:] or ['']: print(r or 'werk','fouten:',load(r if r!='werk' else ''))
