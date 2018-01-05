import ccxt

from mktProfile import MarketProfile

bittrex = ccxt.bittrex()
bittrex.load_markets(reload=True)

symbol = 'BTC/USDT'
ohlcv = bittrex.fetch_ohlcv(symbol, "1m")
period = 6 * 60 * 60 * 1000

mktPfl = MarketProfile(ohlcv_list=ohlcv, duration=period)
mktPfl.prepare_ohlcv()
df = mktPfl.create_profile()

print(df)
df.to_csv("BTCUSDT.csv")
