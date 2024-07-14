ChatGPT clone

# Commands for dev environment
npm run start
docker compose up
source venv/bin/activate
watchfiles 'celery -A chat_ai_app worker --loglevel=info' chat_ai_app
python manage.py runserver