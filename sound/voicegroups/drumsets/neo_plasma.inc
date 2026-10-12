@ Project Grounded: drumkit voor Battle! Neo Team Plasma v12 (neo_plasma_theme.py): de regels van rs_drumset
@ (standaard Emerald-kit): 36 kick, 38 snare, 39 clap, 40 orkestsnare, 42 dichte hihat, 46 open hihat,
@ 49 crash (rs_drumset 57, want 49 is daar PSG), 55 crash. Alles DirectSound.
voice_group neo_plasma_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 220
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_tr909_hand_clap, 255, 255, 255, 180
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 200
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 79, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 30, 54, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 255, 246, 0, 165
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_close_hihat, 255, 0, 0, 0
	voice_directsound_no_resample 60, 14, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 140
