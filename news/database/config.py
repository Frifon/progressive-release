from sqlalchemy import create_engine
import os.path
engine = create_engine('mysql+pymysql://emil:very_secret_pass@149.5.2.221/vk', encoding='utf-8')
