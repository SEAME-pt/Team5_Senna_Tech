"""High-level CTE and maneuver controller for taxi robot mission integration."""

import logging

from decision.decision_fsm import State
from decision.robotaxi_mission import TaxiManeuver

from .parking_in import ParkingInPolicy
from .parking_out import ForcedManeuverWindow, ParkingOutTimer, ReturningProfile

log = logging.getLogger("TaxiRobotCTEController")


class TaxiRobotCTEController:
	"""Owns ArUco maneuver transitions and CTE manipulation strategy."""

	def __init__(
		self,
		lane_offset: float = 0.80,
		return_duration_s: float = 1.5,
		cross_left_forced_trigger_m: float = 0.788,
		cross_right_forced_trigger_m: float = 0.688,
		cross_right_forced_duration_s: float = 12.0,
	):
		self._forced = ForcedManeuverWindow()
		self._parking_out_timer = ParkingOutTimer(duration_s=5.0)
		self._returning = ReturningProfile(
			lane_offset=lane_offset,
			return_duration_s=return_duration_s,
		)
		self._parking_in_policy = ParkingInPolicy()

		self.cross_left_forced_trigger_m = cross_left_forced_trigger_m
		self.cross_right_forced_trigger_m = cross_right_forced_trigger_m
		self.cross_right_forced_duration_s = cross_right_forced_duration_s

		self._cte_only_during_forced_states = {
			"PARKING_OUT_LEFT",
			"CROSS_LEFT",
			"CROSS_RIGHT",
		}
		self._last_forced_active = False

	def update_maneuver_state(
		self,
		fsm,
		taxi_maneuver: TaxiManeuver,
		aruco_id: int | None,
		aruco_distance_m: float | None,
	) -> None:
		forced_active = self._forced.is_active()

		if not forced_active:
			if taxi_maneuver == TaxiManeuver.PARKING_OUT_LEFT:
				changed = fsm.signal_robotaxi_state(State.PARKING_OUT_LEFT, "Exiting parking zone: left bias")
				if changed:
					self._forced.start("PARKING_OUT_LEFT")
			elif taxi_maneuver == TaxiManeuver.PARKING_OUT_RIGHT:
				fsm.signal_robotaxi_state(State.PARKING_OUT_RIGHT, "Exiting parking zone: right bias")
			elif taxi_maneuver == TaxiManeuver.CROSS_LEFT:
				changed = fsm.signal_robotaxi_state(State.CROSS_LEFT, "ArUco 13: Executing cross left")
				if (
					changed
					and aruco_id == 13
					and aruco_distance_m is not None
					and aruco_distance_m <= self.cross_left_forced_trigger_m
				):
					self._forced.start("CROSS_LEFT")
			elif taxi_maneuver == TaxiManeuver.CROSS_RIGHT:
				changed = fsm.signal_robotaxi_state(State.CROSS_RIGHT, "ArUco 11 detected: leaving crossing")
				if (
					changed
					and aruco_id == 11
					and aruco_distance_m is not None
					and aruco_distance_m <= self.cross_right_forced_trigger_m
				):
					self._forced.start("CROSS_RIGHT", duration_s=self.cross_right_forced_duration_s)
			elif taxi_maneuver == TaxiManeuver.PARKING_IN_LEFT:
				fsm.signal_robotaxi_state(State.PARKING_IN_LEFT, "ArUco 11 detected: entering parking")
			elif taxi_maneuver == TaxiManeuver.PARKING_IN_RIGHT:
				fsm.signal_robotaxi_state(State.PARKING_IN_RIGHT, "ArUco 12: Approaching parking from right")

			if self._parking_in_policy.should_transition_to_returning(fsm.state, aruco_id):
				self._set_returning_state(fsm, "Parking-in complete, ArUco lost")

		if (
			not forced_active
			and self._last_forced_active
			and fsm.state in (State.PARKING_OUT_LEFT, State.PARKING_OUT_RIGHT)
		):
			self._set_returning_state(fsm, "Forced parking-out completed")

		self._parking_out_timer.update(
			fsm.state in (State.PARKING_OUT_LEFT, State.PARKING_OUT_RIGHT)
		)
		if self._parking_out_timer.complete():
			self._set_returning_state(fsm, "Parking-out timeout completed")

		self._last_forced_active = self._forced.is_active()

	def resolve_drive_state(self, fsm, env_state):
		forced_active = self._forced.is_active()

		if forced_active:
			forced_state_name = self._forced.state_name()
			forced_state = getattr(State, forced_state_name, None) if forced_state_name else None
			current_state = forced_state if forced_state is not None else State.PARKING_OUT_LEFT
		else:
			current_state = fsm.process(
				env_state,
				planner_return_complete=self._returning.return_complete(),
			)

		pid_reset_needed = forced_active != self._last_forced_active
		self._last_forced_active = forced_active
		return current_state, pid_reset_needed

	def calculate_target_cte(self, current_state) -> float:
		forced_cte = self._forced.forced_cte()
		if forced_cte is not None:
			self._returning.update_deviation_side(forced_cte)
			return forced_cte

		if current_state.name in self._cte_only_during_forced_states:
			maneuver_cte = None
		else:
			maneuver_cte = self._forced.maneuver_cte_by_state.get(current_state.name)

		if maneuver_cte is not None:
			self._returning.update_deviation_side(maneuver_cte)
			return maneuver_cte

		returning_cte = self._returning.target_cte_for_returning(
			is_returning_state=(current_state == State.RETURNING)
		)
		if returning_cte is not None:
			return returning_cte

		return 0.0

	def forced_steering_override(self) -> float | None:
		return self._forced.steering_override()

	def reset(self) -> None:
		self._forced.reset()
		self._parking_out_timer.reset()
		self._returning.reset()
		self._last_forced_active = False

	def _set_returning_state(self, fsm, reason: str) -> None:
		if fsm.state != State.RETURNING:
			log.info("FSM Transition: %s -> %s [%s]", fsm.state.name, State.RETURNING.name, reason)
		fsm.state = State.RETURNING
		self.reset()
