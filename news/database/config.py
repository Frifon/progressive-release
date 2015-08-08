from sqlalchemy import create_engine
import os.path
engine = create_engine('sqlite:///' + os.path.abspath(__file__) + '/../vk.db')
