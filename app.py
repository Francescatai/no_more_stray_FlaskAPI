from flask import Flask
# 數據庫遷移
from flask_migrate import Migrate

from models import auth

import config
from exts import db, mail, cache, csrf, avatars
from mycelery import make_celery
from apps.front import front_bp
from apps.media import media_bp
import commands

app = Flask(__name__)
# 配置
app.config.from_object(config)

# mysql數據庫
db.init_app(app)
# mail設置
mail.init_app(app)
# csrf設定
csrf.init_app(app)

# 數據庫遷移設定
# flask db init
# flask db migrate
# flask db upgrade
migrate = Migrate(app, db)
# celery設定
celery = make_celery(app)
# cache設定
cache.init_app(app)
# 頭像設定
avatars.init_app(app)

# blueprint
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)

# 命令
# flask init_boards
app.cli.command("init_boards")(commands.init_boards)
app.cli.command("create_test_posts")(commands.create_test_posts)

if __name__ == '__main__':
    app.run(debug=True)
