set positional-arguments

[working-directory: 'src']
makemigrations:
    uv run python manage.py makemigrations



[working-directory: 'src']
migrate:
    uv run python manage.py migrate


[working-directory: 'src']
admin:
    uv run python manage.py createsuperuser

[working-directory: 'src']
worker:
    uv run ./entrypoint-worker.sh


#[working-directory: 'src']
#test *ARGS:
#    uv run python manage.py test -v 3 $@

update:
    git pull
    docker compose build
    docker compose up -d


[working-directory: 'src']
seed *ARGS:
    uv run python manage.py seed $@
