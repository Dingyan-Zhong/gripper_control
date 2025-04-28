from gripper import PiperGripper
import time

if __name__ == "__main__":
    # Before execute this program,
    # press the two fingers against each other, 
    # ensure that they can't be closer anymore.

    gripper = PiperGripper()
    print("width:", gripper.get_width())
    print("torque:", gripper.get_torque())

    gripper.set_zero_position()
    time.sleep(0.5)
    print("width after zeroing:", gripper.get_width())
    print("torque after zeroing:", gripper.get_torque())

    time.sleep(1)

    gripper.disable()