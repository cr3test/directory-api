from django.conf import settings

import requests


class StannpClient():

    def __init__(self, api_key, test_mode=True):
        self.api_key = api_key
        # If test_mode is set to true then a sample PDF file will be produced
        # but the item will never be dispatched and no charge will be taken.
        self.test_mode = test_mode

    def post(self, url, data):
        response = requests.post(
            url, data=data, auth=(self.api_key, '')
        )
        return response.json()

    def validate_recipient(self, recipient):
        """
        Validates an recipient.

        https://www.stannp.com/direct-mail-api/recipients
        """
        return self.post(
            'https://dash.stannp.com/api/v1/recipients/validate',
            data=recipient
        )

    def send_letter(self, template, recipient, pages):
        """
        Sends a letter.

        https://www.stannp.com/direct-mail-api/letters
        """
        data = {}

        data['recipient[title]'] = recipient['title']
        data['recipient[firstname]'] = recipient['firstname']
        data['recipient[lastname]'] = recipient['lastname']
        data['recipient[address1]'] = recipient['address_line_1']
        data['recipient[address2]'] = recipient['address_line_2']
        data['recipient[city]'] = recipient['locality']
        data['recipient[postcode]'] = recipient['postal_code']
        data['recipient[country]'] = recipient['country']

        data['template'] = template
        data['pages'] = pages
        data['test'] = self.test_mode

        return self.post(
            'https://dash.stannp.com/api/v1/letters/create',
            data,
        )


stannp_client = StannpClient(
    api_key=settings.STANNP_API_KEY,
    test_mode=settings.STANNP_TEST_MODE
)
