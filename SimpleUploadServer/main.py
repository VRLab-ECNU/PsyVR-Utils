import json
import os
from time import time

from fastapi import FastAPI, File, UploadFile, Request

app = FastAPI()


@app.get("/check_status")
async def root():
    return {"message": "OK"}


@app.post("/upload_record")
async def upload_record(request: Request, file: UploadFile = File(...)):
    if not file.content_type in ['text/csv', 'application/vnd.ms-excel', 'text/txt', 'text/plain', 'text/json']:
        return {'code': -1, 'message': 'File type not supported'}

    if not os.path.exists('./data_received/'):
        os.mkdir('./data_received/')

    try:
        uploaded_data = await file.read()
        timestamp = int(time())
        with open(f'./data_received/{timestamp}_{file.filename}', 'wb') as f:
            f.write(uploaded_data)

        with open(f'./data_received/{timestamp}_{file.filename.split(".")[0]}.json', 'w', encoding='utf-8') as f:
            upload_info = {
                "timestamp": timestamp,
                "filename": f"{timestamp}_{file.filename}",
                "host": request.client.host
            }
            f.write(json.dumps(upload_info, indent=4, ensure_ascii=False))

        return {'code': 0, 'message': 'File uploaded successfully'}

    except Exception as e:
        return {'code': -1, 'message': 'Exception occurred during file upload', 'exception': str(e)}


# RequestUrl: /test RequestType: PUT Usage: Receive a file upload from client directly instead of using multipart/form-data
@app.put("/upload_record")
async def test(request: Request):
    try:
        body = await request.body()
        timestamp = int(time())
        with open(f'./data_received/{timestamp}_test.csv', 'wb') as f:
            f.write(body)

        with open(f'./data_received/{timestamp}_test.json', 'w', encoding='utf-8') as f:
            upload_info = {
                "timestamp": timestamp,
                "filename": f"{timestamp}_test.csv",
                "host": request.client.host
            }
            f.write(json.dumps(upload_info, indent=4, ensure_ascii=False))

        return {'code': 0, 'message': 'File uploaded successfully'}
    except Exception as e:
        return {'code': -1, 'message': 'Exception occurred during file upload', 'exception': str(e)}
