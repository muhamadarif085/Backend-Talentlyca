from google.cloud import storage
import os
import sys

GOOGLE_APPLICATION_CREDENTIALS = 'team-02-bangkit-76f340a873e2.json'

storage_client = storage.Client()

def downloadFile(source):
    source_blob_name = source
    destination_file_name = source
    bucket_name='team02'
    bucket = storage_client.bucket('team02')
    blob = bucket.blob(source_blob_name)
    # print (blob)
    blob.download_to_filename(destination_file_name)

    return destination_file_name

    # print(
    #     "Downloaded storage object {} from bucket {} to local file {}.".format(
    #     source_blob_name, bucket_name, destination_file_name
    #     )
    # )
