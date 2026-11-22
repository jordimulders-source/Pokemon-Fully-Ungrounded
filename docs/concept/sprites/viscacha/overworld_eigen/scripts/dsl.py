"""Rasters schrijven als {y: [(x,'pixels'), ...]} zodat kolommen niet verschuiven. Spatie = niets zetten."""
import numpy as np
def build(spec):
    a=np.zeros((32,32),np.uint8)
    for y,parts in spec.items():
        for x0,s in parts:
            for i,c in enumerate(s):
                if c==' ': continue
                a[y,x0+i]=0 if c=='.' else int(c,16)
    return a
