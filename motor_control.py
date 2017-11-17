# pypot dynamixel library
import pypot.dynamixel as pd

# get ports
# USB2AX will be the first result
ports = pd.get_available_ports()

# connect to port
motors = pd.DxlIO(ports[0], 1000000)
# get list of motors
print 'Scanning for motors...'
# motor_list = motors.scan()
# print 'Found motors: ' + str(motor_list)

def move_wheel(cmd_dict):
    motors.set_moving_speed(cmd_dict)
