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
        self.zero_threshold = 0
        self.max_rotation = 1000000

    def set_zero_position(self):
        self.can_interface.GripperCtrl(0,1,0x00, 0xAE)

    def disable(self):
        # Disable the gripper
        self.can_interface.GripperCtrl(0, 1000, 0x02, 0)

    def read_status(self):
        # Read the status of the gripper
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state
    
    def rotate(self, rotation: int, torque: int = 1000):
        assert torque > 0, "Positive torque expected !!!"
        assert rotation >= 0, "Non-negative rotation expected !!!"
        self.can_interface.GripperCtrl(rotation, torque, 0x01, 0)

    def get_rotation(self):
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state.grippers_angle
    
    def get_torque(self):
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state.grippers_effort
    
    def back_to_zero_position(self, torque: int = 1000):
        self.rotate(0, torque)
        time.sleep(1)

    def test_and_set_zero_threshold(self):
        self.back_to_zero_position()
        self.zero_threshold = self.get_rotation()


        
            

            
    

    

