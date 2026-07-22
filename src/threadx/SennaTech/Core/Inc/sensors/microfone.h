#ifndef SENSORS_MICROFONE_H_
#define SENSORS_MICROFONE_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "utils.h"

typedef struct {
	float noise_alpha;
	float dc_alpha;
	float threshold_factor;
	float min_peak;
	float min_rms;
	ULONG refractory_ms;
} MicrofoneConfig_t;

typedef struct {
	MicrofoneConfig_t cfg;
	float noise_floor;
	float dc_estimate;
	ULONG last_clap_ms;
	bool initialized;
} MicrofoneState_t;

/*
 * Configura limites padrao para comecar testes de deteccao de palma.
 */
void Microfone_DefaultConfig(MicrofoneConfig_t *cfg);

/*
 * Inicializa estado interno do detector.
 */
void Microfone_Init(MicrofoneState_t *state, const MicrofoneConfig_t *cfg);

/*
 * Processa um bloco PCM (16-bit) e retorna true quando detecta uma palma.
 * now_ms pode vir de HAL_GetTick().
 */
bool Microfone_ProcessBlock(MicrofoneState_t *state,
							const int16_t *samples,
							size_t sample_count,
							ULONG now_ms);

#endif /* SENSORS_MICROFONE_H_ */
