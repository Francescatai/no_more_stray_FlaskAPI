from flask_mail import Message
from exts import mail
from celery import Celery


# 發送email任務
def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], body=body)
    try:
        mail.send(message)
        return {"status": "SUCCESS"}
    except:
        return {"status": "FAILURE"}


# 創建celery對象
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    # 定義父類:在flask執行要有app上下文
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    # 綁定到app上
    app.celery = celery

    # 添加任務
    celery.task(name="send_mail")(send_mail)

    return celery
