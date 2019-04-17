import requests
import json

header = {
    'content-type':'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'cache-control': "no-cache"
}

class Api(object):
    def __init__(self, username=None, password=None):
         self._session = requests.Session()
         self.username = username
         self.password = password
         self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

         self._session.headers = {
             'content-type':'application/json',
             'user-agent': self.user_agent,
             'cache-control': "no-cache"
         }

         if username and password:
             login_info = {
                 "username":username,
                 "password":password,
                 "type":"password",
                 "domain":"NLD"
                 }
             url = requests.post('https://www.ah.nl/service/loyalty/rest/tokens', headers=self._session.headers, data=json.dumps(login_info))
             if url.status_code == 200:
                 url_json = url.json()

                 token_data = {
                     'client-id':url_json['clientId'],
                     'token':url_json['token']
                     }

                 clean_cookies = []
                 got_one = True
                 for i in url.headers['set-cookie'].split(','):
                     if "ahold_presumed_member_no=" in i and token_data['client-id'] in i and got_one:
                         clean_cookies.append(i[1:].split(';')[0])
                         got_one = False
                     if "ah_token=" in i:
                         clean_cookies.append(i[1:].split(';')[0])

                 self._session.headers.update({
                     "cookie": clean_cookies[1]+";"+clean_cookies[0]
                 })
             else:
                 print("Couldn't fulfill request / Wrong credentials")
         else:
             print("Fill in credentials")

    def add(self, product_id, amount = 1):
        product_data = {
            "type":"PRODUCT",
            "item":
                {
                    "id":product_id
                },
            "quantity":amount,
            "originCode":"PDT"
            }
        url = requests.post('https://www.ah.nl/service/rest/shoppinglists/0/items', headers=self._session.headers, data=json.dumps(product_data))
        if url.status_code != 200:
            print("could not add to cart")
        else:
            return True
    def cart(self):
        url = requests.get('https://www.ah.nl/service/rest/delegate', params={"url":"/mijnlijst"}, headers=self._session.headers)
        shop = url.json()
        products = []
        for i in shop['_embedded']['lanes'][5]['_embedded']['items']:
            product = {
                'name': i['_embedded']['product']['description'].replace('\xad', ''),
                'href': i['navItem']['link']['href'],
                'brandName':i['_embedded']['product']['brandName'],
                'priceLabel':i['_embedded']['product']['priceLabel']['now']
            }
            products.append(product)

        return {
            'itemsCount': shop['_meta']['shoppingList']['itemCount'],
            'items': products
        }

    def shopping_list_add(self,name,empty_cart = False):
        hdr = self._session.headers.copy()
        description = {
            'description':name
        }
        hdr['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        url = requests.post('https://www.ah.nl/lijstjes/toevoegen',headers=hdr, data=description)
        if empty_cart == True:
            self.empty()

    def empty(self):
            url = requests.delete('https://www.ah.nl/service/rest/shoppinglists/0/items', headers=self._session.headers)
            if url.status_code == 200:
                return True
            else:
                return False

class Product(object):
    def __init__(self, url):
        self.url = url
        res = requests.get('https://www.ah.nl/service/rest/delegate?url=producten/product/{}'.format(url))
        if res.status_code != 200:
            print("Cant connect to product details")
        else:
            res = res.json()

            for lane in res['_embedded']['lanes']:
                if lane['type'] == 'ProductDetailLane':
                    for item in lane['_embedded']['items']:
                        if item['type'] == 'Product':
                            product = item['_embedded']['product']
                            self.id = product.get('id', None)
                            self.brand = product.get('brandName', None)
                            self.description = product.get('description', '').replace('\xad', '')
                            self.summary = product.get('details', {}).get('summary', None)
                            self.unit_size = product.get('unitSize', None)
                            self.category = product.get('categoryName', None)
                            self.is_available = product.get('availability', {}).get('orderable', False)
                            priceLabel = product.get('priceLabel', {})
                            self.price_current = priceLabel.get('now', None)
                            self.price_previous = priceLabel.get('was', None)
                            self.is_discounted = 'discount' in product
