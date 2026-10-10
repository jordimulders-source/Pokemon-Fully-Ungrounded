"""Project Grounded: MP2K-sporen met tijd uitlezen (noten per tick, tempo, loop), voor remixes van rips (v0.9.244).
song_events(rom, songtabel, nummer) -> dict(tracks=[dict(notes=[(tick, cmd, key, vel)], voices=[(tick, prog)],
loop=(start_tick, end_tick) of None)], tempos=[(tick, bpm)], header=offset). 24 ticks per tel."""
import struct

W = list(range(25)) + [28, 30, 32, 36, 40, 42, 44, 48, 52, 54, 56, 60, 64, 66, 68, 72, 76, 78, 80, 84, 88, 90, 92, 96]
ARG1 = {0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC8}


def song_events(path, table, num):
    rom = open(path, 'rb').read()
    u32 = lambda o: struct.unpack_from('<I', rom, o)[0]
    off = lambda p: p - 0x08000000
    hdr = off(u32(off(table) + 8 * num))
    ntr = rom[hdr]
    out = dict(tracks=[], tempos=[], header=hdr)
    for i in range(ntr):
        o = off(u32(hdr + 8 + 4 * i))
        t, pos, rs, stack, key, vel = 0, {}, None, [], 60, 100
        notes, voices, loop = [], [], None
        for _ in range(500000):
            pos.setdefault(o, t)
            b = rom[o]
            if b >= 0x80:
                c = b
                o += 1
                if c >= 0xBD:
                    rs = c
            else:
                c = rs
            if c <= 0xB0:
                t += W[c - 0x80]
                continue
            if c == 0xB1:
                break
            if c == 0xB2:
                loop = (pos.get(off(u32(o))), t)
                break
            if c == 0xB3:
                stack.append(o + 4)
                o = off(u32(o))
                continue
            if c == 0xB4:
                if stack:
                    o = stack.pop()
                continue
            if c == 0xB5:
                o += 5
                continue
            if c == 0xB9:
                o += 3
                continue
            if c in ARG1:
                if c == 0xBB:
                    out['tempos'].append((t, rom[o] * 2))
                if c == 0xBD:
                    voices.append((t, rom[o]))
                o += 1
                continue
            if c == 0xCD:
                o += 2
                continue
            if c == 0xCE:
                if rom[o] < 0x80:
                    o += 1
                continue
            if c >= 0xCF:
                if rom[o] < 0x80:
                    key = rom[o]
                    o += 1
                    if rom[o] < 0x80:
                        vel = rom[o]
                        o += 1
                        if rom[o] < 0x80 and c != 0xCF:
                            o += 1
                notes.append((t, c, key, vel))
        out['tracks'].append(dict(notes=notes, voices=voices, loop=loop))
    return out
