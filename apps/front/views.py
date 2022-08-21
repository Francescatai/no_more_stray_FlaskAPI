from flask import Blueprint, request, render_template, current_app, make_response, session, redirect, g
import string
import random
from hashlib import md5
from io import BytesIO
import time
from flask_avatars import Identicon
import os
from flask_paginate import get_page_parameter, Pagination
from sqlalchemy.sql import func

from exts import db, cache
from utils import restful
from utils.captcha import Captcha
from .forms import RegisterForm, LoginForm, UploadImageForm, EditProfileForm, PublicPostForm, PublicCommentForm
from models.auth import UserModel
from models.post import BoardModel, PostModel, CommentModel, BannerModel
from .decorators import login_required

bp = Blueprint("front", __name__, url_prefix="/")

# 請求過程:before_request => blueprint函數（返回模板） => context_processor => 將context_processor返回的變量也添加到模板中


# 鉤子函數：before_request，在調用其他blueprint內函數前執行
@bp.before_request
def front_before_request():
    if 'user_id' in session:
        user_id = session.get("user_id")
        user = UserModel.query.get(user_id)
        # setattr(object, name, values):給object的屬性賦值，若屬性不存在，先創建再賦值
        setattr(g, "user", user)


# 上下文處理器
@bp.context_processor
def front_context_processor():
    # hasattr(object, name):判斷object裡是否有name屬性或name方法，返回bool值
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


@bp.route("/")
def index():
    sort = request.args.get("st", type=int, default=1)
    board_id = request.args.get("bd", type=int, default=None)
    boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
    post_query = None
    if sort == 1:
        post_query = PostModel.query.order_by(PostModel.create_time.desc())
    else:
        # 根據討論量進行排序
        post_query = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 1：0-9
    # 2：10-19
    start = (page - 1) * current_app.config['PER_PAGE_COUNT']
    end = start + current_app.config['PER_PAGE_COUNT']

    if board_id:
        # "mapped class CommentModel->comment" has no property "board_id"
        # CommentModel中尋找board_id，然后進行filter
        # post_query = post_query.filter_by(board_id=board_id)
        post_query = post_query.filter(PostModel.board_id == board_id)
    total = post_query.count()
    posts = post_query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total, prev_label="上一頁")

    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    context = {
        "boards": boards,
        "posts": posts,
        "pagination": pagination,
        "st": sort,
        "bd": board_id,
        "banners": banners
    }
    return render_template("front/index.html", **context)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("front/login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            print(request.form)
            print(type(request.form))
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return restful.params_error("Email或密碼錯誤")
            if not user.check_password(password):
                return restful.params_error("Email或密碼錯誤")
            if not user.is_active:
                return restful.params_error("此用戶不可登入")
            session['user_id'] = user.id
            if remember == 1:
                # 默認session過期時間，只要瀏覽器關閉就會過期
                session.permanent = True
            return restful.ok()
        else:
            return restful.params_error(message=form.messages[0])


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            identicon = Identicon()
            filenames = identicon.generate(text=md5(email.encode("utf-8")).hexdigest())
            avatar = filenames[2]
            user = UserModel(email=email, username=username, password=password, avatar=avatar)
            db.session.add(user)
            db.session.commit()
            return restful.ok()
        else:
            # form.errors中存放了所有的錯誤訊息
            # {'graph_captcha': ['請輸入正確的圖形驗證碼！', '圖形驗證碼錯誤！']}
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.get("/email/captcha")
def email_captcha():
    email = request.args.get("email")
    if not email:
        return restful.params_error(message="請先輸入Email")
    # 隨機6位數
    source = list(string.digits)
    captcha = "".join(random.sample(source, 6))
    subject = "【齊助浪寶】註冊驗證碼"
    body = "【齊助浪寶】您的註冊驗證碼：%s" % captcha
    current_app.celery.send_task("send_mail", (email, subject, body))
    cache.set(email, captcha)
    print(cache.get(email))
    return restful.ok(message="Email發送成功")


@bp.route("/graph/captcha")
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    # 緩存驗證碼
    # key, value
    # bytes
    key = md5((captcha+str(time.time())).encode('utf-8')).hexdigest()
    cache.set(key, captcha)
    print(cache.set(key, captcha))
    out = BytesIO()
    image.save(out, "png")
    # 把out的文件指针指向一開始的位置
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = "image/png"
    # 把key設置到cookie
    resp.set_cookie("_graph_captcha_key", key, max_age=3600)
    return resp


@bp.route("/setting")
@login_required
def setting():
    email_hash = md5(g.user.email.encode("utf-8")).hexdigest()
    return render_template("front/setting.html", email_hash=email_hash)


@bp.post("/avatar/upload")
@login_required
def upload_avatar():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        # 不使用用戶自己傳上來的文件名，避免惡意攻擊
        filename = image.filename
        # xxx.png,xx.jpeg
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email + str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        g.user.avatar = filename
        db.session.commit()
        return restful.ok(data={"avatar": filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.post("/profile/edit")
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if form.validate():
        signature = form.signature.data
        g.user.signature = signature
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])


@bp.route("/post/public", methods=['GET', 'POST'])
@login_required
def public_post():
    if request.method == 'GET':
        boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            try:
                # get方法：接收id，如果id存在就會返回
                # 如果没有找到id就會報錯
                board = BoardModel.query.get(board_id)
            except:
                return restful.params_error(message="討論分類不存在！")
            post_model = PostModel(title=title, content=content, board=board, author=g.user)
            db.session.add(post_model)
            db.session.commit()
            return restful.ok(data={"id": post_model.id})
        else:
            return restful.params_error(message=form.messages[0])


@bp.post("/post/image/upload")
@login_required
def upload_post_image():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        # 不要使用用户上传上来的文件名，否则容易被黑客攻击
        filename = image.filename
        # xxx.png,xx.jpeg
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email + str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['POST_IMAGE_SAVE_PATH'], filename)
        image.save(image_path)
        # {"data","code", "message"}
        return jsonify({"errno": 0, "data": [{
            "url": url_for("media.get_post_image", filename=filename),
            "alt": filename,
            "href": ""
        }]})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.get("/post/detail/<post_id>")
def post_detail(post_id):
    post_model = PostModel.query.get(post_id)
    comment_count = CommentModel.query.filter_by(post_id=post_id).count()
    context = {
        "comment_count": comment_count,
        "post": post_model
    }
    return render_template("front/post_detail.html", **context)


@bp.post("/comment")
@login_required
def public_comment():
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        try:
            post_model = PostModel.query.get(post_id)
        except:
            return restful.params_error(message="文章不存在！")
        comment = CommentModel(content=content, post_id=post_id, author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return restful.ok()
    else:
        message = form.messages[0]
        return restful.params_error(message=message)