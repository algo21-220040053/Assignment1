import time
import requests
import json
import csv


class GetData:
    def __init__(self, start, end, file_name):
        self.start = self.time2stamp(start)
        self.end = self.time2stamp(end)
        self.name = file_name
        self.price_list = []

    @staticmethod
    def time2stamp(str_time):       # Transfer string time to time stamp
        time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        t_stamp = int(time.mktime(time_array))
        return t_stamp

    def crawler(self):      # Get btc historical data using api
        request_link = f"https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/" \
                       f"historical?convert=USD&slug=bitcoin&time_end={self.end}&time_start={self.start}"
        print("Request link: " + request_link)
        r = requests.get(url=request_link)
        content = json.loads(r.content)
        self.price_list = content['data']['quotes']

    def keep_data(self):        # Keep data in local
        with open(self.name, 'w', encoding='utf8', newline='') as f:
            csv_write = csv.writer(f)
            csv_head = ["Date", "Price", "Volume"]
            csv_write.writerow(csv_head)

            for quote in self.price_list:
                quote_date = quote["time_open"][:10]
                quote_price = "{:.2f}".format(quote["quote"]["USD"]["close"])
                quote_volume = "{:.2f}".format(quote["quote"]["USD"]["volume"])
                csv_write.writerow([quote_date, quote_price, quote_volume])
        print("Done")


if __name__ == '__main__':
    start_time = '2017-03-01 00:00:00'
    end_time = '2021-03-01 00:00:00'
    name = 'BTC.csv'
    get_btc = GetData(start_time, end_time, name)
    get_btc.crawler()
    get_btc.keep_data()