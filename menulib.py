# s3lib.py
# Python 3
"""
Jonathan Mainhart
SDEV400
26 August 2021

Menu functions for homework1.py

"""
import os
import random
import s3lib


PROMPT = 'Please make a selection >>> '
INVALID_SELECTION = 'Please make a valid selection.\n'
CONTINUE = '... press enter to continue ...'
WARNING = ('WARNING: Deleting files and buckets is permanent and cannot ' +
           'be undone! Proceed at your own risk.')


def bucket_list():
    """
    Prints a list of available buckets. Requires s3lib.list_buckets()
    return: True if the list has elements, otherwise False
    """
    # get list of target buckets
    buckets_list = s3lib.list_buckets()
    # verify we have a place to put the file
    if buckets_list:
        print(buckets_list)
        return True
    else:
        # if not, alert user to create one
        print('There are no buckets available')
        input(CONTINUE)
        return False


def file_list(bucket_name):
    """
    Prints a list of available files in the specified bucket.
    Requires s3lib.list_bucket_objects
    :param bucket_name: string
    :return: True if the list has elements, otherwise False
    """
    files = s3lib.list_bucket_objects(bucket_name)
        # verify there are files to delete
    if files:
        print(files)
        return True
    else:
        # nothing to delete - go home
        print(f'{bucket_name} is empty')
        input(CONTINUE)
        return False


def create_new_bucket():
    """
    Menu allows user to create a new bucket with pre-set naming convention
    """

    # generate DNS-legal name consisting of jonathan mainhart and a random 6-digit suffix
    bucket_name = (f'jonathan-mainhart-{random.randrange(100000, 999999)}')
    # make sure no other randomly generated bucket has the same name
    if not s3lib.s3_bucket_exists(bucket_name):
        # bucket does not already exist
        print(f'Creating new bucket with name {bucket_name}')

        # make the bucket
        if s3lib.create_bucket(bucket_name):
            print('Successfully created new bucket\n ')
            input(CONTINUE)
        else:
            # the bucket was not created
            print('Something went wrong. Check the log.')
            input(CONTINUE)
    else:
        # buy a lottery ticket
        print(f'{bucket_name} already exists. Try again.')
        print(f'Maybe you should buy a lottery ticket. Your lucky number is {bucket_name[-6:]}')
        input(CONTINUE)


def upload_local_file():
    """
    Menu allows user to upload a local file to an S3 bucket
    """
    # get user input
    filename = input('Enter the file name: ').strip()
    # check local file exists
    if s3lib.local_file_exists(filename):
        # list available buckets - return if none
        if not bucket_list():
            return
        target_bucket = input('Enter target bucket name: ').strip()
        # check bucket exists - really checking for fat fingers
        if s3lib.s3_bucket_exists(target_bucket):
            # upload file
            if s3lib.upload_file(filename, target_bucket):
                # success - let the user know
                print(f'{filename} successfully uploaded to {target_bucket}\n')
                input(CONTINUE)
            else:
                # failure
                print('File failed to upload\n')
                input(CONTINUE)
        else:
            # bucket does not exist or something else went wrong
            print(f'{target_bucket} not found. Check the name and try again.\n')
            input(CONTINUE)

    else:
        # user entered a filename or path incorrectly
        print(f'{filename} not found. Check the name and try again.\n')
        input(CONTINUE)


def delete_file():
    """
    Menu allows a user to delete a file from an S3 bucket. returns to main menu if
    no buckets or files are available.
    """
    # warn user
    print(WARNING)
    # list available buckets - return if none
    if not bucket_list():
        return
    target_bucket = input('Enter bucket name: ').strip()
    # check bucket exists
    if s3lib.s3_bucket_exists(target_bucket):
        # list files - return if none
        if not file_list(target_bucket):
            return
        target_file = input('Enter file name: ').strip()
        # check object exists
        if target_file in s3lib.list_bucket_objects(target_bucket):
            # delete object
            if s3lib.delete_object(target_bucket, target_file):
                # success
                print(f'{target_file} was successfully deleted from {target_bucket}')
                input(CONTINUE)
            else:
                # failed
                print(f'{target_file} was not deleted from {target_bucket}. ' +
                      'Check your input and try again.')
                input(CONTINUE)
        else:
            # object doesn't exist
            print(f'{target_file} not found. Check the name and try again.\n')
            input(CONTINUE)
    else:
        # bucket doesn't exist
        print(f'{target_bucket} does not exist. Check the name and try again.\n')
        input(CONTINUE)


