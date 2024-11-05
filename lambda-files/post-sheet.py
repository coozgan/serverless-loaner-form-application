import json
import gspread
from datetime import datetime
import boto3
import os, time
from google.oauth2.service_account import Credentials
from botocore.exceptions import ClientError

os.environ['TZ'] = 'Asia/Singapore'
time.tzset()

# Global variables for reuse across invocations
secret_cache = None
gspread_client = None
sheet = None

client = boto3.client('ses', region_name='ap-southeast-1')

def lambda_handler(event, context):
  global secret_cache, gspread_client, sheet
  if not sheet:
        if not secret_cache:
            secret_cache = get_secret()
        
        if not gspread_client:
            scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_info(secret_cache, scopes=scopes)
            gspread_client = gspread.authorize(creds)
        
        wb = gspread_client.open_by_key("KEY_ID_OF_YOUR_GOOGLE_SPREADSHEET")
        sheet = wb.get_worksheet(1)
  
  assetID = event["AssetID"]
  name = event["Name"]
  email = event["Email"]
  reason = event["Reason"]
  deviceType = event["DeviceType"]
  row = sheet.find(assetID).row
  col = sheet.find(assetID).col
  email_col = col + 2
  name_col = col + 3
  time_col = col + 4
  # print time stamp
  current_time = datetime.now()
  email_currenttime = current_time.strftime("%A, %-d %B %Y at %I:%M%p")
  current_time = current_time.strftime("%m/%d/%Y %H:%M:%S")
  sheet.update_cell(row, name_col, name)
  # update email
  sheet.update_cell(row, email_col, email)
  # print(current_time)
  if "@" in email:
    sheet.update_cell(row, time_col, current_time)
  else:
    sheet.update_cell(row, time_col, "")
  # print("Data has been written")
  if "@" in event["Email"]:
    sendemailto_ics(assetID, deviceType, name,email, reason, email_currenttime)
  else:
    print("Device has been returned")
  return {"message": "Data has been written"}
    
def sendemailto_ics(assetID,deviceType, name, email, reason, time):
  response = boto3.client("ses")
  subject = "ICS Device Loaned by "+name.capitalize()
  body = f'''
  <html>
  <body>
    <p>This is an automatic email notification regarding the borrowed IT device</p>
    <ul>
        <li><strong>Timestamp:</strong> {time}</li>
        <li><strong>Name:</strong> {name.capitalize()}</li>
        <li><strong>Device:</strong> {deviceType.upper()}</li>
        <li><strong>Asset Tag:</strong> {assetID.upper()}</li>
        <li><strong>Reason:</strong> {reason}</li>
    </ul>
    <p style="color:red;"><strong>Please ensure to return the borrowed item by the end of the day.</strong></p>
    <p><em>You may reply to this email for any clarifications.</em></p>
    <p>Best regards,<br>IT Support Team</p>
    </body>
    </html>
  '''
  message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
  response = client.send_email(Source = 'IT Support Team <itsupport@example.com>',
  Destination = {"ToAddresses": [email],"CcAddresses":["myemail@example.com"]}, Message = message)

  return response

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