from app.core.database import Base, engine
from .user import *
from .weixin import *

Base.metadata.create_all(bind=engine)
