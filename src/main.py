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
# 	Project:     VEX IQ Starter Project
# 	Author:      VEX Programmer
# 	Description: Basic Autonomous Movement
#
# ----------------------------------------------------------------------------

def autonomous_routine():
    brain.screen.print("Autonomous Starting")
    brain.screen.new_line()
    # Set movement speeds
    drivetrain.set_drive_velocity(50, PERCENT)
    drivetrain.set_turn_velocity(30, PERCENT)

    # 1. Move forward 4 feet
    drivetrain.drive_for(FORWARD, 48, INCHES)

    # 2. Lift the arm motor 90 degrees
    arm_motor.spin_for(REVERSE, 90, DEGREES)

    # 3. Turn right 90 degrees
    drivetrain.turn_for(RIGHT, 90, DEGREES,wait=True)

    # 4. Drive forward another 100 millimeters
    drivetrain.drive_for(FORWARD, 30, INCHES)

    drivetrain.turn_for(RIGHT, 90, DEGREES, wait=True)


    brain.screen.print("Routine Finished!")

# Run the project
autonomous_routine()
