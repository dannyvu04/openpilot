from cereal import car
from selfdrive.car.hyundai.values import DBC, STEER_THRESHOLD, FEATURES
from selfdrive.can.parser import CANParser
from selfdrive.config import Conversions as CV
from common.kalman.simple_kalman import KF1D

GearShifter = car.CarState.GearShifter

def get_can_parser(CP):

  signals = [
    # sig_name, sig_address, default
    ("WHL_SPD_FL", "WHL_SPD11", 0),
    ("WHL_SPD_FR", "WHL_SPD11", 0),
    ("WHL_SPD_RL", "WHL_SPD11", 0),
    ("WHL_SPD_RR", "WHL_SPD11", 0),

    ("YAW_RATE", "ESP12", 0),

    ("CF_Gway_DrvSeatBeltInd", "CGW4", 1),

    ("CF_Gway_DrvSeatBeltSw", "CGW1", 0),
    ("CF_Gway_TSigLHSw", "CGW1", 0),
    ("CF_Gway_TurnSigLh", "CGW1", 0),
    ("CF_Gway_TSigRHSw", "CGW1", 0),
    ("CF_Gway_TurnSigRh", "CGW1", 0),
    ("CF_Gway_ParkBrakeSw", "CGW1", 0),

    ("BRAKE_ACT", "EMS12", 0),
    ("PV_AV_CAN", "EMS12", 0),
    ("TPS", "EMS12", 0),

    ("CYL_PRES", "ESP12", 0),

    ("CF_Clu_CruiseSwState", "CLU11", 0),
    ("CF_Clu_CruiseSwMain", "CLU11", 0),
    ("CF_Clu_SldMainSW", "CLU11", 0),
    ("CF_Clu_ParityBit1", "CLU11", 0),
    ("CF_Clu_VanzDecimal" , "CLU11", 0),
    ("CF_Clu_Vanz", "CLU11", 0),
    ("CF_Clu_SPEED_UNIT", "CLU11", 0),
    ("CF_Clu_DetentOut", "CLU11", 0),
    ("CF_Clu_RheostatLevel", "CLU11", 0),
    ("CF_Clu_CluInfo", "CLU11", 0),
    ("CF_Clu_AmpInfo", "CLU11", 0),
    ("CF_Clu_AliveCnt1", "CLU11", 0),

    ("ACCEnable", "TCS13", 0),
    ("ACC_REQ", "TCS13", 0),
    ("DriverBraking", "TCS13", 0),
    ("DriverOverride", "TCS13", 0),

    ("ESC_Off_Step", "TCS15", 0),

    ("CF_Lvr_GearInf", "LVR11", 0),        #Transmission Gear (0 = N or P, 1-8 = Fwd, 14 = Rev)

    ("CR_Mdps_DrvTq", "MDPS11", 0),

    ("CR_Mdps_StrColTq", "MDPS12", 0),
    ("CF_Mdps_ToiActive", "MDPS12", 0),
    ("CF_Mdps_ToiUnavail", "MDPS12", 0),
    ("CF_Mdps_FailStat", "MDPS12", 0),
    ("CR_Mdps_OutTq", "MDPS12", 0),

    ("SAS_Angle", "SAS11", 0),
    ("SAS_Speed", "SAS11", 0),

  ]

  checks = [
    # address, frequency
    ("MDPS12", 50),
    ("MDPS11", 100),
    ("TCS15", 10),
    ("TCS13", 50),
    ("CLU11", 50),
    ("ESP12", 100),
    ("CGW1", 10),
    ("CGW4", 5),
    ("WHL_SPD11", 50),
    ("SAS11", 100)
  ]
  if CP.carFingerprint not in FEATURES["non_scc"]:
    signals += [
      ("MainMode_ACC", "SCC11", 0),
      ("VSetDis", "SCC11", 0),
      ("SCCInfoDisplay", "SCC11", 0),
      ("ACC_ObjDist", "SCC11", 0),
      ("ACCMode", "SCC12", 1),
    ]
    checks += [
      ("SCC11", 50),
      ("SCC12", 50),
    ]
  else:
    signals += [
      ("CRUISE_LAMP_M", "EMS16", 0),
      ("CF_Lvr_CruiseSet", "LVR12", 0),
    ]
  if CP.carFingerprint in FEATURES["use_cluster_gears"]:
    signals += [
      ("CF_Clu_InhibitD", "CLU15", 0),
      ("CF_Clu_InhibitP", "CLU15", 0),
      ("CF_Clu_InhibitN", "CLU15", 0),
      ("CF_Clu_InhibitR", "CLU15", 0),
    ]
  elif CP.carFingerprint in FEATURES["use_tcu_gears"]:
    signals += [
      ("CUR_GR", "TCU12",0),
    ]
  elif CP.carFingerprint in FEATURES["use_new_gears"]:
    signals += [
      ("Gear_Signal", "NEW11", 0),
    ]
  else:
    signals += [
      ("CF_Lvr_Gear","LVR12",0),
    ]
  return CANParser(DBC[CP.carFingerprint]['pt'], signals, checks, 0)


