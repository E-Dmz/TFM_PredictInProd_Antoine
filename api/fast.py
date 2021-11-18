from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from datetime import datetime
import pytz
import joblib

from TaxiFareModel.gcp import download_object
from TaxiFareModel.params import PATH_TO_LOCAL_MODEL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/predict")
def predict_fare(pickup_datetime,
                 pickup_longitude,
                 pickup_latitude,
                 dropoff_longitude,
                 dropoff_latitude,
                 passenger_count):

    X_pred = pd.DataFrame(columns=["key",
                               "pickup_datetime",
                               "pickup_longitude",
                               "pickup_latitude",
                               "dropoff_longitude",
                               "dropoff_latitude",
                               "passenger_count"])

    X_pred["key"] = ["1"]
    X_pred["pickup_datetime"] = [str(convert_datetime(pickup_datetime))]
    X_pred["pickup_longitude"] = [float(pickup_longitude)]
    X_pred["pickup_latitude"] = [float(pickup_latitude)]
    X_pred["dropoff_longitude"] = [float(dropoff_longitude)]
    X_pred["dropoff_latitude"] = [float(dropoff_latitude)]
    X_pred["passenger_count"] = [int(passenger_count)]

    if False:
        download_object("model.joblib", PATH_TO_LOCAL_MODEL)
    model = joblib.load(PATH_TO_LOCAL_MODEL)

    y_pred = round(model.predict(X_pred)[0],2)
    return {"prediction": y_pred
        # "pickup_datetime": pickup_datetime,
        # "pickup_longitude": pickup_longitude,
        # "pickup_latitude": pickup_latitude,
        # "dropoff_longitude": dropoff_longitude,
        # "dropoff_latitude": dropoff_latitude,
        # "passenger_count": passenger_count
    }


def convert_datetime(pickup_datetime):
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)

    return utc_pickup_datetime
