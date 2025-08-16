import os


APPLICATION_DIR = os.path.dirname(os.path.abspath(__file__))

CRON_ACTIVE = True # True - включить индексацию

# DRIVES = [ # список подключенных гугл дисков
#     {
#         'name'          : 'storage1',
#         'credentials'   : os.path.join(APPLICATION_DIR, 'credentials', 'credentials1.json'),
#     },
# ]


DRIVES = []

for credential in os.listdir(os.path.join(APPLICATION_DIR, 'credentials')):
    DRIVES.append({
        'name' : credential.rsplit('.', 1)[0],
        'credentials' : os.path.join(APPLICATION_DIR, 'credentials', credential),
    })


FILE_TYPES = ['pptx', 'pdf', 'docx'] # from ['pptx', 'docx', 'pdf', 'xlsx] # какие файлы будет индексировать и выводить в поисковой выдаче

CRON_LOCK_FILE = os.path.join(APPLICATION_DIR, 'cron.lock')

INDEX_DATABASE = os.path.join(APPLICATION_DIR, 'storage', 'index.sqlite3')