def get_camera_parser(CP):

  signals = [
    # sig_name, sig_address, default
    ("CF_Lkas_LdwsSysState", "LKAS11", 0),
    ("CF_Lkas_SysWarning", "LKAS11", 0),
    ("CF_Lkas_LdwsLHWarning", "LKAS11", 0),
    ("CF_Lkas_LdwsRHWarning", "LKAS11", 0),
    ("CF_Lkas_HbaLamp", "LKAS11", 0),
    ("CF_Lkas_FcwBasReq", "LKAS11", 0),
    ("CF_Lkas_ToiFlt", "LKAS11", 0),
    ("CF_Lkas_HbaSysState", "LKAS11", 0),
    ("CF_Lkas_FcwOpt", "LKAS11", 0),
    ("CF_Lkas_HbaOpt", "LKAS11", 0),
    ("CF_Lkas_FcwSysState", "LKAS11", 0),
    ("CF_Lkas_FcwCollisionWarning", "LKAS11", 0),
    ("CF_Lkas_FusionState", "LKAS11", 0),
    ("CF_Lkas_FcwOpt_USM", "LKAS11", 0),
    ("CF_Lkas_LdwsOpt_USM", "LKAS11", 0)
  ]

  checks = []

  return CANParser(DBC[CP.carFingerprint]['pt'], signals, checks, 2)


