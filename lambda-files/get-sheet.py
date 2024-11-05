import json
import gspread
from google.oauth2.service_account import Credentials
import boto3
from botocore.exceptions import ClientError

# Global variables for reuse across invocations
secret_cache = None
gspread_client = None
worksheet = None

def lambda_handler(event, context):
    global secret_cache, gspread_client, worksheet
    
    if not worksheet:
        if not secret_cache:
            secret_cache = get_secret()
        
        if not gspread_client:
            scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_info(secret_cache, scopes=scopes)
            gspread_client = gspread.authorize(creds)
        
        wb = gspread_client.open_by_key("KEY_ID_OF_YOUR_GOOGLE_SPREADSHEET")
        worksheet = wb.get_worksheet(1)
    # getting all the records from my google spreadsheet
    return worksheet.get_all_records()

def get_secret():
    # This is your secrets information
    secret_name = "sheets-api/prod"
    region_name = "ap-southeast-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return json.loads(get_secret_value_response['SecretString'])
    except ClientError as e:
        print(f"Error retrieving secret: {e}")
        raise
