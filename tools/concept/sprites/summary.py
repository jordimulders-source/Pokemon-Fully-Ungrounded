"""Samenvatting van een of meer CSV's van measure.py (mediaan en p10-p90).

  python3 tools/concept/sprites/summary.py a.csv [b.csv ...]
"""
import sys, csv
import numpy as np

NUM = ['w', 'h', 'top', 'bottom', 'area', 'mass_cx', 'colors', 'darkest_lum', 'edge_darkest', 'edge_dark',
       'edge_light', 'edge_lum_tl', 'edge_lum_br', 'inner_darkest_frac', 'double_outline', 'n_ramps',
       'ramp_dl', 'ramp_dh', 'ramp_dh_signed', 'ramp_ds', 'light_dx', 'light_dy', 'shadow_frac',
       'highlight_frac', 'dither_px', 'isolated_px', 'checker_px', 'checker_frac', 'frame_diff', 'frame_diff_after_shift',
       'back_w', 'back_h', 'back_bottom', 'back_area', 'back_cut']


def stats(rows, k):
    v = np.array([float(r[k]) for r in rows if r.get(k) not in (None, '', 'None')])
    if len(v) == 0:
        return '-'
    return '%7.3g [%5.3g..%5.3g]' % (np.median(v), np.percentile(v, 10), np.percentile(v, 90))


for fn in sys.argv[1:]:
    rows = list(csv.DictReader(open(fn)))
    print('==', fn, len(rows))
    groups = {'alle': rows}
    for st in '123':
        groups['fase' + st] = [r for r in rows if r['stage'] == st]
    groups['eind'] = [r for r in rows if r['has_evo'] == '0']
    print('%-22s' % 'maat', ' '.join('%-24s' % g for g in groups))
    for k in NUM:
        print('%-22s' % k, ' '.join('%-24s' % stats(g, k) for g in groups.values()))
    print('n', [len(g) for g in groups.values()])
