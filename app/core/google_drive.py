import os
import io
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from fastapi import HTTPException

load_dotenv()

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

SCOPES = ["https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE,
    scopes=SCOPES,
)

drive_service = build("drive", "v3", credentials=credentials)


# ==============================
# CREATE SUBFOLDER IF NOT EXISTS
# ==============================
def get_or_create_subfolder(folder_name: str):

    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false"

    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [GOOGLE_DRIVE_FOLDER_ID],
    }

    folder = drive_service.files().create(
        body=folder_metadata,
        fields="id"
    ).execute()

    return folder.get("id")


# ==============================
# UPLOAD FILE TO SUBFOLDER
# ==============================
async def upload_file_to_drive(file, filename: str, subfolder: str):

    try:
        subfolder_id = get_or_create_subfolder(subfolder)

        file_bytes = await file.read()

        file_metadata = {
            "name": filename,
            "parents": [subfolder_id],
        }

        media = MediaIoBaseUpload(
            io.BytesIO(file_bytes),
            mimetype=file.content_type,
            resumable=True,
        )

        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id",
        ).execute()

        file_id = uploaded_file.get("id")

        drive_service.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"},
        ).execute()

        return f"https://drive.google.com/uc?id={file_id}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Drive Upload Failed: {str(e)}")