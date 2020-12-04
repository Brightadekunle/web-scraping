from bs4 import BeautifulSoup as bs4
import requests
import json
import csv

class truliascraper():
    result=[]
    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '_pxhd=2d1a663c04a31e8d06e3444f11d9f43e6fd2c2549fe25080d642e429ac418ff9:490f74b1-8183-11ea-8880-bb6aa557e23f; _csrfSecret=13RqAcnLH6216WD3OHcmeerJ; tlftmusr=200418q8zno9bc53cat298scuqvdm490; s_fid=6751082593EFEEB7-3F971A0A0C2BF519; s_cc=true; s_vi=[CS]v1|2F4D89510515BAC9-4000076D8D93E1C1[CE]; _pxvid=490f74b1-8183-11ea-8880-bb6aa557e23f; zjs_user_id=null; zjs_anonymous_id=%22200418q8zno9bc53cat298scuqvdm490%22; PHPSESSID=8uanh1qprl8ujmj8lhbvl4rm30; csrft=RFIVVTjpjDQ5rMMiX3cwNZZlB5nJP53HvqcPU4nkCyk%3D; _ga=GA1.2.1899196445.1587221166; _gid=GA1.2.1204963509.1587221166; G_ENABLED_IDPS=google; QSI_S_ZN_aVrRbuAaSuA7FBz=v:0:0; _pxff_tm=1; __gads=ID=b2a5a38b5fdc79f4:T=1587221217:S=ALNI_MZdGO8ZDt4r0vOeOi-oCTB2SmOglg; SERVERID=webfe24|XpsTr; trul_visitTimer=1587221150301_1587221428593; s_sq=%5B%5BB%5D%5D; OptanonConsent=isIABGlobal=false&datestamp=Sat+Apr+18+2020+15%3A50%3A30+GMT%2B0100+(West+Africa+Standard+Time)&version=5.8.0&landingPath=NotLandingPage&AwaitingReconsent=false&groups=1%3A1%2C0_234869%3A1%2C3%3A1%2C4%3A1%2C0_234866%3A1%2C0_234867%3A1%2C0_234868%3A1%2C0_240782%3A1%2C0_240783%3A1%2C0_240780%3A1%2C0_234871%3A1%2C0_240781%3A1%2C0_234872%3A1%2C0_234873%3A1%2C0_234874%3A1%2C0_234875%3A1%2C0_234876%3A1%2C0_234877%3A1; _px3=a7ca062a3a1ca9b58f1002b0b2478724287fdc2e0e7c017c3c77cc2b61d93f55:SXBuRy8N1yMHZyVnthjy+k8fx0Q+a44myvykU+OSodCbY9K/vRAqqZEwU/cu2ECigN/93sCJBOTz6IWwZCPfcg==:1000:gswTKeWksjGCtWNlbfGPY5ikBZdADJZPcl3LA2wzIrniCCGDSEBcSU9nQfmMCxcHEHGR6xo7yZ7QAki1Ji2W/dWBPg+0oiMk94WQGqGsw5GKji1UbgmeFakLMP+kFog28Lgck7JmgKdZY2V9CVbsB0M1UPVT4AuoBmJ5RMkOYKI=',
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
        cards=content.findAll('div', {'class': 'Box-sc-8ox7qa-0 jIGxjA'})
        for card in cards:
            try:
                ba = card.find('div', {'data-testid': 'property-baths'}).text.split('b')[0]
            except:
                ba = 'Null'
            try:
                bds = card.find('div', {'data-testid': 'property-beds'}).text.split('b')[0]
            except:
                bds = 'Null'
            try:
                sqft = card.find('div', {'data-testid': 'property-floorSpace'}).text.split('s')[0]
            except:
                sqft = 'Null'


            self.result.append({
                'Price': card.find('div', {'class': 'Text__TextBase-sc-1i9uasc-0-div Text__TextContainerBase-sc-1i9uasc-1 kNBbhi'}).text,
                'address': card.find('div', {'data-testid': 'property-street'}).text,
                'region': card.find('div', {'data-testid': 'property-region'}).text,
                'bds': bds,
                'ba': ba,
                'sqft': sqft 
            })

            # print(json.dumps(item, indent=2))
    def to_csv(self):
        with open('trulia.csv', 'a') as csv_file:
            writer=csv.DictWriter(csv_file, fieldnames=self.result[0].keys())
            writer.writeheader()

            for row in self.result:
                writer.writerow(row)


    def run(self):
        for page in range(1,2):
            params={'searchQueryState': '{"pagination":{"currentPage:"%s},"mapBounds":{"west":-74.4009301328125,"east":-73.5549828671875,"south":40.45924069713026,"north":40.951655440557104},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":True}' %page} 
            res=self.fetch('https://www.trulia.com/AL/Horton/', params)
            
            self.parse(res.text)
        # self.parse(html)
        self.to_csv()



if __name__ == '__main__':
    scraper=truliascraper()
    scraper.run()