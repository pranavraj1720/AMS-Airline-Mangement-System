import requests, json

class INDIGO_DB:
    def __init__(self):
        self.headers = {
            'authority': 'api-prod-flight-skyplus6e.goindigo.in',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.goindigo.in',
            'referer': 'https://www.goindigo.in/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.setup()

    def setup(self):
        self.headers['user_key'] = "654a6a3cc4998e498e5c0c8ead072915"

    def get_auth(self):
        json_data = {
            'strToken': '',
            'subscriptionKey': 'S9pIpbp4QxCTs98Nzrmy0A==',
        }

        headers = {
            'authority': 'api-prod-session-skyplus6e.goindigo.in',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'access-control-allow-origin': '*',
            'content-type': 'application/json',
            'origin': 'https://www.goindigo.in',
            'referer': 'https://www.goindigo.in/',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'user_key': '654a6a3cc4998e498e5c0c8ead072915',
        }
        response = requests.post('https://api-prod-session-skyplus6e.goindigo.in/v1/token/create', headers = headers, json=json_data)

        token = response.json()['data']['token']['token']
        idleTimeoutInMinutes = response.json()['data']['token']['idleTimeoutInMinutes']
        return token, idleTimeoutInMinutes


    def get_fligits(self, src, dest, beginDate, currency = "INR"):
        token, _ = self.get_auth()
        headers = {
          'authority': 'api-prod-flight-skyplus6e.goindigo.in',
          'accept': 'application/json, text/plain, */*',
          'accept-language': 'en-US,en;q=0.9',
          'authorization': token,
          'content-type': 'application/json',
          'origin': 'https://www.goindigo.in',
          'referer': 'https://www.goindigo.in/',
          'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-site',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
          'user_key': '31e90be8fff2f5e2eea242c225f21b1a',
      }

        # beginDate = yyyy-mm-dd

        json_data = {
            'codes': {
                'currency': currency,
                'promotionCode': '',
            },
            'criteria': [
                {
                    'dates': {
                        'beginDate': beginDate,
                    },
                    'flightFilters': {
                        'type': 'All',
                    },
                    'stations': {
                        'originStationCodes': [
                            src,
                        ],
                        'destinationStationCodes': [
                            dest,
                        ],
                    },
                },
            ],
            'passengers': {
                'residentCountry': 'IN',
                'types': [
                    {
                        'type': 'ADT',
                        'discountCode': '',
                        'count': 1,
                    },
                ],
            },
            'taxesAndFees': 'TaxesAndFees',
        }

        response = requests.post('https://api-prod-flight-skyplus6e.goindigo.in/v1/flight/search', headers=headers, json=json_data)
        journeysAvailable =  response.json()['data']['trips'][0]['journeysAvailable']
        filtered_journeys = [journey for journey in journeysAvailable if len(journey['passengerFares']) != 0]

        # print(filtered_journeys)

        return filtered_journeys


