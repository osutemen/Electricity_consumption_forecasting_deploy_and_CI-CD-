from fastapi import FastAPI, Depends, Request
from models import DailyEnergyConsumption, CreateUpdateEnergy, HourlyEnergyConsumption,ElectricDriftInput
from database import engine, get_db, create_db_and_tables
from sqlalchemy.orm import Session
import pandas as pd
import joblib
from scipy.stats import ks_2samp



# Read models saved during train phase


estimator_loaded = joblib.load("saved_models/xgb.json")

#from mlflow.sklearn import load_model

# Tell where is the tracking server and artifact server
#os.environ['MLFLOW_TRACKING_URI'] = 'http://mlflow:5000/'
#os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://minio:9000/'

# Learn, decide and get model from mlflow model registry
#model_name = "ElectricModel"
#model_version = 1
#model = load_model(
#    model_uri=f"models:/{model_name}/{model_version}"
#)
app = FastAPI()

# Creates all the tables defined in models module
create_db_and_tables()


def create_features(df):
    df['Dayofyear'] = df.index.dayofyear
    df['Hour'] = df.index.hour
    df['Day'] = df.index.day
    df['Month'] = df.index.month
    df['Quarter'] = df.index.quarter
    df['Year'] = df.index.year
    return df


def make_days_prediction(model, request):
    # parse input from request
    Day = request["Date"]
    print(Day)
    # Make an input vector
    FEATURES = ['Dayofyear', 'Hour', 'Day', 'Quarter', 'Month', 'Year']

    start_date = pd.to_datetime(Day, format='%d.%m.%Y %H:%M')
    end_date = start_date + pd.DateOffset(days=4)
    future = pd.date_range(start=start_date, end=end_date, freq='D')
    future_df = pd.DataFrame(index=future)
    future_df_final = create_features(future_df)
    a = future_df_final[FEATURES]
    print(a)
    prediction = model.predict(a)
    print(prediction)
    prediction = ' '.join([str(elem) for elem in prediction])
    print(prediction)
    print(1)
    return prediction


def make_hour_prediction(model, request):
    # parse input from request
    Day = request["Date"]
    print(Day)
    # Make an input vector
    FEATURES = ['Dayofyear', 'Hour', 'Day', 'Quarter', 'Month', 'Year']
    start_date = pd.to_datetime(Day, format='%d.%m.%Y %H:%M')
    future = pd.date_range(start_date, periods=24, freq="1h")
    future_df = pd.DataFrame(index=future)
    future_df_final = create_features(future_df)
    a = future_df_final[FEATURES]
    prediction = model.predict(a)
    print(prediction)
    # prediction = prediction.tolist()
    prediction = ' '.join([str(elem) for elem in prediction])
    print(5)
    print(prediction)
    return prediction


def insert_energy1(request, prediction, client_ip, db):
    print(2)
    new_energy = DailyEnergyConsumption(
        Date=request["Date"],
        prediction=prediction,
        client_ip=client_ip
    )
    print(prediction)
    with db as session:
        session.add(new_energy)
        session.commit()
        session.refresh(new_energy)

    return new_energy


def insert_energy2(request, prediction, client_ip, db):
    print(2)
    new_energy = HourlyEnergyConsumption(
        Date=request["Date"],
        prediction=prediction,
        client_ip=client_ip
    )
    print(prediction)
    with db as session:
        session.add(new_energy)
        session.commit()
        session.refresh(new_energy)

    return new_energy

# Object agnostic drift detection function
def detect_drift(data1, data2):
    ks_result = ks_2samp(data1, data2)
    if ks_result.pvalue < 0.05:
        return "Drift exits"
    else:
        return "No drift"

# ENERGY Prediction endpoint for days
@app.post("/prediction/energy_prediction_for_5days")
async def predict_energy(request: CreateUpdateEnergy, fastapi_req: Request, db: Session = Depends(get_db)):
    prediction = make_days_prediction(estimator_loaded, request.dict())
    print(1, type(prediction))
    db_insert_record = insert_energy1(request=request.dict(), prediction=prediction,
                                      client_ip=fastapi_req.client.host,
                                      db=db)
    return {"prediction": prediction, "db_record": db_insert_record}


# ENERGY Prediction endpoint for hours
@app.post("/prediction/energy_prediction_for_24hours")
async def predict_energy(request: CreateUpdateEnergy, fastapi_req: Request, db: Session = Depends(get_db)):
    prediction = make_hour_prediction(estimator_loaded, request.dict())
    # prediction = prediction.tolist()[0]
    db_insert_record = insert_energy2(request=request.dict(), prediction=prediction,
                                      client_ip=fastapi_req.client.host,
                                      db=db)
    return {"prediction": prediction, "db_record": db_insert_record}

# Energy drift detection endpoint
@app.post("/drift/energy")
async def detect(request: ElectricDriftInput):
    # Select training data
    train_df = pd.read_sql("select * from electrictrain", engine)

    # Select predicted data last n days
    prediction_df = pd.read_sql(f"""SELECT * FROM electric
                                    ORDER BY id DESC
                                    LIMIT {request.last_n_values}""",
                                engine)

    electric_drift = detect_drift(train_df.Datetime, prediction_df.Date)

    return {"electric_drift": electric_drift}

@app.get("/")
async def root():
    return {"data": "Wellcome to MLOps API"}