class CarState():
  def __init__(self, CP):

    self.CP = CP

    # initialize can parser
    self.car_fingerprint = CP.carFingerprint

    # vEgo kalman filter
    dt = 0.01
    # Q = np.matrix([[10.0, 0.0], [0.0, 100.0]])
    # R = 1e3
    self.v_ego_kf = KF1D(x0=[[0.0], [0.0]],
                         A=[[1.0, dt], [0.0, 1.0]],
                         C=[1.0, 0.0],
                         K=[[0.12287673], [0.29666309]])
    self.v_ego = 0.0
    self.left_blinker_on = 0
    self.left_blinker_flash = 0
    self.right_blinker_on = 0
    self.right_blinker_flash = 0
    self.no_radar = self.CP.carFingerprint in FEATURES["non_scc"]

  def update(self, cp, cp_cam):
    # update prevs, update must run once per Loop
    self.prev_left_blinker_on = self.left_blinker_on
    self.prev_right_blinker_on = self.right_blinker_on

    self.door_all_closed = True
    self.seatbelt = cp.vl["CGW1"]['CF_Gway_DrvSeatBeltSw']

    self.brake_pressed = cp.vl["TCS13"]['DriverBraking']
    self.esp_disabled = cp.vl["TCS15"]['ESC_Off_Step']
    self.park_brake = cp.vl["CGW1"]['CF_Gway_ParkBrakeSw']

    self.main_on = (cp.vl["SCC11"]["MainMode_ACC"] != 0) if not self.no_radar else \
                                            cp.vl['EMS16']['CRUISE_LAMP_M']
    self.acc_active = (cp.vl["SCC12"]['ACCMode'] != 0) if not self.no_radar else \
                                      (cp.vl["LVR12"]['CF_Lvr_CruiseSet'] != 0)
    self.pcm_acc_status = int(self.acc_active)

    # calc best v_ego estimate, by averaging two opposite corners
    self.v_wheel_fl = cp.vl["WHL_SPD11"]['WHL_SPD_FL'] * CV.KPH_TO_MS
    self.v_wheel_fr = cp.vl["WHL_SPD11"]['WHL_SPD_FR'] * CV.KPH_TO_MS
    self.v_wheel_rl = cp.vl["WHL_SPD11"]['WHL_SPD_RL'] * CV.KPH_TO_MS
    self.v_wheel_rr = cp.vl["WHL_SPD11"]['WHL_SPD_RR'] * CV.KPH_TO_MS
    v_wheel = (self.v_wheel_fl + self.v_wheel_fr + self.v_wheel_rl + self.v_wheel_rr) / 4.

    self.low_speed_lockout = v_wheel < 1.0

    # Kalman filter, even though Hyundai raw wheel speed is heaviliy filtered by default
    if abs(v_wheel - self.v_ego) > 2.0:  # Prevent large accelerations when car starts at non zero speed
      self.v_ego_kf.x = [[v_wheel], [0.0]]

    self.v_ego_raw = v_wheel
    v_ego_x = self.v_ego_kf.update(v_wheel)
    self.v_ego = float(v_ego_x[0])
    self.a_ego = float(v_ego_x[1])
    is_set_speed_in_mph = int(cp.vl["CLU11"]["CF_Clu_SPEED_UNIT"])
    speed_conv = CV.MPH_TO_MS if is_set_speed_in_mph else CV.KPH_TO_MS
    self.cruise_set_speed = cp.vl["SCC11"]['VSetDis'] * speed_conv if not self.no_radar else \
                                         (cp.vl["LVR12"]["CF_Lvr_CruiseSet"] * speed_conv)
    self.standstill = not v_wheel > 0.1

    self.angle_steers = cp.vl["SAS11"]['SAS_Angle']
    self.angle_steers_rate = cp.vl["SAS11"]['SAS_Speed']
    self.yaw_rate = cp.vl["ESP12"]['YAW_RATE']
    self.left_blinker_on = cp.vl["CGW1"]['CF_Gway_TSigLHSw']
    self.left_blinker_flash = cp.vl["CGW1"]['CF_Gway_TurnSigLh']
    self.right_blinker_on = cp.vl["CGW1"]['CF_Gway_TSigRHSw']
    self.right_blinker_flash = cp.vl["CGW1"]['CF_Gway_TurnSigRh']
    self.steer_override = abs(cp.vl["MDPS11"]['CR_Mdps_DrvTq']) > STEER_THRESHOLD
    self.steer_state = cp.vl["MDPS12"]['CF_Mdps_ToiActive'] #0 NOT ACTIVE, 1 ACTIVE
    self.steer_error = cp.vl["MDPS12"]['CF_Mdps_ToiUnavail']
    self.brake_error = 0
    self.steer_torque_driver = cp.vl["MDPS11"]['CR_Mdps_DrvTq']
    self.steer_torque_motor = cp.vl["MDPS12"]['CR_Mdps_OutTq']
    self.stopped = cp.vl["SCC11"]['SCCInfoDisplay'] == 4. if not self.no_radar else False
    self.lead_distance = cp.vl["SCC11"]['ACC_ObjDist'] if not self.no_radar else 0

    self.user_brake = 0

    self.brake_pressed = cp.vl["TCS13"]['DriverBraking']
    self.brake_lights = bool(self.brake_pressed)
    if (cp.vl["TCS13"]["DriverOverride"] == 0 and cp.vl["TCS13"]['ACC_REQ'] == 1):
      self.pedal_gas = 0
    else:
      self.pedal_gas = cp.vl["EMS12"]['TPS']
    self.car_gas = cp.vl["EMS12"]['TPS']

    # Gear Selection via Cluster - For those Kia/Hyundai which are not fully discovered, we can use the Cluster Indicator for Gear Selection, as this seems to be standard over all cars, but is not the preferred method.
    if self.car_fingerprint in FEATURES["use_cluster_gears"]:
      if cp.vl["CLU15"]["CF_Clu_InhibitD"] == 1:
        self.gear_shifter = GearShifter.drive
      elif cp.vl["CLU15"]["CF_Clu_InhibitN"] == 1:
        self.gear_shifter = GearShifter.neutral
      elif cp.vl["CLU15"]["CF_Clu_InhibitP"] == 1:
        self.gear_shifter = GearShifter.park
      elif cp.vl["CLU15"]["CF_Clu_InhibitR"] == 1:
        self.gear_shifter = GearShifter.reverse
      else:
        self.gear_shifter = GearShifter.unknown
    # Gear Selecton via TCU12
    elif self.car_fingerprint in FEATURES["use_tcu_gears"]:
      gear = cp.vl["TCU12"]["CUR_GR"]
      if gear == 0:
        self.gear_shifter = GearShifter.park
      elif gear == 14:
        self.gear_shifter = GearShifter.reverse
      elif gear > 0 and gear < 9:    # unaware of anything over 8 currently
        self.gear_shifter = GearShifter.drive
      else:
        self.gear_shifter = GearShifter.unknown
    # Gear Selecton - This is only compatible with optima hybrid 2017
    elif self.car_fingerprint in FEATURES["use_new_gears"]:
      gear = cp.vl["NEW11"]["Gear_Signal"]
      if gear == 5:
        self.gear_shifter = GearShifter.drive
      elif gear == 6:
        self.gear_shifter = GearShifter.neutral
      elif gear == 0:
        self.gear_shifter = GearShifter.park
      elif gear == 7:
        self.gear_shifter = GearShifter.reverse
      else:
        self.gear_shifter = GearShifter.unknown
    # Gear Selecton - This is not compatible with all Kia/Hyundai's, But is the best way for those it is compatible with
    else:
      gear = cp.vl["LVR12"]["CF_Lvr_Gear"]
      if gear == 5:
        self.gear_shifter = GearShifter.drive
      elif gear == 6:
        self.gear_shifter = GearShifter.neutral
      elif gear == 0:
        self.gear_shifter = GearShifter.park
      elif gear == 7:
        self.gear_shifter = GearShifter.reverse
      else:
        self.gear_shifter = GearShifter.unknown


    # save the entire LKAS11 and CLU11
    self.lkas11 = cp_cam.vl["LKAS11"]
    self.clu11 = cp.vl["CLU11"]
