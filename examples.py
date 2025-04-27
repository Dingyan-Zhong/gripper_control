from gripper import PiperGripper
import time

if __name__ == "__main__":
    # Steps in this example:
    # initialize and connect to the gripper ->
    # move fingers to the zero position ->
    # test the precision of gripper control ->
    # move fingers to the widest position ->
    # move fingers closer to grasp an object ->
    # check grasp status through torque comparison ->
    # print the status of the gripper ->
    # disable the gripper

    gripper = PiperGripper()

    gripper.back_to_zero_position()
    gripper.test_and_set_threshold()

    torque = 1000

    gripper.move_to_widest(torque=torque)

    # Put something between the fingers during this time
    time.sleep(20)

    # A move_to function call will interrupt the previous move_to call immediately.
    # Get_width and get_torque will not interrupt move_to calls.
    # It takes roughly 0.5s for fingers to move to the widest distance from the zero position, 
    # when torque is 1000.

    gripper.move_to(20000, torque=torque)      
    time.sleep(0.5)

    for i in range(10):
        if gripper.check_grasp(target_torque=torque):
            print(f"round {i} check success!!!")
            time.sleep(0.002)
  
    print("width after grasping:", gripper.get_width())
    print("torque after grasping:", gripper.get_torque())

    # The disable function will stop the motor immediately,
    # even if the fingers are moving
    gripper.disable()