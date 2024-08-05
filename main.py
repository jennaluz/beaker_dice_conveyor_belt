import sys

sys.path.append('../fanuc_ethernet_ip_drivers/src')
from robot_controller import robot

drive_path = '172.29.208.124'   # Robot Beaker

def main():
    crx10 = robot(drive_path, True)

if __name__ == '__main__':
    main()
