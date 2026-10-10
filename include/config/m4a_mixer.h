#ifndef GUARD_CONFIG_M4A_MIXER_H
#define GUARD_CONFIG_M4A_MIXER_H

// Project Grounded (v0.9.240): HQ-mixer van ipatix (MIT, github.com/ipatix/gba-hq-mixer, src/m4a_hq_mixer.s).
// De standaard m4a-mixer telt elk kanaal op in een 8-bit-buffer en rondt dus per kanaal af: elk zacht kanaal brengt
// zijn eigen afrondingsruis mee (gemeten: ruisvloer -32 dB, op donkere nummers als de Yoshi's Island-rips
// hoorbaar als 'overload'). De HQ-mixer telt op in 16 bit, rondt één keer af (met noise shaping) en klemt
// i.p.v. om te slaan. Alleen voor dit bestand en de .s-bestanden: hier mogen alleen #defines staan.
// 0 = oude mixer (src/m4a_1.s), 1 = HQ-mixer.
#define M4A_HQ_MIXER 1

#endif // GUARD_CONFIG_M4A_MIXER_H
