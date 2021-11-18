import os

from google.cloud import storage
from termcolor import colored
from TaxiFareModel.params import BUCKET_NAME, MODEL_NAME, MODEL_VERSION


def storage_upload(rm=False):
    client = storage.Client().bucket(BUCKET_NAME)

    local_model_name = 'model.joblib'
    storage_location = f"models/{MODEL_NAME}/{MODEL_VERSION}/{local_model_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename('model.joblib')
    print(colored(f"=> model.joblib uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove('model.joblib')


def download_object(source_name, destination_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)

    source_blob = f"models/{MODEL_NAME}/{MODEL_VERSION}/{source_name}"
    blob = bucket.blob(source_blob)
    blob.download_to_filename(destination_name)
