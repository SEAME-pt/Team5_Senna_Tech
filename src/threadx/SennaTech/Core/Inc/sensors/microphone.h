#ifndef SENSORS_MICROPHONE_H_
#define SENSORS_MICROPHONE_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "utils.h"
#include "can_manager.h"

typedef struct {
	float noise_alpha;
	float dc_alpha;
	float threshold_factor;
	float min_peak;
	float min_rms;
	ULONG refractory_ms;
	ULONG warmup_blocks;
	float rearm_ratio; /* fração do threshold abaixo da qual volta a armar */
} MicrophoneConfig_t;

typedef struct {
	MicrophoneConfig_t cfg;
	float noise_floor;
	float dc_estimate;
	ULONG last_clap_ms;
	ULONG processed_blocks;
	bool initialized;
	bool armed; /* false logo após uma palma, até o som sossegar */

	/* debug */
	float last_peak_abs;
	float last_avg_abs;
	float last_threshold;
} MicrophoneState_t;

/*
 * Configure default thresholds to start clap detection tests.
 */
void Microphone_DefaultConfig(MicrophoneConfig_t *cfg);

/*
 * Initialize detector internal state.
 */
void Microphone_Init(MicrophoneState_t *state, const MicrophoneConfig_t *cfg);

/*
 * Process a 16-bit PCM block and return true when a clap is detected.
 * now_ms can come from HAL_GetTick().
 */
bool Microphone_ProcessBlock(MicrophoneState_t *state,
							const int16_t *samples,
							size_t sample_count,
							ULONG now_ms);

/*
 * Print current detector readings over UART (peak, avg, floor, threshold).
 */
void Microphone_PrintDebug(const MicrophoneState_t *state);

#endif /* SENSORS_MICROPHONE_H_ */