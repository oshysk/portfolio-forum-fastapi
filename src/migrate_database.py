from sqlalchemy import create_engine

from src.models import forum as forum_model
from src.models import comment as comment_model

# DB_URL = "mysql+pymysql://root@0.0.0.0:3306/forum?charset=utf8"
DB_URL = "mysql+pymysql://root@database:3306/forum?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    forum_model.Base.metadata.drop_all(bind=engine)
    forum_model.Base.metadata.create_all(bind=engine)
    comment_model.Base.metadata.drop_all(bind=engine)
    comment_model.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()
