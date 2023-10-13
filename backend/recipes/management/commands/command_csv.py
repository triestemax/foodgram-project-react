import csv

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredients, Tag

CSV_PATH = 'data/'

DICT_MODELS_WITH_CSV_FILES = {
    Ingredients: 'ingredients.csv',
    Tag: 'tags.csv',
}


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def handle(self, *args, **kwargs):
        for model in DICT_MODELS_WITH_CSV_FILES:
            try:
                with open(
                    CSV_PATH + DICT_MODELS_WITH_CSV_FILES[model],
                    newline='', encoding='UTF-8'
                ) as csv_file:
                    file_reader = csv.DictReader(csv_file, delimiter=",")
                    objects = []
                    for row in file_reader:
                        objects.append(model(**row))
                    model.objects.bulk_create(objects)
                    print(
                        f'Миграция из {DICT_MODELS_WITH_CSV_FILES[model]} '
                        f'в таблицу {model} выполнено успешно!'
                    )
            except Exception as error:
                print(error)
                CommandError(error)
