import pickle
import io
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


from .settings import APPLICATION_DIR


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive']


class GoogleDrive:

    drive_name = ''
    credentials = ''


    def __init__(self, drive_name, credentials):
        self.drive_name = drive_name
        self.credentials = credentials
        
        self.service = self.__get_gdrive_service()


    def __get_gdrive_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(APPLICATION_DIR, f'sessions', self.drive_name + '.pickle')):
            with open(os.path.join(APPLICATION_DIR, f'sessions', self.drive_name + '.pickle'), 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(APPLICATION_DIR, f'sessions', self.drive_name + '.pickle'), 'wb') as token:
                pickle.dump(creds, token)
        # return Google Drive API service
        return build('drive', 'v3', credentials=creds)


    def list_files_in_folder(self, folder_id='root'):
        result = []
        query = f"'{folder_id}' in parents"
        results = self.service.files().list(q=query, pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size)").execute()
        items = results.get('files', [])

        for item in items:
            # logging.info(item)
            # print(u'{0} ({1})'.format(item['name'], item['id']))
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                result += self.list_files_in_folder(item['id'])
            else:
                try:
                    result.append({'name' : item['name'], 'id' : item['id'], 'size' : int(item['size'])})
                except:
                    pass


        page_token = results.get('nextPageToken', None)
        if page_token:
            self.list_files_in_folder(folder_id, page_token)
            
        return result


    def get_all_files(self):
        return self.list_files_in_folder()


    def download_file(self, file_id, file_name, save_directory='./files/'):
        if not os.path.isdir(save_directory): os.mkdir(save_directory)
        try:
            request = self.service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

            with open(os.path.join(save_directory, file_name), 'wb') as f:
                f.write(file.getvalue())

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

        return True
