#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import twstock
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the CSV file from the given URL
url = 'https://raw.githubusercontent.com/wenchiehlee/Python-Selenium-Action.TWSE-auction/main/2020-Now-utf8-filter.csv'

try:
    # Load the uploaded CSV file
    df = pd.read_csv(url, dtype={'證券代號': str})
    logging.info("CSV file loaded successfully.")
except Exception as e:
    logging.error(f"Error reading the CSV file: {e}")
    exit()

# Update stock codes in twstock
twstock.__update_codes()
logging.info(f"Number of stock codes loaded: {len(twstock.codes)}")

# Remove specified columns
columns_to_remove = [
    "發行市場", "發行性質", "競拍方式", "投標開始日", "投標結束日", "競拍數量(張)", "最低投標價格(元)",
    "最低每標單投標數量(張)", "最高投(得)標數量(張)", "保證金成數(%)", "每一投標單投標處理費(元)",
    "撥券日期(上市、上櫃日期)", "主辦券商", "得標總金額(元)", "得標手續費率(%)", "總合格件",
    "合格投標數量(張)", "最低得標價格(元)", "最高得標價格(元)", "得標加權平均價格(元)", "承銷價格(元)",
    "取消競價拍賣(流標或取消)"
]

df.drop(columns=columns_to_remove, inplace=True, errors='ignore')

# Add a new column "類別" with NaN as default value
df["類別"] = None

# Create a lookup dictionary from the provided table
lookup_table = {
    "6982": "汽車工業",
    "7704": "半導體業",
    "6885": "生技醫療業",
    "6997": "數位雲端",
    "6955": "生技醫療業",
    "8045": "光電業",
    "6996": "半導體業",
    "7722": "數位雲端",
    "6720": "半導體業",
    "6950": "資訊服務業",
    "6962": "半導體業",
    "7705": "觀光餐旅",
    "7708": "觀光餐旅",
    "7703": "其他電子業",
    "6988": "汽車工業",
    "2646": "航運業",
    "6862": "電子零組件業",
    "8272": "資訊服務業",
    "6919": "生技醫療業",
    "6913": "電子零組件業",
    "1294": "食品工業",
    "6967": "電子零組件業",
    "6923": "綠能環保",
    "4772": "化學工業",
    "2751": "觀光餐旅",
    "6969": "綠能環保",
    "6739": "其他電子業",
    "6958": "其他業",
    "6968": "居家生活",
    "6838": "生技醫療業",
    "7584": "文化創意業",
    "3150": "半導體業",
    "6957": "其他業",
    "6951": "綠能環保",
    "6637": "生技醫療業",
    "6952": "其他業",
    "6890": "運動休閒",
    "6903": "其他電子業",
    "6794": "生技醫療業",
    "6771": "綠能環保",
    "6881": "其他業"
}

# Update missing values in the DataFrame
for index, row in df.iterrows():
    stock_code = str(row['證券代號']).split('.')[0].strip()  # Ensuring no decimal point

    if stock_code in twstock.codes:
        stock_info = twstock.codes[stock_code]

        # Update stock name if missing
        if pd.isna(row['證券名稱']) or row['證券名稱'] == '':
            df.at[index, '證券名稱'] = stock_info.name
            #logging.info(f"Updated '證券名稱' for {stock_code}: {stock_info.name}")

        # Update stock category if missing
        if pd.isna(row['類別']) or row['類別'] == '':
            df.at[index, '類別'] = stock_info.group
            if stock_code in lookup_table:
                if lookup_table[stock_code] != stock_info.group:
                    logging.warning(f"{stock_code} {stock_info.group}!={lookup_table[stock_code]}")
    else:
        # Lookup the category using the lookup table
        if stock_code in lookup_table:
            df.at[index, '類別'] = lookup_table[stock_code]
        else:
            logging.warning(f"Stock code {stock_code} not found in twstock.codes.")

# Save the updated DataFrame
output_file = 'company.csv'
try:
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    logging.info(f"CSV file has been updated successfully as '{output_file}'.")
except Exception as e:
    logging.error(f"Error writing the CSV file: {e}")
