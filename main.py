import logging
import os
import json
import requests
import pandas as pd
from slugify import slugify


logger = logging.getLogger(__name__)


class API:
    API_KEY = os.environ['WOW_API_KEY']
    realm = 'die silberne hand'

    @classmethod
    def download_data(cls):
        payload = {
            'locale': 'de_DE',
            'apikey': cls.API_KEY,
        }

        response = requests.get(f'https://eu.api.battle.net/wow/auction/data/{cls.realm}', params=payload).json()
        url = response['files'][0]['url']
        timestamp = response['files'][0]['lastModified']

        logger.info(f'Getting {url}')
        json_data = requests.get(url).json()
        with open('data/{}.json'.format(slugify(cls.realm), timestamp), 'w') as output_file:
            json.dump(json_data, output_file)
            logger.info(f'Saved to {output_file.name}.')


class AuctionData:

    @classmethod
    def from_json(cls, path):
        with open(path, 'r') as data_file:
            data = json.load(data_file)
        dataframe = pd.DataFrame.from_dict(data['auctions'])


def main():
    # API.download_data()
    AuctionData.from_json('data/die-silberne-hand.json')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
