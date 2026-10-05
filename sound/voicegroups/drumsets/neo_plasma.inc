@ Project Grounded: drumkit voor Battle! Neo Team Plasma v5 (neo_plasma_theme.py): standaard GBA-samples
@ (rs_drumset). 36 kick, 37 off-beat-snare (kort), 38 snare, 39 open hihat, 40 crash,
@ 41 splash. Dichte hihats op het PSG-ruiskanaal (eigen spoor).
voice_group neo_plasma_drumset, 36
	voice_directsound 60, 0, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0
	voice_directsound_no_resample 62, 0, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 180
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 220
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_unknown_open_hihat, 255, 242, 141, 0
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 67, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 200, 0, 140
