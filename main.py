import sys
import time

sys.path.append('../fanuc_ethernet_ip_drivers/src')
from robot_controller import robot

drive_path = '172.29.208.124'   # Robot Beaker

positions = [[618, -5, -50, 179, 1.5, 31],      # 0: Start
             [618, -5, -184, 179, 1.5, 31],     # 1: Start Die Grap
             [932, 645.5, -30, 179, 1.5, 31],   # 2: Conveyor Belt (CB) Start
             [932, 645.5, -181, 179, 1.5, 31],  # 3: CB Start Die Release
             [155, 649.5, -30, 179, 1.5, 31],   # 4: CB End
             [155, 649.5, -181, 179, 1.5, 31],  # 5: CB End Die Grap
             [618, -5, -174, 179, 1.5, 31]      # 6: End
            ]

def main():
    crx10 = robot(drive_path)

    crx10.schunk_gripper('open')
    crx10.write_cartesian_position(positions[0])

    while True:
        # Grap die from starting position
        crx10.write_cartesian_position(positions[1])
        crx10.schunk_gripper('close')
        crx10.write_cartesian_position(positions[0])

        # Release die onto the conveyor belt
        crx10.write_cartesian_position(positions[2])
        crx10.conveyor('forward')
        crx10.write_cartesian_position(positions[3])
        crx10.schunk_gripper('open')
        crx10.write_cartesian_position(positions[2])

        # Wait for die to reach the end of the conveyor belt
        crx10.set_speed(300)
        crx10.write_cartesian_position(positions[4])

        while not crx10.conveyor_proximity_sensor('right'):
            pass
        crx10.conveyor('stop')

        # Grap die from the end of the conveyor belt
        crx10.set_speed(200)
        crx10.write_cartesian_position(positions[5])
        crx10.schunk_gripper('close')
        crx10.write_cartesian_position(positions[4])

        # Move to the end position
        crx10.write_cartesian_position(positions[6])
        crx10.schunk_gripper('open')

        time.sleep(1)


if __name__ == '__main__':
    main()
