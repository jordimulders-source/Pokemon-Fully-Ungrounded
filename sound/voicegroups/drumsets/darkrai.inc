@ Project Grounded: drumkit voor Battle! Darkrai (darkrai_theme.py), alles DirectSound: 36 kick, 37 snare,
@ 38 hihat, 39 crash, 40 omgekeerd bekken (darkrai_revcym, 1,4 s), 41 taiko, 42 lage tom, 43 hartslag
@ (kick 10 halve tonen lager), 44 tikje (het mechaniek van de speeldoos).
voice_group darkrai_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_sc88pro_rnd_snare, 255, 0, 255, 160
	voice_directsound_no_resample 60, 74, DirectSoundWaveData_unknown_close_hihat, 255, 127, 0, 120
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_darkrai_revcym, 255, 0, 255, 120
	voice_directsound 60, 64, DirectSoundWaveData_sc88pro_taiko, 255, 0, 255, 0
	voice_directsound 55, 52, DirectSoundWaveData_sd90_ambient_tom, 255, 0, 255, 120
	voice_directsound 50, 64, DirectSoundWaveData_sc88pro_rnd_kick, 255, 0, 255, 0
	voice_directsound 84, 76, DirectSoundWaveData_ethnic_flavours_hyoushigi, 255, 0, 255, 60

