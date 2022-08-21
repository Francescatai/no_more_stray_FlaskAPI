from models.post import BoardModel, PostModel
from models.auth import UserModel
from exts import db
import random


def init_boards():
    board_names = ['領養新手', '健康照護', '愛寵教育', '線下小聚']
    for index, board_name in enumerate(board_names):
        board = BoardModel(name=board_name, priority=len(board_names) - index)
        db.session.add(board)
    db.session.commit()
    print("專區分類初始化成功")


def create_test_posts():
    boards = list(BoardModel.query.all())
    board_count = len(boards)
    authors = list(UserModel.query.all())
    authors_count = len(authors)
    for x in range(30):
        title = "測試標題%d" % x
        content = "測試内容%d" % x
        author_index = random.randint(0, authors_count - 1)
        author = authors[author_index]
        index = random.randint(0, board_count - 1)
        board = boards[index]
        post_model = PostModel(title=title, content=content, author=author, board=board)
        db.session.add(post_model)
    db.session.commit()
    print("測試文章發布成功")
