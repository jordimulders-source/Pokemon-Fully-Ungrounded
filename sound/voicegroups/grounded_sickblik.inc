@ Project Grounded: grounded_gm voor Battle! SickBlik (slap-funk). Gegenereerd door tools/grounded/sickblik_theme.py.
@ 4/5 = Rhodes Em9/A13, 7 = clavinet, 26/27 = wah-chank A9/Em9, 28 = scratch, 29 = gedempte gitaar, 34-37 = slap bass (thumb, pop, dode thumb, dode pop), 38 = flageolet, 30/31 = jazzgitaar-octaven, 59/60 = gedempte trompet, 61/62 = hoorns, 80 = PSG-synth, 85 = talkbox, 90-97 = Rhodes-akkoorden, 100-107 = blazersakkoorden, 127 = drumkit.
voice_group grounded_sickblik
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 0
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 1
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 2
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 3
	voice_directsound 60, 0, DirectSoundWaveData_sb_rhodes_m9, 255, 0, 255, 200  @ 4
	voice_directsound 60, 0, DirectSoundWaveData_sb_rhodes_13, 255, 0, 255, 200  @ 5
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 6
	voice_directsound 60, 0, DirectSoundWaveData_sb_clav, 255, 0, 255, 140  @ 7
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 8
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 242  @ 9
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 242  @ 10
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_xylophone, 255, 235, 0, 204  @ 11
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_xylophone, 255, 235, 0, 204  @ 12
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_xylophone, 255, 235, 0, 204  @ 13
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_glockenspiel, 255, 165, 51, 242  @ 14
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 15
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 16
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 17
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 18
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 19
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 20
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 21
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 22
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_organ2, 255, 0, 255, 127  @ 23
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 24
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 25
	voice_directsound 60, 0, DirectSoundWaveData_sb_gtr_wah_9, 255, 0, 255, 150  @ 26
	voice_directsound 60, 0, DirectSoundWaveData_sb_gtr_wah_m9, 255, 0, 255, 150  @ 27
	voice_directsound 60, 0, DirectSoundWaveData_sb_gtr_scratch, 255, 0, 255, 120  @ 28
	voice_directsound 60, 0, DirectSoundWaveData_sb_gtr_mute, 255, 0, 255, 140  @ 29
	voice_directsound 60, 0, DirectSoundWaveData_sb_jazz_oct, 255, 0, 255, 200  @ 30
	voice_directsound 60, 0, DirectSoundWaveData_sb_jazz_oct_hi, 255, 0, 255, 200  @ 31
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149  @ 32
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_fingered_bass, 255, 253, 0, 149  @ 33
	voice_directsound 60, 0, DirectSoundWaveData_sb_slap_thumb, 255, 0, 255, 150  @ 34
	voice_directsound 60, 0, DirectSoundWaveData_sb_slap_pop, 255, 0, 255, 150  @ 35
	voice_directsound 60, 0, DirectSoundWaveData_sb_dead_thumb, 255, 0, 255, 100  @ 36
	voice_directsound 60, 0, DirectSoundWaveData_sb_dead_pop, 255, 0, 255, 100  @ 37
	voice_directsound 60, 0, DirectSoundWaveData_sb_bass_harm, 255, 0, 255, 225  @ 38
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_synth_bass, 255, 252, 0, 115  @ 39
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 40
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 41
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 42
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 43
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 44
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 45
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_harp, 255, 242, 51, 242  @ 46
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 226  @ 47
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 48
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 49
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 50
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 51
	voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 165  @ 52
	voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 165  @ 53
	voice_directsound 60, 0, DirectSoundWaveData_classical_choir_voice_ahhs, 255, 0, 255, 165  @ 54
	voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet  @ 55
	voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet  @ 56
	voice_keysplit voicegroup_tuba_keysplit, keysplit_tuba  @ 57
	voice_keysplit voicegroup_tuba_keysplit, keysplit_tuba  @ 58
	voice_directsound 60, 0, DirectSoundWaveData_sb_mute_tpt, 255, 0, 255, 170  @ 59
	voice_directsound 60, 0, DirectSoundWaveData_sb_mute_tpt_hi, 255, 0, 255, 170  @ 60
	voice_directsound 60, 0, DirectSoundWaveData_sb_horns, 255, 0, 255, 160  @ 61
	voice_directsound 60, 0, DirectSoundWaveData_sb_horns_hi, 255, 0, 255, 160  @ 62
	voice_keysplit voicegroup_trumpet_keysplit, keysplit_trumpet  @ 63
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 64
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 65
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 66
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 67
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 68
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 69
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 70
	voice_directsound 60, 0, DirectSoundWaveData_sd90_classical_oboe, 255, 165, 154, 127  @ 71
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 72
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 73
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 74
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 75
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 76
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 77
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 78
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_flute, 255, 127, 231, 127  @ 79
	voice_square_2 60, 0, 1, 0, 1, 9, 2  @ 80
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 81
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 82
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 83
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 84
	voice_directsound 60, 0, DirectSoundWaveData_sb_talkbox, 255, 0, 255, 185  @ 85
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 86
	voice_square_2 60, 0, 2, 0, 1, 7, 1  @ 87
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 88
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 89
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_cmaj9, 255, 0, 255, 200  @ 90
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_b7alt, 255, 0, 255, 200  @ 91
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_am9, 255, 0, 255, 200  @ 92
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_d13, 255, 0, 255, 200  @ 93
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_gmu, 255, 0, 255, 200  @ 94
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_fmaj7s11, 255, 0, 255, 200  @ 95
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_fsm7b5, 255, 0, 255, 200  @ 96
	voice_directsound 60, 0, DirectSoundWaveData_sb_rh_cmu, 255, 0, 255, 200  @ 97
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 98
	voice_keysplit voicegroup_strings_keysplit, keysplit_strings  @ 99
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_em9, 255, 0, 255, 190  @ 100
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_a13, 255, 0, 255, 190  @ 101
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_cmaj9, 255, 0, 255, 190  @ 102
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_b7alt, 255, 0, 255, 190  @ 103
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_am9, 255, 0, 255, 190  @ 104
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_d13, 255, 0, 255, 190  @ 105
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_gmu, 255, 0, 255, 190  @ 106
	voice_directsound 60, 0, DirectSoundWaveData_sb_br_fmaj7s11, 255, 0, 255, 190  @ 107
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 108
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 109
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 110
	voice_keysplit voicegroup_piano_keysplit, keysplit_piano  @ 111
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216  @ 112
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216  @ 113
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216  @ 114
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216  @ 115
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 0  @ 116
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 0  @ 117
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 0  @ 118
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 216  @ 119
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 120
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 121
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 122
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 123
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 124
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 125
	voice_noise_alt 60, 0, 0, 0, 1, 0, 0  @ 126
	voice_keysplit_all voicegroup_sickblik_drumset  @ 127
