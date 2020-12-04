from bs4 import BeautifulSoup as bs4
import requests
import json
import csv

class zillowscraper():
    result=[]
    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'zguid=23|%24d664d476-adad-4558-b452-b73a9bc85bd4; zgsession=1|96d77c4d-46da-44e8-8efd-8ec4ca5cac4c; _ga=GA1.2.195451508.1587044381; _gid=GA1.2.1976668325.1587044381; zjs_user_id=null; zjs_anonymous_id=%22d664d476-adad-4558-b452-b73a9bc85bd4%22; _pxvid=b9f2a9c1-7fe7-11ea-8eb2-0242ac12000c; _gcl_au=1.1.575077272.1587044384; KruxPixel=true; DoubleClickSession=true; _fbp=fb.1.1587044385426.2047090831; KruxAddition=true; __gads=ID=d3db3f2cda2d9e8d:T=1587044516:S=ALNI_MZIiD5jQOsN8JILLL_gRJtoWbPulA; ki_t=1587044519427%3B1587044519427%3B1587044519427%3B1%3B1; ki_r=; JSESSIONID=20FA1B90AFF01F58C269E115906E069B; GASession=true; _uetsid=_uetf0a8b5bf-16f5-93b6-9675-3d972e441d12; _px3=4f3c9ee94f62033acdc9976ab48c11c409d0e07698110c78148ff8aa49c86c4d:nis5Y8gZ8ZIINmRut+EbtDKTKQo+HaIjktMKIzfODLF/iV0i7ldTR8KMsbkwWjwS0/77TH251fXNUvO1mDTJEA==:1000:k56HOnUy2wQnIN7I0ZZV54BXN91r8GH1rTx5WXvK2f3X7PnJIPFdupmlRMXmrKrPbU4u+195oie/p/uO37AHVb9MRhdBD7atWfuyeeixWs1+uLR1w3euIcO4I9vaQie+N2sWmipvcakNy4tfv7GNzRmbArnkpA6vJtatgqaHfI8=; AWSALB=HmueCXck1396LsC5WBti+ORQRwt4W7mkad0z5buceODY2WeiJLVPSs9REwF5oCs5chIIvcspqFfN4BwUxxwya3+KknLjUdfBV+syVM+NSsfVJU3dAnMvQkW7kUbe; AWSALBCORS=HmueCXck1396LsC5WBti+ORQRwt4W7mkad0z5buceODY2WeiJLVPSs9REwF5oCs5chIIvcspqFfN4BwUxxwya3+KknLjUdfBV+syVM+NSsfVJU3dAnMvQkW7kUbe; search=6|1589675505436%7Crect%3D40.951655440557104%252C-73.5549828671875%252C40.45924069713026%252C-74.4009301328125%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D0%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%09%096181%09%09%09%09%09%09',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

    def fetch(self, url, params):
        print('HTTP GET request to URL: %s' %url, end='')
        res=requests.get(url, params=params, headers=self.headers)
        print(' status code: %s' % res.status_code)
        return res

    def save_response(self, res):
        with open('res.html', 'w', encoding="utf-8") as html_file:
            html_file.write(res)

    def load_response(self):
        html=''
        with open('res.html', 'r', encoding="utf-8") as html_file:
            for line in html_file:
                html+=line
        return html

    def parse(self, html):
        content=bs4(html, 'lxml')
        cards=content.findAll('article', {'class':"list-card"})
        for card in cards:
            try:
                ba=card.find('ul', {'class': 'list-card-details'}).findAll('li')[1].text.split(' ')[0]
            except:
                ba='Null'
            try:
                sqft=card.find('ul', {'class': 'list-card-details'}).findAll('li')[2].text.split(' ')[0]
            except:
                sqft='Null'
            self.result.append({
                'price': card.find('div', {'class': 'list-card-price'}).text,
                'address': card.find('address', {'class': 'list-card-addr'}).text,
                'bds': card.find('ul', {'class': 'list-card-details'}).findAll('li')[0].text.split(' ')[0],
                'ba': ba,
                'sqft': sqft
            })
            # print(json.dumps(item, indent=2))

    def to_csv(self):
        with open('zillow.csv', 'a') as csv_file:
            writer=csv.DictWriter(csv_file, fieldnames=self.result[0].keys())
            writer.writeheader()

            for row in self.result:
                writer.writerow(row)


    def run(self):
        for page in range(1, 21):
            params={'searchQueryState': '{"pagination":{"currentPage:"%s},"mapBounds":{"west":-74.4009301328125,"east":-73.5549828671875,"south":40.45924069713026,"north":40.951655440557104},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":True}' %page } 
            res=self.fetch('https://www.zillow.com/homes/london_rb/', params)
            
            self.parse(res.text)
        self.to_csv()



if __name__ == '__main__':
    scraper=zillowscraper()
    scraper.run()