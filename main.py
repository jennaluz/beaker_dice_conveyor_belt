# Import FANUC Drivers =========================================================
import sys
import time
sys.path.append('../fanuc/src')
from robot_controller import robot


# Variables ====================================================================
drive_path = '172.29.208.124'   # Beaker's IP address
position = [[470, -2.25, 150, 179, 1, 31.25],               # Position 0: Start
            [470, -2.25, -181, 179, 1, 31.25],              # Position 1: Start Pre-grab
            [-360, 626.25, 150, 179, -0.5, 120.75],         # Position 2: Conveyor Start
            [-360, 626.25, 20, 179, -0.5, 120.75],          # Position 3: Conveyor Pre-drop
            [-363.25, 824.75, 50, 179, -1.5, 123.25],       # Position 4: Conveyor Pre-grab
            [-363.25, 824.75, 16, 179, -1.5, 123.25],       # Position 5: Conveyor Grab
            [-363.25, 824.75, 150, 179, -1.5, 123.25],      # Position 6: Conveyor Post-grab
            [472.75, -3, 150, 179, 1, 31.25],               # Position 7: Table Post-conveyor
            [472.75, -3, -180.25, 179, 1, 31.25],           # Position 8: Table Pre-drop
            [472.75, -3, -117.5, 179, 1, 31.25],            # Position 9: Table Post-drop
            [474.25, 146, -117.5, 124.5, -56.25, -30.5],    # Position 10: Rotate Start
            [474.25, 34.75, -196.5, 124.5, -56.25, -30.5],  # Position 11: Rotate Pre-grab
            [474.25, 34.75, -135.25, 124.5, -56.25, -30.5], # Position 12: Ratate Post-grab
            [468, -18.25, -150, -172.5, 18.25, -59.5],      # Position 13: Rotate End
            [468, -18.25, -179, -172.5, 18.25, -59.5]    # Position 14: Rotate Pre-drop
            ]


# User-defined Functions =======================================================
def gripper(robot, motion):
    robot.schunk_gripper(motion)
    time.sleep(0.5)


def main():
    # Initialize Robot =========================================================
    crx10 = robot(drive_path)

    crx10.set_speed(200)

    gripper(crx10, 'open')
    crx10.write_cartesian_position(position[0])

    # Grab the dice
    crx10.write_cartesian_position(position[1])
    gripper(crx10, 'close')

    # Move to conveyor belt
    crx10.write_cartesian_position(position[0])
    crx10.write_cartesian_position(position[2])

    # Place the dice on conveyor belt
    crx10.write_cartesian_position(position[3])
    crx10.conveyor('forward')
    gripper(crx10, 'open')

    # Wait for the dice to reach the right proximity sensor
    crx10.write_cartesian_position(position[2])
    while crx10.conveyor_proximity_sensor('right') == 0:
        pass

    # Reverse the conveyor belt
    crx10.conveyor('stop')
    crx10.conveyor('reverse')

    # Wait for the dice to reach the left proximity sensor
    crx10.write_cartesian_position(position[4])
    while crx10.conveyor_proximity_sensor('left') == 0:
        pass

    crx10.conveyor('stop')

    # Pick up the dice from the conveyor belt
    crx10.write_cartesian_position(position[5])
    gripper(crx10, 'close')

    # Place the dice on the table
    crx10.write_cartesian_position(position[6])
    crx10.write_cartesian_position(position[7])
    crx10.write_cartesian_position(position[8])
    gripper(crx10, 'open')

    # Rotate the dice 90 degrees about the x-axis
    # Grab the dice
    crx10.write_cartesian_position(position[9])
    crx10.write_cartesian_position(position[10])
    crx10.write_cartesian_position(position[11])
    gripper(crx10, 'close')

    # Rotate the dice
    crx10.write_cartesian_position(position[12])
    crx10.write_cartesian_position(position[13])
    crx10.write_cartesian_position(position[14])
    gripper(crx10, 'open')

    # Return to start position
    crx10.write_cartesian_position(position[0])


# Call Main Function ===========================================================
if __name__ == '__main__':
    main()
