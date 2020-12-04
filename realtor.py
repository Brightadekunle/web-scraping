from bs4 import BeautifulSoup as bs4
import requests
import json
import csv


class realtorscraper():
    result = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'split_tcv=189; __vst=17b28cb8-4ab7-43d1-955c-07acd965d958; ab.storage.userId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%22visitor_17b28cb8-4ab7-43d1-955c-07acd965d958%22%2C%22c%22%3A1586989048386%2C%22l%22%3A1586989048386%7D; ab.storage.deviceId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%223d59373c-f87e-09f9-ccd2-e2135d5134d3%22%2C%22c%22%3A1586989048397%2C%22l%22%3A1586989048397%7D; __gads=ID=c5025c41af26b553:T=1586989044:S=ALNI_MY5m6mKDMBXAC22CT5Ry8RLdUU6Ew; s_ecid=MCMID%7C70257912586621233631631401363441397307; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22768e32a4-7ed4-4e71-8f75-dfe0ab996267%22; _tac=false~self|not-available; _ta=us~1~89df68bc35032d48c293adce8574aa42; G_ENABLED_IDPS=google; _ga=GA1.2.42452822.1586989043; _fbp=fb.1.1586989080651.1521163251; __qca=P0-1434068557-1586989099598; threshold_value=100; clstr=v; clstr_tcv=64; QSI_SI_6DNTqAMybsoeO2N_intercept=true; _ncg_g_id_=b2a3898d-399d-43cc-94ca-5e4ab83cd7d7; _ncg_id_=17180b3f245-25279534-91d6-458b-9851-1960780f51b7; last_ran=1587052717851; split=v; __ssnstarttime=1587304023; __ssn=790f2b13-6aa9-47a3-95f5-2d20b63ef3b9; __split=80; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1712354808%7CMCIDTS%7C18372%7CMCMID%7C70257912586621233631631401363441397307%7CMCAAMLH-1587908831%7C6%7CMCAAMB-1587908831%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1587311231s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; _gid=GA1.2.1064567646.1587304040; _ncg_sp_ses.cc72=*; user_activity=return; last_ran=-1; _tas=7f01ohdz2rs; user_canceled_one_tap=true; srchID=4da953e6aef4415b96aca5bb2d8b4d17; criteria=pg%3D1%26locSlug%3DHartford-County_CT%26sprefix%3D%252Frealestateandhomes-search%26county%3DHartford%2520County%26state_code%3DCT%26area_type%3Dcounty%26search_type%3Dcounty%26state_id%3DCT%26lat%3D41.8060534%26long%3D-72.7329157%26loc%3DHartford%2520County%252C%2520CT; last_ran_threshold=1587309092500; ab.storage.sessionId.7cc9d032-9d6d-44cf-a8f5-d276489af322=%7B%22g%22%3A%2250146e89-d1f2-d11e-b13f-da6199b705f2%22%2C%22e%22%3A1587310895372%2C%22c%22%3A1587307716074%2C%22l%22%3A1587309095372%7D; reese84=3:V1Itd2/uGBO614I5kwHpbQ==:pGrGfeTllGUpsXcFgtpXqm+NtmmOo1NzfMcdoSGARYk6PZDG985takRw2YDWH17Ymcx6HAi94p2zt016YBPtKYzXUnpR0HlWi7e0t3ckUdhDniotHknQbdNQVAYxHZet+05JBvreshmLCbBl10Xjndg76Iw107hZtYJ+U/cFu+5g4PdO+zOKQXjteAd6dPHC7WVu9sbVVyBfg6YjKK6iiSEgXLUwOFYGdCPjFonXP+ILXXJP0/LLyF7ksdLzHfJCCQSwjY33qv1Wm/cpwMrxWR2c2uuawhGxSIQc8kmSC9RF44XXTPOnOT50/iJPQyEztEMichbhxnXWXimoxwwPgKPWRrD2WRy6OTUzRomETs8rk8IMV6zk+TaNYV7f6FW5aFCOiQrA4jiE+LeyO7ZSNf1LqpkB1Izf3D3W1AdHGrA=:RyYoY09kAXhERGhKhQGrtX25xg+qR4UklS4hLelWIDU=; adcloud={%22_les_v%22:%22y%2Crealtor.com%2C1587310897%22}; QSI_HistorySession=https%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FAlaska%2Fcounties~1587307445442%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FSoutheast-Fairbanks-County_AK%2Fexplore~1587307450217%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FAlaska%2Fcounties~1587307526438%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FBethel-County_AK%2Fexplore~1587307532083%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FAlaska%2Fcounties~1587307533702%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FJuneau-County_AK%2Fexplore~1587307542328%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FAlaska%2Fcounties~1587307618768%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FPetersburg-County_AK%2Fexplore~1587307624945%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FAlaska%2Fcounties~1587307677938%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FAlaska~1587307679575%7Chttps%3A%2F%2Fwww.realtor.com%2F~1587307694373%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FLos-Angeles-County_CA~1587307719380%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FLos-Angeles-County_CA%2Fpg-2~1587307742291%7Chttps%3A%2F%2Fwww.realtor.com%2F~1587308300748%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FOrleans-County_LA~1587308329678%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FOrleans-County_LA%2Fpg-52~1587308343232%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FOrleans-County_LA~1587308377785%7Chttps%3A%2F%2Fwww.realtor.com%2F~1587308407331%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FMiami-Dade-County_FL~1587308428921%7Chttps%3A%2F%2Fwww.realtor.com%2F~1587309079375%7Chttps%3A%2F%2Fwww.realtor.com%2Frealestateandhomes-search%2FHartford-County_CT~1587309099461; _ncg_sp_id.cc72=8ce4381b-3220-49ed-ae91-26267b27b314.1586989087.1.1587309100.1586989087.1065da4d-985d-49b5-9f69-fa9a2e93da97; _gat=1; _uetsid=_uet2c4ea40a-5e11-a0b6-af9d-60bf07f65221',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }

    def fetch(self, url, params):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url, params=params, headers=self.headers)
        print(' status code: %s' % res.status_code)
        return res

    def save_response(self, res):
        with open('res.html', 'w', encoding="utf-8") as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''
        with open('res.html', 'r', encoding="utf-8") as html_file:
            for line in html_file:
                html += line
        return html

    def parse(self, html):
        content = bs4(html, 'lxml')
        cards = content.findAll(
            'li', {'class': "jsx-3446352583 component_property-card"})
        for card in cards:
            try:
                sqft = card.find('ul', {
                                 'class': 'jsx-1140360578 property-meta list-unstyled'}).findAll('li')[2].text.split('s')[0]
            except:
                sqft = 'Null'

            try:
                sqftlot = card.find('ul', {
                                    'class': 'jsx-1140360578 property-meta list-unstyled'}).findAll('li')[3].text.split('s')[0]
            except:
                sqftlot = 'Null'

            try:
                ba = card.find('ul', {
                               'class': 'jsx-1140360578 property-meta list-unstyled'}).findAll('li')[1].text.split('b')[0]
            except:
                ba = 'Null'

            try:
                bds = card.find(
                    'li', {'class': 'jsx-1140360578 prop-meta srp_list'}).text.split('b')[0]
            except:
                bds = 'Null'

            self.result.append({
                'price': card.find('div', {'class': 'jsx-543673669 price'}).text,
                'address':  card.find('div', {'class': 'jsx-543673669 address ellipsis'}).text,
                'bds': bds,
                'ba': ba,
                'sqft': sqft,
                'sqftlot': sqftlot
            })

            # print(json.dumps(items, indent=2))

    def to_csv(self):
        # pass
        with open('realtor.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.result[0].keys())
            writer.writeheader()

            for row in self.result:
                writer.writerow(row)

    def run(self):
        for page in range(1, 24):
            params = {
                'searchQueryState': '{"pagination":{"currentPage:"%s},"mapBounds":{"west":-74.4009301328125,"east":-73.5549828671875,"south":40.45924069713026,"north":40.951655440557104},"regionSelection":[{"regionId":6181,"regionType":6}],"isMapVisible":false,"filterState":{"sort":{"value":"globalrelevanceex"}},"isListVisible":True}' % page}
            res = self.fetch(
                'https://www.realtor.com/realestateandhomes-search/Kanawha-County_WV', params)
            # html=self.load_response()
            self.parse(res.text)

        self.to_csv()


if __name__ == '__main__':
    scraper = realtorscraper()
    scraper.run()
