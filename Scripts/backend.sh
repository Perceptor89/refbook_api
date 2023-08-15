python manage.py migrate &&

python manage.py collectstatic --noinput &&

if [ ${DEBUG} = True ];
    then
        echo 'Debug is True: starting develop...'
        python manage.py runserver 0.0.0.0:8000
    else
        echo 'Debug is False: starting production...'
        gunicorn refbook_api.wsgi --bind 0.0.0.0:8000
fi