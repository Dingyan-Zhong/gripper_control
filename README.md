## The Requirements:
1. A Linux (virtual) machine with sudo authorization. WSL 2 won't work. 
2. Python with required libraries: python-can, piper_sdk.
3. can-utils and ethtool, can be installed by sudo apt install can-utils ethtool.

## Interesting Facts:
1. The data the motor sends are not always precise. When fingers are at the zero position physically, its position and torque read from the motor are not 0.
2. When fingers move to a position with a given torque, the torque read from the motor will not change much until the fingers contact something, when the torque jumps to the target value.
3. If one calls the move_to function twice, the motor will execute the second one immediately the command is sent, no matter whether the previous one has been finished.
4. In the code of piper_sdk, it seems that we should control the fingers by setting the rotation angle. But it turns out that we should set the width between fingers.


