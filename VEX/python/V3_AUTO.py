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
flap_motor = Motor(Ports.PORT4, False)
arm_motor = Motor(Ports.PORT10, False)
controller = Controller()
touchLED_9 = Touchled(Ports.PORT9)



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



# define variables used for controlling motors based on controller inputs
controller_left_shoulder_control_motors_stopped = True
controller_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, controller_left_shoulder_control_motors_stopped, controller_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axisA + axisC
            # right = axisA - axisC
            drivetrain_left_side_speed = controller.axisA.position() + controller.axisC.position()
            drivetrain_right_side_speed = controller.axisA.position() - controller.axisC.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonLUp/buttonLDown status
            # to control flap_motor
            if controller.buttonLUp.pressing():
                flap_motor.spin(FORWARD)
                controller_left_shoulder_control_motors_stopped = False
            elif controller.buttonLDown.pressing():
                flap_motor.spin(REVERSE)
                controller_left_shoulder_control_motors_stopped = False
            elif not controller_left_shoulder_control_motors_stopped:
                flap_motor.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_left_shoulder_control_motors_stopped = True
            # check the buttonRUp/buttonRDown status
            # to control arm_motor
            if controller.buttonRUp.pressing():
                arm_motor.spin(FORWARD)
                controller_right_shoulder_control_motors_stopped = False
            elif controller.buttonRDown.pressing():
                arm_motor.spin(REVERSE)
                controller_right_shoulder_control_motors_stopped = False
            elif not controller_right_shoulder_control_motors_stopped:
                arm_motor.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

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

    drivetrain.set_drive_velocity(70, PERCENT)  # bumped from 40% - more push to climb the ramp
    drivetrain.set_turn_velocity(30, PERCENT)
    arm_motor.set_velocity(100, PERCENT)  # bumped from 50% - not enough torque to lift consistently
    flap_motor.set_velocity(100, PERCENT)  # bumped from 50% - not enough push to move the loaded flap

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
ARM_LIFT_1_DEG = 145      # first arm lift
STEP2_DRIVE_IN = 22       # drive toward the goal
ARM_LIFT_2_DEG = 145      # second arm lift (relative, on top of the first)
STEP3_DRIVE_IN = 8.5      # final approach distance
RELEASE_FLAP_DEG = 90     # spins the outtake flap to release the Bean Bag

def autonomous_routine_v2():
    brain.screen.print("Skills: Drive & Place")
    brain.screen.new_line()

    # touchLED_9.set_color(Color.BLUE) # touchLED_9 will turn blue

    drivetrain.set_drive_velocity(70, PERCENT)  # bumped from 40% - more push to climb the ramp
    drivetrain.set_turn_velocity(30, PERCENT)
    arm_motor.set_velocity(100, PERCENT)  # bumped from 50% - not enough torque to lift consistently
    flap_motor.set_velocity(100, PERCENT)  # bumped from 50% - not enough push to move the loaded flap

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
# touchLED_9.pressed(autonomous_routine_v2)
# touchLED_9.set_color(Color.BLACK)

