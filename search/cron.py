import pickle
import io
import os
import json
import fcntl
import sys

from .settings import FILE_TYPES
from .settings import DRIVES
from .settings import APPLICATION_DIR
from .settings import CRON_ACTIVE
from .settings import CRON_LOCK_FILE


from .gdrive import GoogleDrive
from .convert import Converter


from .indexing import Indexing


import logging

logging.basicConfig(level=logging.INFO, filename=os.path.join(APPLICATION_DIR, 'cron.log'), filemode="w")


import pprint
pp = pprint.PrettyPrinter(indent=4)


def my_scheduled_job():
    if not CRON_ACTIVE: return
    
    try:
        with open(CRON_LOCK_FILE, 'w') as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another instance of this script is already running.")
        sys.exit(1)

    indexing = Indexing()
    
    for gdrive in DRIVES:
        storage_path = os.path.join(APPLICATION_DIR, f'storage', gdrive["name"])
        indexing.set_storage(gdrive['name'])
        
        drive = GoogleDrive(gdrive['name'], gdrive['credentials'])
        files = []

        for f in drive.get_all_files():
            # logging.info(f)
            filename, id, fsize = f['name'], f['id'], f['size']
            if filename.split('.', 1)[-1].lower() in FILE_TYPES:
                files.append(f)
                
        pp.pprint(files)
        
        for f in files:
            fid = f['id']
            filename = fid + '.' + f['name'].rsplit('.', 1)[1] # fid.extension
            fsize = f['size']
            in_storage_filename = os.path.join(storage_path, filename) # {}/storage/storage1/fid.extension                
            
            if (not os.path.isfile(in_storage_filename) or os.path.getsize(in_storage_filename) != fsize) and not filename.startswith('file'):
                drive.download_file(fid, filename, save_directory=storage_path)
                indexing.index_file(in_storage_filename, f['name'])
                
                    
    indexing.close()
    os.remove(CRON_LOCK_FILE)

                    
                
                
        
                
                
            
        