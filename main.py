import threading
import time

import requests
import pandas as pd

coins_endpoint = "https://api.bybit.com/v2/public/symbols"
kline_endpoint = "https://api.bybit.com/v5/market/kline"

response = requests.get(coins_endpoint)
percentuali = []
start_time = time.time()
threads = []


def check_coin_percentuale(symbol):
    kline_endpoint_symbol = f'{kline_endpoint}?category=linear&interval=D&limit=5&symbol={symbol}'
    response_symbol = requests.get(kline_endpoint_symbol).json()
    candele = pd.DataFrame(response_symbol["result"]["list"])
    ultima_candela = candele.iloc[0]
    percentuale = ((float(ultima_candela[4]) - float(ultima_candela[1])) / float(ultima_candela[1])) * 100
    percentuali.append((symbol, percentuale))


data = response.json()

for dato in data['result']:
    symbol = dato['name']
    t = threading.Thread(target=check_coin_percentuale, args=[symbol], name=symbol)
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

percentuali_df = pd.DataFrame(percentuali, columns=['Nome', 'Percentuale'])

percentuali_df_sorted = percentuali_df.sort_values(by='Percentuale', ascending=False)

top_10 = percentuali_df_sorted.head(10)

bottom_10 = percentuali_df_sorted.tail(10)

print("Top 10:")
print(top_10[['Nome', 'Percentuale']].to_string(index=False))

print("\n")

print("Bottom 10:")
print(bottom_10[['Nome', 'Percentuale']].to_string(index=False))

end_time = time.time()
execution_time = end_time - start_time

print("\n")
print(f"Execution time: {execution_time} seconds")
