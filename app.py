from flask import request, jsonify, Flask
import json
import random
import string
import time
from datetime import datetime
from fastapi import Request, FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from db import DBManipulator
import pandas as pd
from utilities import InboundUtility
from fastapi.middleware.cors import CORSMiddleware
from utilities import  LoggerSettings
from flow import BranchAppFlow, ClientAppFlow, InvoiceAppFlow, StaticAppFlow, TypeAppFlow, UserAppFlow, static_app_flow, LicenseAppFlow, PlanAppFlow
f = open("utilities/conf/app_info.json")
json_data = json.load(f)
DBManipulator({"host":json_data["database_data"]["DATABASE_IP"],"port":json_data["database_data"]["DATABASE_PORT"]})
db = DBManipulator.create_session(json_data["database_data"]["DATABASE_NAME"])
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

char_set = string.ascii_uppercase + string.digits
request_id = ''.join(random.sample(char_set*12,12))

# Make file downloadable endpoint
@app.get("/api/download/{filename_path}")
async def download(filename_path):
    logger, _ = LoggerSettings.logger_setting()

    tick = time.time()
    logger.debug(f'[{request_id}] request recived with file_name =  {filename_path}')
    try:
        filename_path = filename_path.replace("+","/")
        logger.debug(f'[{request_id}] request converted to download file_name =  {filename_path}')
        path = "/" + filename_path
        logger.debug(f'[{request_id}] request is done on the /api/download with ({path})')
        tock = time.time()

        logger.debug(f'[{request_id}] request has been done , in time {round((tock - tick)*1000)} in msec!.')

        return FileResponse(path=path, media_type='text/*', filename=filename_path)
    except Exception as ex:
        status_code = 500
        logger.error(f'failed to send request as target not a valid option and for more info this is the exception  {str(ex)}')
        msg = f"failed to send request as target not a valid option and for more info this is the exception " + str(ex)
        return {
            "success":"False",
            "error":{
                "status_code": status_code,
                "title":"error seems that the request body have an issue",
                "details": msg
                }
        }


@app.post("/api/uploadfile/")
async def upload(request: Request, file: UploadFile = File(...)):
    logger, _ = LoggerSettings.logger_setting()
    tick = time.time()
    data =  {}
    logger.debug(f'[{request_id}] request recived ')
    logger.debug(f'[{request_id}] request recived with file name = {file.filename}')


    try:
        target = request.headers.get('target')
        action = request.headers.get('action')
        data["user_id"] = request.headers.get('user_id')
        data["validators"] = request.headers.get('validators')
        data["data"] = pd.read_csv(file.file)
        logger.debug(f'[{request_id}] request recived with target =  {target}')
        logger.debug(f'[{request_id}] request recived with action =  {action}')

        logger.debug(f'[{request_id}] request recived with user_id =  {data["user_id"]}')
        logger.debug(f'[{request_id}] request recived with validators =  {data["validators"]}')
        logger.debug(f'[{request_id}] request recived with data = \n {data["data"]}')


    except Exception as ex:
        status_code = 500
        logger.error(f'failed to send request as target not a valid option and for more info this is the exception {str(ex)}')
        msg = f"failed to send request as target not a valid option and for more info this is the exception " + str(ex)
        return {
            "success":"False",
            "error":{
                "status_code": status_code,
                "title":"error seems that the request body have an issue",
                "details": msg
                }
        }
    data_result = InboundUtility.request_handeler(target, data, action, request_id)
    if data_result == False:
            StatusCode = 403
    StatusMessage  = "Success"
    logger.debug(f'[{request_id}] request recived with StatusMessage = {StatusMessage}')

    StatusCode = 200
    data_result["status_code"] = StatusCode
    logger.debug(f'[{request_id}] request recived with StatusCode = {StatusCode}')
    logger.debug(f'[{request_id}] request has been done')

    tock = time.time()
    logger.debug(f'[{request_id}] request has been done , in time {round((tock - tick)*1000)} in msec!.')
    return data_result
# Main endpoint for inbound integration
@app.post('/api/inbound/', description="this api is used for ,,,,")
async def inbound_integration(request: Request):
    logger, _ = LoggerSettings.logger_setting()

    tick = time.time()
    data = await request.json()
    logger.debug(f'[{request_id}] request recived ')
    logger.debug(f'[{request_id}] request recived with json = \n {data}')
    target = data["target"]
    start = time.time()
    logger.debug(f'[{request_id}] request recived with Target = {target}')
    action = data["action"]
    logger.debug(f'[{request_id}] request recived with action =  {action}')

    try:
        del data["action"]
        del data["target"]
        logger.debug(f'[{request_id}] request is send to request handeler')

        data_result = InboundUtility.request_handeler(target, data, action, request_id)

    except Exception as ex:
        logger.error(f'[{request_id}] request is failed to send request as target not a valid option and for more info this is the exception {str(ex)}')
        status_code = 500
        msg = f"failed to send request as target not a valid option and for more info this is the exception" + str(ex)
        return {
            "success":"False",
            "error":{
                "status_code": status_code,
                "title":"error seems that the request body have an issue",
                "details": msg
                }
        }


    if data_result == False:
        StatusCode = 403
    StatusMessage  = "Success"
    logger.debug(f'[{request_id}] request recived with StatusMessage = {StatusMessage}')

    StatusCode = 200
    data_result["status_code"] = StatusCode
    logger.debug(f'[{request_id}] request recived with StatusCode = {StatusCode}')
    logger.debug(f'[{request_id}] request has been done')

    tock = time.time()
    logger.debug(f'[{request_id}] request has been done , in time {round((tock - tick)*1000)} in msec!.')
    return data_result

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}