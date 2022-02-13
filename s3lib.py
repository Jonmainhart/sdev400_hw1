# s3lib.py
# Python 3
"""
Jonathan Mainhart
SDEV400
26 August 2021

Support functions for homework1.py

Much of this code is courtesy of the examples provided by Amazon AWS team. Code snippets
are annotated throughout this file. Any snippets used are in compliance with the Apache
License, Version 2.0 as stipulated in the original work. A copy of the license is
available at https://aws.amazon.com/apache2.0

"""
import logging
import boto3
from botocore.exceptions import ClientError


# look for bucket by name
def s3_bucket_exists(bucket_name):
    """Determine whether bucket_name exists and the user has permission to access it

    :param bucket_name: string
    :return: True if the referenced bucket_name exists, otherwise False

    Amazon (2019) bucket_exists.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """
    s3 = boto3.client('s3')
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.debug(e)
        return False
    return True


# create bucket
def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False

    Amazon (2019) create_bucket.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# Check local file exists
def local_file_exists(filename):
    """
    Check if local file exists.

    :param filename: String
    :return: True if file exists, else False
    """
    # check the path
    try:
        with open(filename):
            return True
    except FileNotFoundError as e:
        logging.error(e)
        return False


def list_buckets():
    """
    Lists available buckets.

    :return: list of available buckets

    Amazon (2019) s3-python-example-list-buckets.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # create s3 client
    s3 = boto3.client('s3')
    # call client and get list of buckets
    response = s3.list_buckets()
    # get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    # print list of bucket names
    return buckets


def list_bucket_objects(bucket_name):
    """
    List the objects in an Amazon S3 bucket_name

    :param bucket_name: string
    :return: List of bucket objects. If error, return None.

    Derived from:
    Amazon (2019) list_objects.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # create s3 client
    s3 = boto3.client('s3')
    try:
        objects = [obj['Key'] for obj in s3.list_objects_v2(Bucket=bucket_name)['Contents']]
    except ClientError as e:
        logging.error(e)
        return None
    except KeyError:
        # KeyError will raise when the bucket is empty - return None if this happens
        return None
    return objects


def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: bucket to upload to
    :param object: S3 object name. If none specified then same as file_name
    :return: True if file was uploaded, else False

    Amazon (2019) upload_file.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # use filename if s3 object not specified
    if object_name is None:
        object_name = file_name

    # upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_object(bucket_name, object_name):
    """
    Delete an object from an S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: True if the referenced object was deleted, otherwise False

    Amazon (2019) delete_object.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # delete the object
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_objects(bucket_name, object_names):
    """
    Delete multiple objects from an Amazon S3 bucket

    :param bucket_name: string
    :param object_names: list of strings
    :return: True if the referenced objects were deleted, otherwise False

    Amazon (2019) delete_objects.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # Convert list of object names to appropriate data format
    objlist = [{'Key': obj} for obj in object_names]

    # Delete the objects
    s3 = boto3.client('s3')
    try:
        s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objlist})
    except ClientError as e:
        logging.error(e)
        return False
    return True


def copy_object(src_bucket_name, src_object_name, dest_bucket_name, dest_object_name=None):
    """
    Copy an object from one S3 bucket to another S3 bucket

    :param src_bucket_name: string
    :param src_object_name: string
    :param dest_bucket_name: string. Must already exist
    :param dest_object_name: string. If destination bucket/object exists, it is
    overwritten. Default: src_object_name
    :return: True if object was copied, otherwise False

    Amazon (2019) copy_object.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # construct the source bucket/object parameter
    copy_source = {'Bucket': src_bucket_name, 'Key': src_object_name}

    if dest_object_name is None:
        dest_object_name = src_object_name

    # copy the object
    s3 = boto3.client('s3')
    try:
        s3.copy_object(CopySource=copy_source, Bucket=dest_bucket_name, Key=dest_object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(bucket_name, object_name, file_name=None):
    """
     Download a file from an S3 bucket

    :param bucket_name: S3 bucket to download from
    :param object_name: S3 object name to download.
    :param file_name: Name of file downloaded. If none specified then same as object_name
    :return: True if file was downloaded, else False
    """

     # use object_name if file_name not specified
    if file_name is None:
        file_name = object_name

    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket_name, object_name, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_bucket(bucket_name):
    """
    Deletes an empty S3 bucket.

    If the bucket is not empty, the operation fails.

    :param bucket_name: string
    :return: True if the target bucket is deleted, otherwise False

    Amazon (2019) delete_bucket.py
    Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
    """

    # delete the bucket
    s3 = boto3.client('s3')
    try:
        s3.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    