def copy_file():
    """
    Menu allows a user to copy a file from one bucket to another. Returns to main menu if
    there are no buckets or files available.
    """
    # list available buckets - return if none
    if not bucket_list():
        return
    # get source and target buckets
    source_bucket = input('Enter source bucket name: ').strip()
    destination_bucket = input('Enter destination bucket name: ').strip()
    # check source bucket and destination buckets exist
    if s3lib.s3_bucket_exists(source_bucket) and s3lib.s3_bucket_exists(destination_bucket):
        # list files in source - return if none
        if not file_list(source_bucket):
            return
        # get the file to copy
        source_file = input('Enter source file name: ').strip()
        # check object exists
        if source_file in s3lib.list_bucket_objects(source_bucket):
            # copy the file
            if s3lib.copy_object(source_bucket, source_file, destination_bucket, None):
                # success
                print(f'{source_file} successfully copied from' +
                      f'{source_bucket} to {destination_bucket}')
                input(CONTINUE)
            else:
                # Failed to copy
                print(f'Something went wrong while trying to copy ' +
                      f'{source_file} from {source_bucket} to {destination_bucket}.')
                input(CONTINUE)
        else:
            # object not found
            print(f'{source_file} not found. Check the name and try again.\n')
            input(CONTINUE)
    else:
        # bucket not found
        print(f'{source_bucket} or {destination_bucket} does not exist. '+
              'Check the name and try again.\n')
        input(CONTINUE)


def download_file():
    """
    Menu allows a user to download a file from an S3 bucket.
    returns to main menu if no buckets or files exist.
    """
    # list buckets - return if none
    if not bucket_list():
        return
    source_bucket = input('Enter bucket name: ').strip()
    # check bucket exists
    if s3lib.s3_bucket_exists(source_bucket):
        # list files - return if none
        if not file_list(source_bucket):
            return
        source_object = input('Enter file name: ').strip()
        # check object exists
        if source_object in s3lib.list_bucket_objects(source_bucket):
            # download file
            if s3lib.download_file(source_bucket, source_object, None):
                print(f'{source_object} successfully downloaded')
                input(CONTINUE)
            else:
                # the file was not downloaded for one reason or another
                print(f'Something went wrong and {source_object} was not downloaded\n')
                input(CONTINUE)
        else:
            # the object went missing or was not entered correctly
            print(f'{source_object} does not exist in {source_bucket}.'+
                  ' Check the name and try again.\n')
            input(CONTINUE)
    else:
        # the bucket went missing or was not entered correctly
        print(f'{source_bucket} does not exist. Check the name and try again.\n')
        input(CONTINUE)


def delete_bucket():
    """
    Menu allows a user to delete a bucket. Alerts user to objects
    in the bucket if any and allows user to abort.
    """
    # list buckets - return if none
    if not bucket_list():
        return
    # define the target
    target_bucket = input('Enter bucket name: ').strip()
    # check bucket exists
    if s3lib.s3_bucket_exists(target_bucket):

        # check bucket for objects
        bucket_objects = s3lib.list_bucket_objects(target_bucket)
        # warn user of impending destruction
        if bucket_objects:
            print(f'{target_bucket} contains the following items:')
            print(bucket_objects)
            print(WARNING + '\nBy continuing you agree that you understand that' +
                  ' all files will be deleted forever.')
            # user must explicitly confirm deletion with a 'y'
            if input('Continue? y/n: ')[:1] is not 'y':
                print('Aborting process')
                input(CONTINUE)
                return

        # empty the bucket if objects exist
        if bucket_objects:
            print(f'deleting the following:\n{bucket_objects}')
            s3lib.delete_objects(target_bucket, bucket_objects)
            print('done')

        # delete bucket
        # user must confirm deletion of the bucket one last time
        if input(f'{target_bucket} is about to be deleted. Continue? y/n: ')[:1] is not 'y':
            print('Aborting process')
            input(CONTINUE)
            return
        print(f'deleting bucket {target_bucket}')

        if s3lib.delete_bucket(target_bucket):
            # successfully deleted the bucket
            print('done')
            input(CONTINUE)
        else:
            # something prevented the bucket from being deleted
            print(f'{target_bucket} could not be deleted.')
            input(CONTINUE)
    else:
        # the bucket went missing or was entered incorrectly
        print(f'{target_bucket} does not exists. Check the name and try again.')
        input(CONTINUE)


def main_menu():
    """
    Displays main menu to user
    """

    user_selection = 0

    while user_selection == 0:
        os.system('clear')
        print('Main Menu\n'
              '1. Create new S3 bucket\n'
              '2. Upload file to existing bucket\n'
              '3. Delete file from existing bucket\n'
              '4. Copy a file from bucket-to-bucket\n'
              '5. Download a file from a bucket\n'
              '6. Delete a bucket\n'
              '7. Exit\n')

        # get user selection
        user_selection = input(PROMPT).strip()
        # discard invalid selections
        if user_selection not in ('1', '2', '3', '4', '5', '6', '7'):
            print(f'{INVALID_SELECTION}')
            input(CONTINUE)
            user_selection = 0

        # user create new bucket
        if user_selection == '1':
            create_new_bucket()
            user_selection = 0
        # user upload file
        if user_selection == '2':
            upload_local_file()
            user_selection = 0
        # user delete file
        if user_selection == '3':
            delete_file()
            user_selection = 0
        # user copy file B2B
        if user_selection == '4':
            copy_file()
            user_selection = 0
        # user download a file
        if user_selection == '5':
            download_file()
            user_selection = 0
        # user delete a bucket
        if user_selection == '6':
            delete_bucket()
            user_selection = 0
        # user exit
        if user_selection == '7':
            return
