FLASK_ENV=development
FLASK_APP=auth_service_api.app:create_app
SECRET_KEY=changeme
DATABASE_URI=postgresql://postgres:admin123@postgres:15033/auth_service_db
TZ=Asia/Qyzylorda
PGTZ=Asia/Qyzylorda
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=rpc://
