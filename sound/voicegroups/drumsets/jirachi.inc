@ Project Grounded: drumkit voor Battle! Jirachi (jirachi_theme.py), alles DirectSound: 36 kick, 37 roffel,
@ 38 snare, 39 crash, 40 triangel, 41 windgong (jirachi_chimes), 42 belletjes.
voice_group jirachi_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0
	voice_directsound 72, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 100
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 160
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound_no_resample 64, 80, DirectSoundWaveData_sd90_open_triangle, 255, 242, 103, 188
	voice_directsound 96, 50, DirectSoundWaveData_jirachi_chimes, 255, 252, 0, 200
	voice_directsound_no_resample 64, 84, DirectSoundWaveData_sc88pro_jingle_bell, 255, 0, 255, 120

