## The Requirements:
1. A Linux (virtual) machine with sudo authorization. WSL 2 won't work. 
2. Connection to the gripper: CAN wire between the motor and the CAN-toUSB adapter, whose is connected to the server/pc's USB 2.0 port (USB 3.0 & type-c not tested).
3. Python with required libraries: python-can, piper_sdk.
4. can-utils and ethtool, can be installed by sudo apt install can-utils ethtool.


## How to Run:
1. Ensure that the motor has been connected to the server.
2. Look for the adapter on the server. It will usually be recongnized as a /dev/ttyACMx device. To find out the value of x, one may run sudo dmesg | grep tty in the terminal to check the connected USB devices. If the adapter is the only device connected, it's usually /dev/ttyACM0.
3. Set up the CAN interface and name it as can0. 
In terminal: sudo slcand -o -c -s8 /dev/ttyACM0 can0
Set bitrate: sudo ip link set can0 type can bitrate 1000000
Then enable it: sudo ip link set can0 up
Veriify connection: candump can0
You should now be able to see tons of messages flood into your terminal. Ctrl + C to stop it.

Finally, set txqueuelen to ensure smooth connection: sudo ifconfig can0 txqueuelen 1000

4. The motor's control precision may fall after we use it for some time. When this happens, we may need to manually set the zero position, following the guide in manual_set_zero.py.

## Interesting Facts:
1. The data the motor sends are not always precise. When fingers are at the zero position physically, its position and torque read from the motor are not 0.
2. When fingers move to a position with a given torque, the torque read from the motor will not change much until the fingers contact something, when the torque jumps to the target value.
3. If one calls the move_to function twice, the motor will execute the second one immediately the command is sent, no matter whether the previous one has been finished.
4. In the code of piper_sdk, it seems that we should control the fingers by setting the rotation angle. But it turns out that we should set the width between fingers.


