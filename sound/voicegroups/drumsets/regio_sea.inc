@ Project Grounded: drumkit voor regio_theme.py (zee). Alleen stock-samples, geen PSG.
@ 36 kick, 37 snare, 38 tamboerijn, 39 crash, 40 bekkenzwel, 41 pauk.
@ voice_directsound (niet _no_resample): speelt op de rate van de sample, niet op de mixersnelheid.
voice_group regio_sea_drumset, 36
	voice_directsound 62, 64, DirectSoundWaveData_drum_and_percussion_kick, 255, 0, 255, 180
	voice_directsound 58, 64, DirectSoundWaveData_sc88pro_orchestra_snare, 255, 0, 255, 160
	voice_directsound 60, 76, DirectSoundWaveData_sc88pro_tambourine, 255, 0, 255, 150
	voice_directsound 60, 64, DirectSoundWaveData_trinity_cymbal_crash, 255, 235, 0, 165
	voice_directsound 54, 52, DirectSoundWaveData_sc88pro_orchestra_cymbal_crash, 30, 0, 255, 150
	voice_directsound 43, 64, DirectSoundWaveData_sc88pro_timpani, 255, 246, 0, 180
