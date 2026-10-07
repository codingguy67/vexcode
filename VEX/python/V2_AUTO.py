#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT1, 0.5, False)
right_drive_smart = Motor(Ports.PORT6, 0.5, True)
drivetrain_gyro = Gyro(Ports.PORT7)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gyro, 200)
arm_motor = Motor(Ports.PORT10, False)
flap_motor = Motor(Ports.PORT4, False)



# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
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
FLAP_RELEASE_DEG = 90    # spins the outtake flap to tip the Preload onto L1
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

    # Clear away so the scored Bean Bag isn't contacting the Robot, and stow.
    # NOTE: on this Robot, REVERSE drives toward the wall - FORWARD is what
    # actually backs away from it (confirmed on the field 2026-09-04).
    drivetrain.drive_for(FORWARD, RETREAT_IN, INCHES)
    arm_motor.spin_for(FORWARD, ARM_LIFT_DEG, DEGREES)
    drivetrain.stop()

    brain.screen.print("L1 scored")

# Run the project
autonomous_routine()
