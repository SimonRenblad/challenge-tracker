from __future__ import print_function
import pickle
import os.path
import json
from pprint import pprint
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def analyze_data(values):
    titles = values[0]
    rows = np.array(values[1:])

    # get the columns
    dates = rows[:,0]
    new_dates = []

    # convert dates to date_time
    for date in dates:
        dt = np.datetime64(datetime.strptime(date, '%d/%m/%Y').date())
        new_dates.append(dt)

    dates = np.array(new_dates)
    bsup = rows[:,1].astype(np.int)
    scis = rows[:,2].astype(np.int)
    plt.plot_date(dates, bsup)
    plt.plot_date(dates, scis)
    plt.ylabel("seconds")
    plt.title("Challenge Tracker")
    plt.show()



def read_data(service, sheetId):
    result = service.spreadsheets().values().get( \
                spreadsheetId=sheetId, \
                range="A1:C30" \
             ).execute()
    return result['values']

def load_config():
    with open('config.json','r') as cfg:
        data = json.load(cfg)
    return data


def use_service(service):
    # load config file
    config = load_config()
    sheetId = config['sheetId']
    values = read_data(service, sheetId)
    analyze_data(values)


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    use_service(service)


if __name__ == '__main__':
    main()
