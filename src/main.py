#dependencies
import requests
import matplotlib.pyplot as plot
import json
import numpy as np
import sys
import os
import argparse

from genData import gen_main



#wrappers for main
def getUserCoin():
    while True:
        coin = input("Please enter cryptocurrency abbreviation (btc, eth, etc.): ").lower()
        temp = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin}")

        if temp.status_code == 200:
            return coin
        else:
            print("Invalid Coin. Please try again.")

def showGraph(data, coinName, title_mod='History'):
    xList = range(len(data), 0, -1)
    
    yList = data

    plot.plot(xList, yList)
    plot.title('Coin ' + title_mod + ' of ' + str(coinName).upper())
    plot.xlabel('Time')
    plot.ylabel('Price (USD)')
    plot.show()

def getData(coin, days):
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}'

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Unable to fetch data for {coin}. Status code: {response.status_code}")
        return []

    try:
        data = response.json()
        if 'prices' not in data:
            print("Error: Invalid API response format.")
            return []

        # Extract prices
        prices = [entry[1] for entry in data['prices']]
        return prices

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response.")
        return []
def generate_data(dataArray, seed):
    return gen_main(dataArray, seed)

#main
def main(): 
    # This program has data points from October 22, 2017 and before.
    # All predictions are from data from that point and before.
    # The program cannot factor in data points from 10/22/17 to present day

    #parse arguments
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--seed', help="seed to be used", type=int, default=123)
    args = p.parse_args()
    seed = args.seed

    print("prediction coins by Lachi Balabanski")
    coin = getUserCoin()

    try:
        time = int(input('From how long ago would you like to view data from?(days): '))

    except ValueError:
        print("Error while parsing previous input, will revert to default=31")
        time = 31
    
    print('\nLoading Data. . .', end='   ')
    data = getData(coin, time)
    print('[DONE]')

    print('\nGenerating Data. . .', end='   ')
    gen_data = generate_data(data, seed=seed)
    print('[DONE]')
    
    showGraph(data, coin)

    showGraph(gen_data, coin, title_mod='Prediction')


if __name__ == "__main__":
    main()
