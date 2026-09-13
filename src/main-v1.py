#region VEXcode Generated Robot Configuration
from vex import *
import random

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT1, 1.0, False)
right_drive_smart = Motor(Ports.PORT6, 1.0, True)
drivetrain_gyro = Gyro(Ports.PORT7)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gyro,
                         wheelTravel=200, trackWidth=175, units=MM, externalGearRatio=2)

arm_motor = Motor(Ports.PORT10, GearSetting.RATIO_1_1, False)
flap_motor = Motor(Ports.PORT4, GearSetting.RATIO_1_1, False)


# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    random.seed(int(xaxis + yaxis + zaxis + systemTime))


# Initialize random seed
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Gyro
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Gyro")
    drivetrain_gyro.calibrate(GyroCalibrationType.NORMAL)
    while drivetrain_gyro.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()

#endregion VEXcode Generated Robot Configuration
# ----------------------------------------------------------------------------
#
# 	Project:     VEX IQ Level Up - Autonomous Coding Skills
# 	Author:      VEX Programmer
# 	Description: Scores the Preload Bean Bag on the L1 Goal (3 pts) well within
# 	             the 1:00 Autonomous Period. Robot starts sharing a wall with
# 	             the red Pyramid Goal per <RSC3c>, holding a yellow Preload
# 	             per <SG5> (yellow counts on any Goal color, <SC4d>).
#
# ----------------------------------------------------------------------------

# Tune these on the real field/robot - exact distances/angles depend on your
# mechanism and how the Robot sits against the Pyramid Goal wall.
ARM_LIFT_DEG = 135       # raises the carrier so the Preload clears the L1 lip
FLAP_RELEASE_DEG = 45    # spins the outtake flap to tip the Preload onto L1
RETREAT_IN = 6           # backs off so the Bean Bag isn't touching the Robot
                         # at Match end, which <SC4a> requires to count as scored

def autonomous_routine():
    brain.screen.print("Skills: L1 Score")
    brain.screen.new_line()

    drivetrain.set_drive_velocity(40, PERCENT)
    drivetrain.set_turn_velocity(30, PERCENT)
    arm_motor.set_velocity(50, PERCENT)
    flap_motor.set_velocity(50, PERCENT)

    # Robot already starts flush against the Pyramid Goal wall (<RSC3c>) -
    # no seating drive needed; driving forward here would just ram the wall.

    # Deposit the Preload onto the L1 surface (3 points, <SC4>)
    arm_motor.spin_for(REVERSE, ARM_LIFT_DEG, DEGREES)
    flap_motor.spin_for(FORWARD, FLAP_RELEASE_DEG, DEGREES)

    # Clear away so the scored Bean Bag isn't contacting the Robot, and stow
    drivetrain.drive_for(REVERSE, RETREAT_IN, INCHES)
    arm_motor.spin_for(FORWARD, ARM_LIFT_DEG, DEGREES)
    drivetrain.stop()

    brain.screen.print("L1 scored")


# ----------------------------------------------------------------------------
# Alternate routine: drive-out-and-place sequence from the Red starting
# position. Tune these on the real field/robot.
# ----------------------------------------------------------------------------
STEP1_DRIVE_IN = 6        # move forward off the Red starting position
TURN_DEG = 90             # rotate to face the goal
ARM_LIFT_1_DEG = 135      # first arm lift
STEP2_DRIVE_IN = 22       # drive toward the goal
ARM_LIFT_2_DEG = 145      # second arm lift (relative, on top of the first)
STEP3_DRIVE_IN = 8.5      # final approach distance
RELEASE_FLAP_DEG = 45     # spins the outtake flap to release the Bean Bag

def autonomous_routine_v2():
    brain.screen.print("Skills: Drive & Place")
    brain.screen.new_line()

    drivetrain.set_drive_velocity(40, PERCENT)
    drivetrain.set_turn_velocity(30, PERCENT)
    arm_motor.set_velocity(50, PERCENT)
    flap_motor.set_velocity(50, PERCENT)

    # Move forward 6 inches from the Red starting position
    drivetrain.drive_for(FORWARD, STEP1_DRIVE_IN, INCHES)

    # Lift arm up 135 degrees
    arm_motor.spin_for(REVERSE, ARM_LIFT_1_DEG, DEGREES)

    # Rotate 90 degrees (change RIGHT to LEFT if it turns the wrong way)
    drivetrain.turn_for(RIGHT, TURN_DEG, DEGREES)

    # Move forward 22 inches
    drivetrain.drive_for(FORWARD, STEP2_DRIVE_IN, INCHES)

    # Lift arm up another 145 degrees
    arm_motor.spin_for(REVERSE, ARM_LIFT_2_DEG, DEGREES)

    # Move forward 8.5 inches
    drivetrain.drive_for(FORWARD, STEP3_DRIVE_IN, INCHES)

    # Release the Preload Bean Bag
    flap_motor.spin_for(FORWARD, RELEASE_FLAP_DEG, DEGREES)
    drivetrain.stop()

    brain.screen.print("Beanbag released")


# Run the project
autonomous_routine_v2()
