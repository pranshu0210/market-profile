import argparse

import pandas as pd

from mktProfile import MarketProfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Market Profile. Output is a csv named profile.csv")
    parser.add_argument('csv', help='location of csv')
    parser.add_argument('duration', help='duration in milliseconds')
    parser.add_argument('--compact', help='Whether to save compact or standard profile(t or f)', choices=['t', 'f'])

    args = parser.parse_args()

    location = args.csv
    duration = int(args.duration)
    compact = args.compact

    ohlcv = pd.read_csv(location, usecols=['t', 'o', 'h', 'l', 'c'])

    # Create Market Profile Object
    mktProfileObj = MarketProfile.init_market_profile_df(ohlcv_df=ohlcv, duration=duration)
    mktProfileObj.prepare_ohlcv()

    # Generate Profile
    if compact is None or compact == 'f':
        df = mktProfileObj.create_profile()
    else:
        df = mktProfileObj.compact_profile()

    # Write to csv
    df.to_csv('profile.csv')

    print('You profile is saved as profile.csv')
