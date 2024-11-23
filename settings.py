import os

import dotenv

dotenv.load_dotenv()

PORT = int(os.getenv('PORT', 8000))
HOST = os.getenv('HOST', '0.0.0.0')
SKIP_PREPARE = os.getenv('SKIP_PREPARE', 'false').lower() == 'true'

ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')
if not ADMIN_TOKEN:
    print("Warning: ADMIN_TOKEN is not set. You will not be able to access the admin panel.")


DLC_EXPECTED_STRUCTURE = {
    'manifest.json': 'file',
    'data': 'folder',
    'components': 'folder',
    'assets': 'folder',
    'functions': 'folder',
    'translations': 'folder',
    'LICENSE': 'file',
}
