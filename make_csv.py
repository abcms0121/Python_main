from backports import csv
import pandas as pd
from pandas import DataFrame

def store_to_csv_pandas(store_infos):
    data = []
    for e in store_infos:
        temp_name = None
        temp_branch = None
        temp_address = None
        temp_phone_num = None
        if type(e.getName()) is not str:
            temp_name = e.getName().decode('euc-kr')
        else:
            temp_name = e.getName()
        if type(e.getName()) is not str:
            temp_branch = e.getBranch().decode('euc-kr')
        else:
            temp_branch = e.getBranch
        if type(e.getAddress()) is not str:
            temp_address = e.getAddress().decode('euc-kr')
        else:
            temp_address = e.getAddress()
        if type(e.getName()) is not str:
            temp_phone_num = e.getPhoneNum().decode('euc-kr')
        else:
            temp_phone_num = e.getPhoneNum()
        data.append([temp_name, temp_branch, temp_address, temp_phone_num])
    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv("./store.csv", mode='a', encoding='euc-kr', header=False, index=False)

def store_to_csv(store_infos):
    f = open('./store.csv', 'a', encoding='euc-kr')
    csvWriter = csv.writer(f)

    for e in store_infos:
        temp_name = None
        temp_branch = None
        temp_address = None
        temp_phone_num = None
        if type(e.getName()) is not str:
            temp_name = e.getName().decode('euc-kr')
        else:
            temp_name = e.getName()
        if type(e.getName()) is not str:
            temp_branch = e.getBranch().decode('euc-kr')
        else:
            temp_branch = e.getBranch
        if type(e.getAddress()) is not str:
            temp_address = e.getAddress().decode('euc-kr')
        else:
            temp_address = e.getAddress()
        if type(e.getName()) is not str:
            temp_phone_num = e.getPhoneNum().decode('euc-kr')
        else:
            temp_phone_num = e.getPhoneNum()

        csvWriter.writerow(
            [
                temp_name,
                temp_branch,
                temp_address,
                temp_phone_num
            ]
        )

    f.close()