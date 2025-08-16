import pickle
import io
import os
import argparse

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive']


parser = argparse.ArgumentParser(description='Конвертировать данные credentials в сессию')

# Добавляем аргументы
parser.add_argument('credentials', help='Имя credentials файла .json')
parser.add_argument('-O', '--output', '-o', '-output', help='Имя выходного файла с расширением pickle', required=True)

# Парсим аргументы
args = parser.parse_args()

credentials = args.credentials
if credentials.rsplit('.', 1) == 'json':
    credentials += '.json'
    
output = args.output
if output.rsplit('.', 1) == '.pickle':
    credentials += '.pickle'


if not os.path.isfile(credentials):
    print(f'*** Credentials file {credentials} not exists ***')
    exit(-1)


print(f'*** Credentials file: {credentials} ***')
print(f'*** Output file: {output} ***')

print('\n\n')

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

flow = InstalledAppFlow.from_client_secrets_file(
    credentials, SCOPES)
creds = flow.run_local_server(bind_addr='0.0.0.0', port=0, open_browser=False)
# Save the credentials for the next run
with open(output, 'wb') as token:
    pickle.dump(creds, token)

build('drive', 'v3', credentials=creds)


print(f'*** Saved to: {output} ***')