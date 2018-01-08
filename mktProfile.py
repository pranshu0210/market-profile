import math
import sys

import pandas as pd


class MarketProfile:
    def __init__(self, ohlcv_list, duration):
        '''
        Initialise a MarketProfile Object with a ohlcv list
        '''
        self.ohlcv_list = ohlcv_list
        self.duration = duration
        self.df = None
        self.low = 0
        self.high = 0

    def prepare_ohlcv(self):
        '''
        Prepares ohlcv into the desired list
        :return: 
        '''
        cur_timestamp = self.ohlcv_list[-1][0]
        ohlcv_selected = []
        for i in range(len(self.ohlcv_list) - 1, 0, -1):
            if cur_timestamp - self.ohlcv_list[i][0] >= self.duration:
                break
            else:
                ohlcv_selected.append(self.ohlcv_list[i])
        self.ohlcv_list = ohlcv_selected

    def create_profile(self):
        '''
        Creates the market profile
        :return: market profile in the form of a pandas Dataframe
        '''
        self.high, self.low = 0.0, sys.float_info.max
        my_list = []
        offset = math.ceil(len(self.ohlcv_list) / 26)

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
                mychar += 1
            for j in range(0, len(my_list)):
                for q in range(0, 4):
                    if abs(my_list[j][0] - self.ohlcv_list[i][q]) / my_list[j][0] * 100 < difference_threshold:
                        f[q] = 1
                        if f[q] != 2:
                            if my_list[j].count(chr(mychar)) == 0:
                                my_list[j].append(chr(mychar))
                            f[q] = f[q] + 1

            for q in range(0, 4):
                if f[q] <= 0:
                    my_list.append([self.ohlcv_list[i][1], chr(mychar)])

        length = len(my_list)
        i = 0

        my_list.sort(key=lambda x: x[0])
        while i < length - 1:
            if abs(my_list[i][0] - my_list[i + 1][0]) / my_list[i][0] * 100 < difference_threshold:
                del my_list[i + 1]
                length = length - 1
            else:
                i = i + 1

        for i in range(65, 92):
            f_idx = 0
            l_idx = 0
            append = 0
            for z in range(0, 2):
                if z == 0:
                    for j in range(0, len(my_list)):
                        for k in range(1, len(my_list[j])):
                            if my_list[j][k] == chr(i):
                                if f_idx == 0:
                                    f_idx = j
                                l_idx = j
                                break
                elif z == 1:
                    for j in range(f_idx + 1, l_idx):
                        if my_list[j].count(chr(i)) == 0:
                            for k in range(1, len(my_list[j])):
                                if my_list[j][k] > chr(i):
                                    my_list[j].insert(k, chr(i))
                                    append = 0
                                    break
                                append = 1
                            if append == 1:
                                my_list[j].append(chr(i))

        self.df = pd.DataFrame(my_list)
        return self.df

    def poc(self):
        columns = self.df.columns.values
        # new_df = self.df[self.df[columns[-1]].notnull()]
        rows = self.df.index[self.df[columns[-1]].notnull()].tolist()

        avg = [0] * 10  # stores the avg of all possible combinations of poc
        j = 0  # Index for avg
        k = [0] * 10  # Counter for number of consecutive rows
        avg_flag = 0  # flag to check where the last value came from
        i = 0
        while i < len(rows) - 1:
            if rows[i] + 1 == rows[i + 1]:  # If consecutive rows
                avg[j] += self.df.iloc[rows[i]][0]
                k[j] += 1
                avg_flag = 0
            else:  # If not
                avg[j] += self.df.iloc[rows[i]][0]
                k[j] += 1
                avg[j] /= k[j]
                j += 1
                avg_flag = 1
            i += 1

        if avg_flag == 1:
            j += 1
        avg[j] += self.df.iloc[rows[i]][0]
        k[j] += 1
        avg[j] /= k[j]

        poc = avg[k.index(max(k))]

        return poc

    def range(self):
        return self.low, self.high
