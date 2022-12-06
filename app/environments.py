import os

STAGE = os.getenv('STAGE', 'dev')
DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://root:root@localhost:5432/dev')
