import time
from piper_sdk import *

class Gripper:
    def __init__(self, can_name: str = "can0", judge_flag: bool = True, can_auto_init: bool = True, motor_id: int = 7):
        self.motor_id = motor_id
        self.can_interface = C_PiperInterface(
                can_name=can_name, 
                judge_flag=judge_flag, 
                can_auto_init=can_auto_init
            )
        
        self.can_interface.ConnectPort()

    def enable(self):
        # Enable the gripper and set the gripper to the zero position
        self.can_interface.EnableArm(self.motor_id)
        self.rotate(0, 1000)

        # Wait for the gripper to reach the zero position
        time.sleep(1)

        # Verify gripper status
        status = self.read_status()
        rotation = status.grippers_angle
        if status.foc_status.driver_enable_status and abs(rotation)<10:
            print("Gripper enabled and zeroed")
            return True
        elif status.foc_status.driver_enable_status and abs(rotation)>10:
            print("Gripper enabled but zeroing failed")
            return False
        else:
            print("Gripper enable failed")
            return False

    def disable(self):
        # Disable the gripper
        self.can_interface.DisableArm(self.motor_id)
        self.can_interface.GripperCtrl(0, 1000, 0x02, 0)

    def read_status(self):
        # Read the status of the gripper
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state
    
    def rotate(self, rotation: int, torque: int):
        self.can_interface.GripperCtrl(rotation, torque, 0x01, 0)

    def get_rotation(self):
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state.grippers_angle
    
    def get_torque(self):
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state.grippers_effort
    
    def set_zero_position(self):
        # Ensure the gripper is enabled
        if self.read_status().foc_status.driver_enable_status:
            # Move to zero position
            self.can_interface.GripperCtrl(0, 1000, 0x00, 0)
            time.sleep(1)
            if self.read_status().grippers_angle < 10:
                print("Gripper zeroed")
                self.can_interface.GripperCtrl(0, 1000, 0x00, 0xAE)
            else:
                print("Gripper zeroing failed")
            

            
    

    

