import argparse
import sys

import pandas as pd

sys.path.append('./mktProfile/')
from mktProfile import MarketProfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Market Profile. Output is a csv named profile.csv")
    parser.add_argument('csv', help='location of csv')
    parser.add_argument('duration', help='duration in milliseconds')
    parser.add_argument('--compact', help='Whether to save compact or standard profile(t or f)', choices=['t', 'f'])
    parser.add_argument('--dest', help='Destination to save profile to')

    args = parser.parse_args()

    location = args.csv
    duration = int(args.duration)
    compact = args.compact
    dest = args.dest

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
    if dest is None:
        dest = 'profile.csv'
    df.to_csv(dest)

    print('You profile is saved as', dest)
