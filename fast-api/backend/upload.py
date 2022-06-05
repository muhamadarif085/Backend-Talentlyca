from google.cloud import storage
import firebase_admin
from firebase_admin import db
import json
import os
import dotenv

# Get environment variables
config = dotenv.dotenv_values()


def upload_blob_from_memory(contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client.from_service_account_json(config["CREDENTIAL_PATH"])
    bucket = storage_client.bucket('team02')
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents)

    print(
        f"{destination_blob_name} uploaded to team02."
    )


def fire_database(certificate, databaseURL, pathData):
    # Add firebase credential
    cred = firebase_admin.credentials.Certificate(certificate)
    if not firebase_admin._apps:
        # Create the database app
        firebase_admin.initialize_app(cred, {
            "databaseURL": databaseURL
        })
    # Set the reference path for database
    ref = db.reference(pathData)

    return ref

def set_data(ref, data):
    # Set data to database
    cond = False

    if not cond:
        try:
            ref.set(data)
            print("Upload Successful")
            cond = True
        except:
            print("Upload Failed")
            cond = False
