import ccxt

from mktProfile import MarketProfile

"""
An example on how to use this script.
Here, we are retrieving 1 minute ohlcv data from Bittrex. 
"""

# Initialize Exchange
bittrex = ccxt.bittrex()
bittrex.load_markets(reload=True)

# Define Symbol
symbol = 'BTC/USDT'

# Fetch Ohlcv data
ohlcv = bittrex.fetch_ohlcv(symbol, "1m")
period = 6 * 60 * 60 * 1000

# Create an object of MarketProfile
mktPfl = MarketProfile.init_market_profile_list(ohlcv_list=ohlcv, duration=period)
mktPfl.prepare_ohlcv()

# Build the profile
df = mktPfl.create_profile()

# Compact the profile
cmp_df = mktPfl.compact_profile()

# Calculate the poc
poc = mktPfl.poc()

# Get the range of prices
low, high = mktPfl.range()

# Write to csv
cmp_df.to_csv("BTCUSDT.csv")
