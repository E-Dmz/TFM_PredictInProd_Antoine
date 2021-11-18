FROM python:3.8.6-buster

COPY api /api
COPY TaxiFareModel /TaxiFareModel
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt

RUN pip install Cython --install-option="--no-cython-compile" && pip install -r requirements.txt

CMD uvicorn api.fast:predict_fare --host 0.0.0.0 --port $PORT
