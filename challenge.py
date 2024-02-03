
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1BxeqyHIt4vG6hPt9t9h9Ha24QCvul8UQh6GK_4u3HrA"
SAMPLE_RANGE_NAME = "engenharia_de_software!A4:H27"


def calculate_situation(average, fouls, total_classes):
  if fouls > 0.25 * total_classes:
    return "Reprovado por faltas"
  elif average < 5:
    return "Reprovado por nota"
  elif 5 <= average < 7:
    return "Exame final"
  else:
    return "Aprovado"

def calculate_naf(average):
    naf = 10 - average
    return round(naf)

def main():

  creds = None

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

    situation_column = [


    ]

    naf_column =[

    ]

    total_classes = 60

    for i, line in enumerate(values, start=3):
      p1 = int(line[3])
      p2 = int(line[4])
      p3 = int(line[5])
      fouls = int(line[2])
      average = ((p1 + p2 + p3) / 3) / 10

      situation = calculate_situation(average, fouls, total_classes)

      if situation == "Exame final":
        naf = calculate_naf(average)
      else:
        naf = 0

      situation_column.append([situation])

      result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                     range="G4", valueInputOption="USER_ENTERED",
                                     body={'values': situation_column}).execute()
      naf_column.append([naf])

      result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                     range="h4", valueInputOption="USER_ENTERED",
                                     body={'values': naf_column}).execute()





  except HttpError as err:
    print(err)

if __name__ == "__main__":
  main()

