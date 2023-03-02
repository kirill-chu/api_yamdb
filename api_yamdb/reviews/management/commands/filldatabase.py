from csv import DictReader

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

DATAPATH = {
    Category: 'static/data/category.csv',
    Genre: 'static/data/genre.csv',
    Title: 'static/data/titles.csv',
    Title.genre.through: 'static/data/genre_title.csv',
    User: 'static/data/users.csv',
    Review: 'static/data/review.csv',
    Comment: 'static/data/comments.csv',
}


class Command(BaseCommand):
    help = 'Use this command to fill the database'

    def handle(self, *args, **options):
        for model in DATAPATH:
            print(f'Start {model.__name__} data transfer')
            try:
                objs = [
                    model.objects.create(**obj)
                    for obj in DictReader(
                        open(DATAPATH[model], encoding='utf8')
                    )
                ]
                model.objects.bulk_create(objs=objs, ignore_conflicts=True)
                print(f'Data successfully loaded into {model.__name__}\n')
            except Exception as erorr:
                print(erorr)
                print(
                    f'We have a problem with data or {model.__name__} model\n'
                )
