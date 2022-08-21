from flask import request
from wtforms.fields import StringField, IntegerField, FileField
from wtforms import Form, ValidationError
from wtforms.validators import Email, Length, EqualTo, InputRequired
from flask_wtf.file import FileAllowed, FileSize
from models.auth import UserModel
from exts import cache


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.extend(errors)
        return message_list


class RegisterForm(BaseForm):
    # pip install email_validator
    email = StringField(validators=[Email(message="請輸入正確的Email")])
    email_captcha = StringField(validators=[Length(6, 6, message="請輸入正確的email驗證碼")])
    username = StringField(validators=[Length(3, 20, message="請輸入3-20個字長的用戶名")])
    password = StringField(validators=[Length(6, 20, message="請輸入6-20位密碼")])
    repeat_password = StringField(validators=[EqualTo("password", message="兩次輸入密碼不一致")])
    graph_captcha = StringField(validators=[Length(4, 4, message="請輸入正確的圖形驗證碼")])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError(message="Email不能重複註冊")

    def validate_email_captcha(self, field):
        email_captcha = field.data
        email = self.email.data
        # 從緩存取出驗證碼
        cache_captcha = cache.get(email)
        if not cache_captcha or email_captcha != cache_captcha:
            raise ValidationError(message="Email驗證碼錯誤")

    def validate_graph_captcha(self, field):
        key = request.cookies.get("_graph_captcha_key")
        # 從緩存取出驗證碼
        cache_captcha = cache.get(key)
        graph_captcha = field.data
        # 全部轉成小寫再比對
        if not cache_captcha or cache_captcha.lower() != graph_captcha.lower():
            raise ValidationError(message="圖形驗證碼錯誤")


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message="請輸入正確的Email")])
    password = StringField(validators=[Length(6, 20, message="請輸入正確的密碼")])
    remember = IntegerField()


class UploadImageForm(BaseForm):
    image = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="圖片格式不符合規定"), FileSize(max_size=1024*1024*5, message="圖片最大不能超過5M")])


class EditProfileForm(BaseForm):
    signature = StringField(validators=[Length(max=50, message="個性簽名最多50字")])


class PublicPostForm(BaseForm):
    title = StringField(validators=[Length(max=200, message="討論標題最多200字")])
    content = StringField(validators=[InputRequired(message="請輸入內容")])
    board_id = IntegerField(validators=[InputRequired(message="請選擇討論分類")])


class PublicCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message="請輸入內容")])
    post_id = IntegerField(validators=[InputRequired(message="請選擇討論文章")])