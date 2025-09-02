import os

from dotenv import load_dotenv


load_dotenv()

USED_SETTINGS = os.getenv('USED_SETTINGS')

if USED_SETTINGS == 'dev':
    from .dev import *
elif USED_SETTINGS == 'prod':
    from .prod import *
else:
    raise ValueError('Choice "dev" or "prod" settings')