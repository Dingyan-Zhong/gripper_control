import time
from piper_sdk import *

class PiperGripper:
    """
    A class to control the parallel jaw gripper originally for Piper Robot by AgileX Robotics.

    The gripper is controled through CAN.

    Length of fingers: 7cm
    Maximal width between fingers: 7cm by product manual, 7.15cm by in-house measurement

    """
    def __init__(self, 
                 can_name: str = "can0", 
                 judge_flag: bool = True, 
                 can_auto_init: bool = True, 
                 motor_id: int = 7,
                 max_width: int = 70000,
                 finger_len: int = 70000,
                 zero_threshold: int = 500,
                 torque_threshold: int = 100,):
        self.motor_id = motor_id
        self.can_interface = C_PiperInterface(
                can_name=can_name, 
                judge_flag=judge_flag, 
                can_auto_init=can_auto_init
            )
        
        self.can_interface.ConnectPort()
        self.zero_threshold = zero_threshold
        self.torque_threshold = torque_threshold
        self.max_width = max_width
        self.finger_len = finger_len

    def set_zero_position(self, force_set: bool = False):
        # [dzhong-2025/04/27]: 
        # It seems to me the zero position has been set by the manufacturer.
        # I was trying to implement a function to set the current position as the zero position.
        # But simply sending (CURRENT_WIDTH, 1000, 0x00, 0xAE) doesn't seem to work.
        self.can_interface.GripperCtrl(0,1000,0x00,0xAE)

    def disable(self):
        self.can_interface.GripperCtrl(0,1000,0x02,0)

    def read_status(self):
        msg = self.can_interface.GetArmGripperMsgs()
        return msg.gripper_state
    
    def move_to(self, width: int, torque: int = 1000):
        """
        Move fingers to the desired location with the given torque.

        width: Distance between two fingers, measured in 10^(-6) meters.
        torque: Absolute value of the torque, measured in 10^(-3) N/m.

        """

        assert torque >= 100, "A torque at least 100 is expected. Recommended >= 1000."
        assert width >= 0, "Non-negative width expected !!!"
        self.can_interface.GripperCtrl(width, torque, 0x01, 0)

    def move_to_widest(self, torque: int = 1000):
        self.move_to(self.max_width, torque=torque)

    def back_to_zero_position(self, torque: int = 1000):
        self.move_to(0, torque)
        # Leave enough time for fingers to move
        time.sleep(1)

    def test_and_set_threshold(self):
        """
        IMPORTANT: Make sure nothing is in between the two fingers when calling this function.

        Read the distance between the fingers when they are at the zero position.
        This distance is usually a small positive integer, useful for measuring the location of the fingers.

        Also record the torque, as it's usually a small number around 100, useful when checking the grasping status.
        """
        self.back_to_zero_position()

        # The manufacturer declares that the max error can be 0.5 mm.
        # [dzhong-2025/04/17] 
        # The error can be larger than 0.5 mm sometimes,
        # especially when the width is large, e.g., close to the max width
        self.zero_threshold = max(500, self.get_width())
        self.torque_threshold = self.get_torque()
    
    def get_width(self):
        """Distance between two fingers, measured in 10^(-6) meters."""
        msg = self.can_interface.GetArmGripperMsgs()
        return abs(msg.gripper_state.grippers_angle)
    
    def get_torque(self):
        """Absolute value of the torque, measured in 10^(-3) N/m"""
        msg = self.can_interface.GetArmGripperMsgs()
        return abs(msg.gripper_state.grippers_effort)
    
    def check_grasp(self, target_torque: int, torque_threshold: int = 0):
        """
        Check that the current torque has been close enough to the target.

        Optional: Override the threshold temporarily by passing a new one.
        """
        threshold = torque_threshold if torque_threshold > 0 else self.torque_threshold
        for repeat in range(10):
            if abs(self.get_torque()-target_torque)>threshold:
                return False
        return True

    
    
    


        
            

            
    

    

