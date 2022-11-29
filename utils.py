import csv
import json
import os

from collections import namedtuple

import django
from django.core import management
from django.conf import settings


AD_MAPPING = {
    'name': 'name',
    'author_id': 'author',
    'price': 'price',
    'description': 'description',
    'is_published': 'is_published',
    'image': 'image',
    'category_id': 'category',
}

CATEGORY_MAPPING = {
    'name': 'name',
}

LOCATION_MAPPING = {
    'name': 'address',
    'lat': 'latitude',
    'lng': 'longitude',
}

USER_MAPPING = {
    'first_name': 'first_name',
    'last_name': 'last_name',
    'username': 'username',
    'password': 'password',
    'role': 'role',
    'age': 'age',
    'location_id': 'location',
}


def load_csv(filename: str) -> list[dict]:
    with open(settings.BASE_DIR / 'datasets' / filename, encoding='utf-8') as f:
        data = [*csv.DictReader(f)]

    return data


def load_csv_to_fixture(source: str, destination: str, model_name: str, mapping: dict) -> None:
    data = load_csv(source)
    fixture = []

    for row in data:
        obj = {
            "model": model_name,
            "pk": int(row['id'] if 'id' in row else row['Id']),
            "fields": {}
        }

        for key, value in mapping.items():
            if key.endswith('_id') or key == 'age':
                obj['fields'][value] = int(row[key])

            elif key == 'is_published':
                obj['fields'][value] = True if row[key] == 'TRUE' else False

            else:
                obj['fields'][value] = row[key]

        fixture.append(obj)

    save_json_fixture(destination, fixture)


def load_models(models_order: tuple, models: dict) -> None:
    for model in models_order:
        load_csv_to_fixture(
            source=models[model].source,
            destination=models[model].destination,
            model_name=models[model].model_name,
            mapping=models[model].mapping
        )


def run_call_commands(models_order: tuple, models: dict) -> None:
    for model in models_order:
        management.call_command('loaddata', f'fixtures/{models[model].destination}')


def save_json_fixture(filename: str, data: list[dict]) -> None:
    with open(settings.BASE_DIR / 'fixtures' / filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bulletin_board_system.settings'
    django.setup()

    Model = namedtuple('Model', 'source destination model_name mapping')

    all_models_data = {
        'ads': Model('ads.csv', 'ads.json', 'ads.Ad', AD_MAPPING),
        'categories': Model('categories.csv', 'categories.json', 'ads.Category', CATEGORY_MAPPING),
        'locations': Model('locations.csv', 'locations.json', 'ads.Location', LOCATION_MAPPING),
        'users': Model('users.csv', 'users.json', 'ads.User', USER_MAPPING)
    }
    order_to_run_models = ('locations', 'categories', 'users', 'ads')

    load_models(models_order=order_to_run_models, models=all_models_data)
    run_call_commands(models_order=order_to_run_models, models=all_models_data)
