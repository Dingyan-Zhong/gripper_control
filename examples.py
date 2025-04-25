from gripper import Gripper
import time

if __name__ == "__main__":
    gripper = Gripper()

    #gripper.enable()
    gripper.back_to_zero_position()
    time.sleep(1.5)
    gripper.set_zero_position()
    time.sleep(0.5)
    #print("rotation:", gripper.get_rotation())
    #print("torque:", gripper.get_torque())

    time.sleep(0.5)

    
    gripper.rotate(70000, 1000)
        
    
    time.sleep(15)
    gripper.rotate(0, 1000)
    time.sleep(1)
    
    print("rotation after rotating:", gripper.get_rotation())
    print("torque after rotating:", gripper.get_torque())

    time.sleep(20)

    #gripper.back_to_zero_position()

    

    gripper.disable()