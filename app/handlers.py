from aiogram import F,Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import app.keyboard as kb
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1gdcb9L88ZrU2Yd6iP-LoiL1n8Ukkd6lluTlc8KFvHPw"
SAMPLE_RANGE_NAME = "Пивная заправка!A1:J"

router = Router()

def validate(date_text):
        #date_text_iso = datetime.datetime.strptime(date_text,"%d/%m/%Y").strftime("%d.%m.%Y")
        #print(date_text_iso,date_text)
        try:
          if date_text != datetime.datetime.strptime(date_text, "%d.%m.%Y").strftime('%d.%m.%Y'):
            raise ValueError
          return True
        except ValueError:
          return False

def getDate(date):
  allData = getData()
  for dateItem in range(2, len(allData)):
    print("@@@@"+str(allData[dateItem][0]),"@@@@@",date)
    if allData[dateItem][0] == date:
      return allData[dateItem]
  return "Дата не найдена =("

def getData():
  data = ""
  
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    #if not values:
    #  data = ("No data found.")
    #  return data
    return values
  except HttpError as err:
      print(err)

def outputData():
  allData = getData()
  data = ""
  try:
    for row in range(2, len(allData)):
      # Print columns A and E, which correspond to indices 0 and 4.
        #if row[0] == None or row[1] == None or row[2] == None or row[3] == None or row[4] == None or row[5] == None or row[6] == None or row[7] == None or row[8] == None or row[9] == None:
        print(row)
        for i in range(10):
          try:
            data += allData[0][i]+ ": " + allData[row][i] + ", "
            print(allData[row][i]+"\n" )
          except IndexError:
            data += "|Нет данных"

        print(allData)
        print("************",data)
        #data += (f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}")
        data += "\n\n"
    return data
  except IndexError:
    return "Пусто"

def outputDate(datetext):
  if getDate(datetext) != "Дата не найдена =(":
    allDate= getDate(datetext)
    allData = getData()
    data = ""
    for i in range(10):
      # Print columns A and E, which correspond to indices 0 and 4.
        #if row[0] == None or row[1] == None or row[2] == None or row[3] == None or row[4] == None or row[5] == None or row[6] == None or row[7] == None or row[8] == None or row[9] == None:
        try:
          data += allData[0][i] + ": " + allDate[i] + "\n"
          print(allDate[i])
        except IndexError:
          data += "|Нет данных"
        print(allDate)
        #data += (f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}")
    return data
  else:
    return getDate(datetext)



@router.message(CommandStart())
async def cmd_start(message: Message):
    print(message.text)
    await message.answer("Привет!",reply_markup=kb.main)

@router.message(F.text== "Все данные")
async def cmd_getData(message: Message):
    print(message.text)
    gettedData = outputData()
    if len(gettedData) > 4095:
       for x in range(0, len(gettedData), 4095):
          await message.answer(gettedData[x:x+4095])
    else:
       await message.answer(gettedData)

@router.message(F.text)
async def cmd_getDate(message: Message):
    print(message.text)
    if validate(message.text):
       await message.answer(outputDate(message.text))

