import ccxt

from mktProfile import MarketProfile

'''
An example on how to use this script.
Here, we are retrieving 1 minute ohlcv data from Bittrex. 
'''

# Initialize Exchange
bittrex = ccxt.bittrex()
bittrex.load_markets(reload=True)

# Define Symbol
symbol = 'BTC/USDT'

# Fetch Ohlcv data
ohlcv = bittrex.fetch_ohlcv(symbol, "1m")
period = 6 * 60 * 60 * 1000

# Create an object of MarketProfile
mktPfl = MarketProfile(ohlcv_list=ohlcv, duration=period)
mktPfl.prepare_ohlcv()

# Build the profile
df = mktPfl.create_profile()

print(df)
df.to_csv("BTCUSDT.csv")
