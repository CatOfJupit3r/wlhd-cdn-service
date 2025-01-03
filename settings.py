import os

import dotenv

dotenv.load_dotenv()

PORT = int(os.getenv('PORT', 8000))
HOST = os.getenv('HOST', '0.0.0.0')
SKIP_PREPARE = os.getenv('SKIP_PREPARE', 'false').lower() == 'true'

VALKEY_PORT = int(os.getenv('VALKEY_PORT', 6379))
VALKEY_HOST = os.getenv('VALKEY_HOST', 'localhost')
VALKEY_DB = int(os.getenv('VALKEY_DB', 0))
VALKEY_KEY_LIFETIME = int(os.getenv('VALKEY_KEY_LIFETIME', 3600))

ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')
if not ADMIN_TOKEN:
    print("Warning: ADMIN_TOKEN is not set. You will not be able to access admin API routes.")

COORDINATOR_TOKEN = os.getenv('COORDINATOR_TOKEN')
if not COORDINATOR_TOKEN:
    print("Warning: COORDINATOR_TOKEN is not set. You will not be able to access coordinator API routes.")

DLC_EXPECTED_STRUCTURE = {
    'manifest.json': 'file',
    'data': 'folder',
    'components': 'folder',
    'assets': 'folder',
    'functions': 'folder',
    'translations': 'folder',
    'LICENSE': 'file',
}
