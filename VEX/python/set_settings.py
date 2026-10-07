#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
flap_motor = Motor(Ports.PORT4, False)
arm_motor = Motor(Ports.PORT10, False)
left_drive_smart = Motor(Ports.PORT1, 0.5, False)
right_drive_smart = Motor(Ports.PORT6, 0.5, True)
# increasing torque
left_drive_smart.set_max_torque(100, PERCENT)
right_drive_smart.set_max_torque(100, PERCENT)#
drivetrain_gyro = Gyro(Ports.PORT7)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_gyro, 200)
controller = Controller()



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
            # to control arm_motor
            if controller.buttonLUp.pressing():
                arm_motor.spin(REVERSE)
                controller_left_shoulder_control_motors_stopped = False
            elif controller.buttonLDown.pressing():
                arm_motor.spin(FORWARD)
                controller_left_shoulder_control_motors_stopped = False
            elif not controller_left_shoulder_control_motors_stopped:
                arm_motor.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_left_shoulder_control_motors_stopped = True
            # check the buttonRUp/buttonRDown status
            # to control flap_motor
            if controller.buttonRUp.pressing():
                flap_motor.spin(REVERSE)
                controller_right_shoulder_control_motors_stopped = False
            elif controller.buttonRDown.pressing():
                flap_motor.spin(FORWARD)
                controller_right_shoulder_control_motors_stopped = False
            elif not controller_right_shoulder_control_motors_stopped:
                flap_motor.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

#endregion VEXcode Generated Robot Configuration
# #region VEXcode Generated Robot Configuration
# from vex import *
# import urandom
# import math

# # Brain should be defined by default
# brain=Brain()

# # Robot configuration code
# brain_inertial = Inertial()



# # generating and setting random seed
# def initializeRandomSeed():
#     wait(100, MSEC)
#     xaxis = brain_inertial.acceleration(XAXIS) * 1000
#     yaxis = brain_inertial.acceleration(YAXIS) * 1000
#     zaxis = brain_inertial.acceleration(ZAXIS) * 1000
#     systemTime = brain.timer.system() * 100
#     urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
# # Initialize random seed 
# initializeRandomSeed()

# #endregion VEXcode Generated Robot Configuration
# from vex import *

# def run_arm_motors():
#     drivetrain.set_drive_velocity(100, PERCENT)
#     motor_10.set_velocity(100, PERCENT)
#     motor_10.set_max_torque(100, PERCENT)
#     motor_10.spin(FORWARD)

#     drivetrain.drive(FORWARD)
    

# def run_flaps():
#     flap_motor.set_velocity(100, PERCENT)
#     flap_motor.set_max_torque(100, PERCENT)
#     flap_motor.spin(FORWARD)


# def stop_motors():
#     drivetrain.stop()
#     motor_10.stop()
#     motor_4.stop()

# controller.buttonL3.pressed(run_motors)
# # controller.buttonEUp.released(stop_motors)
# controller.buttonRUp.pressed(run_faps);

################# New Program ###################

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

# ---------------------------------------------------------------------
# Robot Configuration
# If you already added the flap motor and controller in VEXcode IQ's
# "Devices" window, VEXcode will auto-generate lines like these at the
# top of your project -- delete this block and use the names it gave
# you instead (just make sure the rest of the code below refers to the
# same name). Otherwise, change PORT1 to whichever Smart Port the flap
# motor is actually plugged into.
# ---------------------------------------------------------------------
flap_motor = Motor(Ports.PORT4, GearSetting.RATIO_1_1, False)
arm_motor = Motor(Ports.PORT10, GearSetting.RATIO_1_1, False)
controller = Controller()

def set_up_arm_speed():
    # Sets the arm motor's speed to 100% and starts spinning it reverse.
    arm_motor.set_velocity(100, PERCENT)
    arm_motor.set_stopping(HOLD)
    arm_motor.spin(REVERSE)

def set_down_arm_speed():
    # Sets the arm motor's speed to 100% and starts spinning it reverse.
    arm_motor.set_velocity(100, PERCENT)
    arm_motor.set_stopping(HOLD)
    arm_motor.spin(FORWARD)

def set_up_flap_speed():
    # Sets the flap motor's speed to 100% and starts it spinning forward.
    flap_motor.set_velocity(100, PERCENT)
    flap_motor.spin(REVERSE)

def set_down_flap_speed():
    # Sets the flap motor's speed to 100% and starts it spinning forward.
    flap_motor.set_velocity(100, PERCENT)
    flap_motor.spin(FORWARD)

# Runs set_flap_speed() every time the F-Up button is pressed.
# Swap buttonFUp for any of these if you want a different button:
# buttonEUp, buttonEDown, buttonFUp, buttonFDown,
# buttonLUp, buttonLDown, buttonRUp, buttonRDown, buttonL3, buttonR3
controller.buttonRUp.pressed(set_up_flap_speed)
controller.buttonRDown.pressed(set_down_flap_speed)
controller.buttonLUp.pressed(set_up_arm_speed)
controller.buttonLDown.pressed(set_down_arm_speed)

# Keep the project alive so the button callback keeps listening
while True:
    wait(20, MSEC)