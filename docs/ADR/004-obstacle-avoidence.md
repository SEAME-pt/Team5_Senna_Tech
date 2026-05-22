# [ADR-004] Multi-Phase Evasive Maneuver Sequence for Obstacle Avoidance
Status: Accepted

Date: 11-05-2026

### 1. Context and Problem Statement
When the ObstacleTracker flags an imminent hazard in the vehicle's direct corridor, the vehicle must perform an unmapped lateral lane detour. However, a simple binary state ("Avoiding" vs. "Normal") creates a dangerous control loop failure: as soon as the vehicle turns away from the obstacle to dodge it, the camera's fixed field of view no longer captures the object.

If the system blindly switches back to normal lane tracking the moment the obstacle disappears from the frame, the vehicle will steer back into the hazard prematurely. Additionally, executing a sudden maneuver requires filtering out traffic signs and light triggers to prevent the vehicle from stalling or braking unsafely while driving on an inverted trajectory.

### 2. Considered Options
Option A: Reactive Toggle Strategy (Steer away when the obstacle is detected; steer back immediately when the corridor is clear).

Option B: 4-Phase Evasive State Sequence (PREPARE_AVOID -> AVOIDING -> BLIND_WAIT -> RETURNING) integrated into the core FSM.

### 3. Decision Outcome
Chosen Option: **Option B**, because it provides explicit deterministic transitions through every physical milestone of an overtaking maneuver. The architecture isolates the evasive maneuver into four strictly sequential states:

PREPARE_AVOID: A 2-frame stabilization buffer where the PathPlanner begins displacing the target CTE before the vehicle reaches higher angular velocities.

AVOIDING: The active overtaking state. The vehicle maintains its lateral offset as long as the obstacle remains visible to the model.

BLIND_WAIT: Triggered when the obstacle disappears for more than 10 consecutive frames (OBSTACLE_LOST_THRESHOLD). The vehicle maintains its shifted trajectory, bypassing the object blindly for a fixed duration (blind_wait_time = 2.5s) to ensure physical clearance.

RETURNING: A controlled recovery phase where the target CTE is smoothly interpolated back to 0.0. Normal traffic state evaluation only resumes once the PathPlanner confirms the interpolation is complete.

### 4.Pros and Cons of the Options
**Option A:** Reactive Toggle Strategy
* Bad: Causes destructive state oscillation. The car would steer away, lose sight of the object, steer back into the object, see it again, and repeat this loop until a physical crash occurs.

**Option B:** 4-Phase Evasive Sequence
* Good: Completely neutralizes the camera blind spot bottleneck via the BLIND_WAIT timer.

* Good: Protects the vehicle from false environmental data; traffic light and area emergency checks are ignored while inside the avoidance state loop.

* Good: Restores the exact speed state the vehicle was traveling at prior to the detour (_pre_avoidance_state).

* Bad: Increases FSM code complexity, introducing state dependency variables that must be carefully reset if the maneuver is aborted by a sudden hard stop (ObstacleSituation.BRAKE).

### 5. Follow-up Tasks
None