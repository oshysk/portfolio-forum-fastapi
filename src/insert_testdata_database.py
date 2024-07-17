from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import get_session

from src.models import forum as forum_model
from src.models import comment as comment_model

# DB_URL = "mysql+pymysql://root@0.0.0.0:3306/forum?charset=utf8"
DB_URL = "mysql+pymysql://root@database:3306/forum?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def insert_record():

    # セッションを作成
    session_maker = sessionmaker(engine)
    session = session_maker()

    # テストデータ１行目
    forum: forum_model.Forum = forum_model.Forum(
        title="初投稿",
        content="初投稿です。",
    )
    session.add(forum)

    # テストデータ２行目
    forum: forum_model.Forum = forum_model.Forum(
        title="最近の音楽について",
        content="最近の音楽は？",
    )
    session.add(forum)

    # テストデータ３行目
    forum: forum_model.Forum = forum_model.Forum(
        title="アフリカに行ったことはありますか？",
        content="アフリカに行ったことはありますか？",
    )
    session.add(forum)

    # テストデータ４行目
    forum: forum_model.Forum = forum_model.Forum(
        title="九州の魅力がどこにあるのか？",
        content="九州の魅力がどこにあるのか？",
    )
    session.add(forum)

    # テストデータ５行目
    forum: forum_model.Forum = forum_model.Forum(
        title="おすすめの本を教えてください。",
        content="おすすめの本は何ですか？",
    )
    session.add(forum)
    session.flush()
    comment = comment_model.Comment(
        forum_id=forum.forum_id,
        comment_id=1,
        comment="漫画が好きです。",
    )
    session.add(comment)
    comment = comment_model.Comment(
        forum_id=forum.forum_id,
        comment_id=2,
        comment="将来のためになる本です。",
    )
    session.add(comment)

    session.commit()
    session.close()
    return


if __name__ == "__main__":
    insert_record()
