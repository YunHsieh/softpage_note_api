import os

STAGE = os.getenv('STAGE', 'dev')
DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://root:root@localhost:5432/dev')
SECRET_KEY = os.getenv('SECRET_KEY', '^*-x(@n*zyi4^+vv+zg316p&g7=z_8s#_a$u!hz)=(5da+s=@8')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60000')

CLIENT_HOST = os.getenv('CLIENT_HOST', 'http://localhost:3000')

GOOGLE_OAUTH_URL = os.getenv('GOOGLE_OAUTH_URL')
GOOGLE_TOKEN_URL = os.getenv('GOOGLE_TOKEN_URL')
GOOGLE_OAUTH_SCOPE = os.getenv('GOOGLE_OAUTH_SCOPE')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
