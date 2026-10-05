@ Project Grounded: drumkit voor Battle! Neo Team Plasma v4 (neo_plasma_theme.py). Gemeten aan het BW2-origineel:
@ een grote elektronische kick op elke tel (np_kick, pitch-sweep), hihats op de achtsten, crash/splash; geen droge
@ snare op 2 en 4. 36 kick, 37 snare (Power-kit), 38 hihat dicht, 39 hihat open (Electronic-kit), 40 crash, 41 splash.
voice_group neo_plasma_drumset, 36
	voice_directsound 60, 0, DirectSoundWaveData_np_kick, 255, 0, 255, 0
	voice_directsound 60, 0, DirectSoundWaveData_np_snare, 255, 0, 255, 100
	voice_directsound 60, 0, DirectSoundWaveData_np_hat_closed, 255, 0, 255, 60
	voice_directsound 60, 0, DirectSoundWaveData_np_hat_open, 255, 0, 255, 120
	voice_directsound_no_resample 60, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 67, 0, DirectSoundWaveData_trinity_cymbal_crash, 255, 200, 0, 140
