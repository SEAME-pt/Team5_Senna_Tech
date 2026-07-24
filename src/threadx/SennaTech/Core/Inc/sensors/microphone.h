#ifndef SENSORS_MICROPHONE_H_
#define SENSORS_MICROPHONE_H_

#include <stdbool.h>
#include <stddef.h>
#include "utils.h"
#include "can_manager.h"

#define MICROPHONE_BLOCK_SAMPLES 160U
#define MICROPHONE_DEBUG_PERIOD_MS 1000U

extern MDF_HandleTypeDef AdfHandle0;
extern MDF_FilterConfigTypeDef AdfFilterConfig0;

typedef struct {
	float noise_alpha; // Smoothing for the "noise floor"
	float dc_alpha; // Smoothing for the filter estimating DC offset (silence/average level)
	float threshold_factor; // How far above background noise a sound must be to count as a peak
	float min_peak; // Absolute minimum threshold, even if background noise is very low
	float min_rms; // Minimum noise floor (avoids becoming too sensitive in total silence)
	ULONG refractory_ms; // Minimum time between two detections (avoids re-triggering on the same sound)
	ULONG warmup_blocks; // Number of initial blocks ignored, so the filters stabilize before detecting
	float rearm_ratio; // Factor used to "re-arm" detection after it fires
} MicrophoneConfig_t;

typedef struct {
	MicrophoneConfig_t cfg;
	float noise_floor;
	float dc_estimate;
	ULONG last_clap_ms;
	ULONG processed_blocks;
	bool initialized;
	bool armed; /* false logo após uma palma, até o som sossegar */
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

#endif /* SENSORS_MICROPHONE_H_ */