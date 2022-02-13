# homework1.py
# Python 3
"""
Jonathan Mainhart
SDEV400
26 August 2021

CLI menu-driven application which allows users to create AWS S3 buckets, upload objects
to the buckets, delete objects from buckets, copy objects from one bucket to another,
download objects from a bucket, and delete a bucket.
"""
import sys
import os
import logging
import datetime
import menulib


def main():
    """
    main() function of homework1 project.
    """
    # set up logging
    LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log/homework1.log'))
    logging.basicConfig(level=logging.INFO,
                        filename=LOG_FILE,
                        datefmt='%d-%b-%y %H:%M:%S',
                        format='%(levelname)s: %(asctime)s: %(message)s')
    logging.info('starting homework1')

    # present the main menu - all functions are accessed via the main and sub menus
    menulib.main_menu()

    # clear the screen then exit with current UTC date and time
    os.system('clear')
    logging.info('finishing homework1')
    # print exit message with date/time stamp as required
    print(f'Exiting at {datetime.datetime.utcnow().strftime("%d-%b-%y %H:%M:%S")}')
    sys.exit(0)


if __name__ == '__main__':
    main()
    