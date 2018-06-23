import math
import sys

import pandas as pd


class MarketProfile:
    def __init__(self, ohlcv_list=None, ohlcv_df=None, duration=None):
        """
        Initialise a MarketProfile Object with a ohlcv list
        """
        self.ohlcv_list = ohlcv_list
        self.duration = duration
        self.ohlcv_df = ohlcv_df
        self.df = None
        self.low = 0
        self.high = 0
        self.cpt_market_profile = None
        self.my_list = None
        self.cmp_df = None
        self.u_step_df = None

        self.convert_to_list()

    @classmethod
    def init_market_profile_df(cls, ohlcv_df, duration):
        """
        Class method for when ohlcv is a Dataframe
        :param ohlcv_df: 
        :param duration: 
        :return: Market_Profile object
        """
        return cls(ohlcv_df=ohlcv_df, duration=duration)

    @classmethod
    def init_market_profile_list(cls, ohlcv_list, duration):
        """
        Class method for when ohlcv is a list
        :param ohlcv_list: 
        :param duration: 
        :return: Market_Profile object
        """
        return cls(ohlcv_list=ohlcv_list, duration=duration)

    def convert_to_list(self):
        """
        Convert input ohlc Dataframe to List
        :return: 
        """
        if self.ohlcv_df is None:
            pass
        else:
            cols = ['t', 'o', 'h', 'l', 'c']
            self.ohlcv_df = self.ohlcv_df[cols]  # reorder columns in the desired way
            self.ohlcv_list = self.ohlcv_df.values.tolist()  # convert df to list

    def prepare(self, ohlcv: list, duration: int):
        ohlcv.reverse()
        limit = ohlcv[0][0] - duration

        for ohlc in ohlcv:
            if ohlc[0] > limit:
                yield ohlc
            else:
                return  # Divide interval into 26 parts

    def prepare_ohlcv(self):
        """
        Prepares ohlcv into the desired list
        :return: 
        """
        self.ohlcv_list = list(self.prepare(self.ohlcv_list, self.duration))

    def create_profile(self, ones=False):
        """
        Creates the market profile
        :return: market profile in the form of a pandas Dataframe
        """
        self.high, self.low = 0.0, sys.float_info.max
        self.my_list = []

        cur_timestamp = self.ohlcv_list[-1][0]
        self.ohlcv_list.reverse()
        mychar = 65
        period = math.ceil(self.duration / 26)
        difference_threshold = 0.01

        for i in range(0, len(self.ohlcv_list)):
            f = [0] * 4
            if self.ohlcv_list[i][2] > self.high:
                self.high = self.ohlcv_list[i][2]
            if self.ohlcv_list[i][3] < self.low:
                self.low = self.ohlcv_list[i][3]
            if self.ohlcv_list[i][0] - cur_timestamp >= period:
                cur_timestamp = self.ohlcv_list[i][0]
                for j in range(0, len(self.my_list)):
                    if self.my_list[j][-1] != chr(mychar):  # If price does not exist for this interval
                        # Append 0 to the list
                        self.my_list[j].append(0)
                mychar += 1
            for j in range(0, len(self.my_list)):
                for q in range(0, 4):
                    if abs(self.my_list[j][0] - self.ohlcv_list[i][q + 1]) \
                            / self.my_list[j][0] * 100 < difference_threshold:
                        f[q] = 1
                        if self.my_list[j].count(chr(mychar)) == 0:
                            self.my_list[j].append(chr(mychar))

            for q in range(0, 4):
                if f[q] == 0:
                    similar_flag = 0
                    for m in range(1, q + 1):
                        if abs(self.ohlcv_list[i][q + 1] - self.ohlcv_list[i][m]) / self.ohlcv_list[i][
                                    q + 1] * 100 < difference_threshold:
                            similar_flag = 1
                    if similar_flag == 0:
                        self.my_list.append([self.ohlcv_list[i][q + 1]])
                        for char_ter in range(65, mychar):
                            self.my_list[-1].append(0)
                        self.my_list[-1].append(chr(mychar))

        for j in range(0, len(self.my_list)):
            if self.my_list[j][-1] != chr(mychar):  # If price does not exist for this interval
                # Append 0 to the list
                self.my_list[j].append(0)

        # Sort the list based on price
        self.my_list.sort(key=lambda x: x[0])

        mychar = 65
        # Fill in empty cell belonging to the same interval
        for j in range(1, len(self.my_list[0])):
            first_idx = -1
            last_idx = 0

            for i in range(0, len(self.my_list)):
                if self.my_list[i][j] == chr(mychar):
                    if first_idx == -1:
                        first_idx = i
                    last_idx = i

            for i in range(first_idx, last_idx):
                if self.my_list[i][j] != chr(mychar):
                    self.my_list[i][j] = chr(mychar)

            mychar += 1

        self.df = pd.DataFrame(self.my_list)
        if ones is True:
            self.df = self.df.replace('[A-Z]', 1, regex=True)
        return self.df

    def compact_profile(self, new_df=None):
        """
        Compacts the standard market profile
        :return: 
        """
        uncmpt_list = []
        if new_df is None:
            uncmpt_df = self.df
            if uncmpt_df is None:  # Create profile if not already created
                self.create_profile()
            uncmpt_list = self.my_list
        else:
            uncmpt_list = new_df.values.tolist()

        cmp_list = []
        for row in uncmpt_list:
            cmp_list.append(list(filter(lambda a: a != 0, row)))
        self.cmp_df = pd.DataFrame(cmp_list)
        return self.cmp_df

    def poc(self):
        """
        Calculates the poc and returns it
        :return: poc
        """
        if self.cmp_df is None:
            self.compact_profile()
        columns = self.cmp_df.columns.values
        # new_df = self.df[self.df[columns[-1]].notnull()]
        rows = self.cmp_df.index[self.df[columns[-1]].notnull()].tolist()

        avg = [0] * 10  # stores the avg of all possible combinations of poc
        j = 0  # Index for avg
        k = [0] * 10  # Counter for number of consecutive rows
        avg_flag = 0  # flag to check where the last value came from
        i = 0
        while i < len(rows) - 1:
            if rows[i] + 1 == rows[i + 1]:  # If consecutive rows
                avg[j] += self.cmp_df.iloc[rows[i]][0]
                k[j] += 1
                avg_flag = 0
            else:  # If not
                avg[j] += self.cmp_df.iloc[rows[i]][0]
                k[j] += 1
                avg[j] /= k[j]
                j += 1
                avg_flag = 1
            i += 1

        if avg_flag == 1:
            j += 1
        avg[j] += self.cmp_df.iloc[rows[i]][0]
        k[j] += 1
        avg[j] /= k[j]

        poc = avg[k.index(max(k))]

        return poc

    def range(self):
        """
        Calculates the range and returns
        :return: rangeLow, rangeHigh
        """
        if self.df is None:
            self.create_profile()
        return self.low, self.high

    def reduce_profile(self, n_r, compact=False):
        """
        Reduces the profile to the given number of rows
        :param n_r: number of rows to reduce the profile to
        :return:
        """
        n_r = n_r - 1  # To account for the fact that the starting and ending prices will also be included
        price_range = self.range()  # Get the range
        step = (price_range[1] - price_range[0]) / n_r

        # Store the prices in the form of steps
        price_list = [i * step + price_range[0] for i in range(0, n_r + 1)]

        # Get the actual list of prices from dataframe
        price_list_actual = self.df.ix[:, 0].tolist()

        # Find the indices closest rows
        price_idx = []
        for j in range(0, len(price_list)):
            price_idx.append(
                min(range(len(price_list_actual)), key=lambda i: abs(price_list_actual[i] - price_list[j])))

        # Get the rows only associated with indices in price_idx
        self.u_step_df = self.df.iloc[price_idx, :]

        # Replace first column with price list
        self.u_step_df[0] = price_list

        # Reorder the indices
        self.u_step_df.index = range(len(price_list))
        # Reverse the dataframe
        self.u_step_df = self.u_step_df.iloc[::-1]
        self.u_step_df.index = range(len(price_list))
        if compact:
            return self.compact_profile(new_df=self.u_step_df)
        return self.u_step_df
