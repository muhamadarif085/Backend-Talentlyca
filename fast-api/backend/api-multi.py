import os
import dotenv
import tempfile
from upload import upload_blob_from_memory, set_data, fire_database
from pydantic import BaseModel
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import sys
import shutil
import concurrent
import https_redirect
import asyncio
# Add path to system path


# Database variable
cred = "/home/c2284f2446/talentlyca-db-firebase-adminsdk-1wsye-9e3ecafefb.json"
database_url = 'https://talentlyca-db-default-rtdb.asia-southeast1.firebasedatabase.app/'
database_path = '/'

# # Database object
ref = fire_database(cred, database_url, database_path)

app = FastAPI()
config = dotenv.dotenv_values()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(HTTPSRedirectMiddleware)

sys.path.append(config["ML_DIR_PATH"])
from prediction.main import predict as pd

queue = []


class Upload(BaseModel):
    uid: str
    file: UploadFile


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>API Machine Learning Talentlyca</title>
        </head>
        <body>
            <h1>API Machine Learning Talentlyca</h1>
        </body>
    </html>
    """


def inference(uid, contents, destination_blob_name):

    # Create segmentation folder
    os.makedirs("./segmentation-{}".format(uid), exist_ok=True)

    # Save to local
    with open(destination_blob_name, "wb") as fp:
        fp.write(contents)

        # Predict
        result = pd(destination_blob_name, uid)

    # Cleaning up
    os.remove(destination_blob_name)
    shutil.rmtree("./segmentation-{}".format(uid))

    inferences_ref = ref.child("inferences/{}".format(uid))
    inferences_ref.set({
        "filename": result["File"],
        "skills": list(result["Skills"]),
        "experiences": list(result["Exp"])
    })

    print("{} Inference done".format(uid))


@app.post("/api/v1/predict")
async def predict(uid: str, file: UploadFile, background_tasks: BackgroundTasks):
    contents = file.file.read()
    destination_blob_name = file.filename

    # Save to GCS
    upload_blob_from_memory(contents, destination_blob_name)

    background_tasks.add_task(inference, uid, contents, destination_blob_name)

    return {"status": "success", "uid": uid, "filename": destination_blob_name, "message": "Upload success! Prediction is in progress"}


def main():
    uvicorn.run("api-multi:app", host="0.0.0.0",
                port=int(config["PORT"]), reload=False, workers=4,
                ssl_keyfile='/home/c2284f2446/private.key',
                ssl_certfile='/home/c2284f2446/certificate.crt')


if __name__ == "__main__":
    sys.exit(main())
