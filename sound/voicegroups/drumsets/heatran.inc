@ Project Grounded: stoner-drumkit voor Battle! Heatran (heatran_theme.py), samples uit FluidR3 (gm_samples.py):
@ 36 kick, 37 snare, 38 open hihat, 39 ride, 40 floor tom, 41 middentom, 42 crash (links), 43 crash (rechts, lager).
voice_group heatran_drumset, 36
	voice_directsound_no_resample 60, 64, DirectSoundWaveData_heatran_kick, 255, 0, 255, 0
	voice_directsound_no_resample 60, 60, DirectSoundWaveData_heatran_snare, 255, 0, 255, 0
	voice_directsound_no_resample 60, 84, DirectSoundWaveData_heatran_open_hat, 255, 0, 255, 200
	voice_directsound_no_resample 60, 44, DirectSoundWaveData_heatran_ride, 255, 0, 255, 210
	voice_directsound 60, 40, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, 0
	voice_directsound 66, 80, DirectSoundWaveData_heatran_floor_tom, 255, 0, 255, 0
	voice_directsound_no_resample 60, 36, DirectSoundWaveData_heatran_crash, 255, 0, 255, 220
	voice_directsound 57, 92, DirectSoundWaveData_heatran_crash, 255, 0, 255, 220

