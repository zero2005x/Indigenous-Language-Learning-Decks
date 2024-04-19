

import requests
import pandas as pd
import os
import re
import genanki
from google.colab import files


# Step 1: 在這裡設定你所需要的方言別
# Step 1: Set the desired dialect here

# 讓使用者輸入方言ID來選擇方言，以下面的id = 3為例，這是選擇海岸阿美語
# Let the user input the dialect ID to choose the dialect. For example, id = 3 selects Coastal Amis.
user_input_id = 3 

# 方言ID與名稱的對照表
# Mapping table for dialect IDs and names
dialects_mapping = {
    1: "南勢阿美語",
    2: "秀姑巒阿美語",
    3: "海岸阿美語",
    4: "馬蘭阿美語",
    5: "恆春阿美語",
    6: "賽考利克泰雅語",
    7: "澤敖利泰雅語",
    8: "汶水泰雅語",
    9: "萬大泰雅語",
    10: "四季泰雅語",
    11: "宜蘭澤敖利泰雅語",
    13: "賽夏語",
    14: "邵語",
    15: "都達賽德克語",
    16: "德固達雅賽德克語",
    17: "德鹿谷賽德克語",
    18: "卓群布農語",
    19: "卡群布農語",
    20: "丹群布農語",
    21: "巒群布農語",
    22: "郡群布農語",
    23: "東排灣語",
    24: "北排灣語",
    25: "中排灣語",
    26: "南排灣語",
    27: "東魯凱語",
    28: "霧台魯凱語",
    29: "大武魯凱語",
    30: "多納魯凱語",
    31: "茂林魯凱語",
    32: "萬山魯凱語",
    33: "太魯閣語",
    34: "噶瑪蘭語",
    36: "卡那卡那富語",
    37: "拉阿魯哇語",
    38: "南王卑南語",
    39: "知本卑南語",
    40: "西群卑南語",
    41: "建和卑南語",
    42: "雅美語",
    43: "撒奇萊雅語"
}



user_input_dialect = dialects_mapping.get(user_input_id, None)

if user_input_dialect is None:
    print("輸入的ID無效，請重新輸入一個有效的方言ID。")
    print("The entered ID is invalid. Please re-enter a valid dialect ID.")
    exit()

print(f"選擇的方言是: {user_input_dialect}")
print(f"The selected dialect is: {user_input_dialect}")

# 基礎URL設定
# Base URL settings
base_audio_urls = r'https://ilrdc.tw/tow/2022/audio/word/'
base_excel_url = r'https://glossary-api.ilrdf.org.tw/glossary_2022/excel/2022學習詞表-'
base_excel_path = r'2022學習詞表-'
base_apkg_file_name = r'_deck_2022.apkg'

# 下載Excel文件
# Download the Excel file
excel_url = f'{base_excel_url}{user_input_id:02d}{user_input_dialect}.xlsx'
response = requests.get(excel_url)
excel_path = f'/content/{base_excel_path}{user_input_id:02d}{user_input_dialect}.xlsx'
with open(excel_path, 'wb') as f:
    f.write(response.content)
print("Excel file downloaded successfully.")


# Step 2: Analyzing the Excel File
# 步驟2：分析Excel文件

# 讀取並顯示Excel文件的前幾行
# Read and display the first few rows of the Excel file
data = pd.read_excel(excel_path, header=1)  # Adjust header to align with actual data start

data.dropna(how='all', inplace=True) # 去除全為空的行和列
# Remove rows and columns that are all empty

print(data.head())  # Display the first few rows of the dataframe


# Step 2-1:
# 步驟2-1：
# Find the start of the data after the header
# 找到標題後的數據開始位置
data_start_row = data.index[data.iloc[:, 0] == '序號'].tolist()[0]
data.columns = data.iloc[data_start_row]  # Set the correct headers
data = data[data_start_row+1:]  # Skip the headers
data.reset_index(drop=True, inplace=True)

# Keep only rows where the first cell is a number
# 只保留第一個單元格為數字的行
filtered_data = data[pd.to_numeric(data['序號'], errors='coerce').notnull()]

# 儲存修改後的 Excel 檔案
# Save the modified Excel file
filtered_data.to_excel(excel_path, index=False)

# Adjust column names based on the actual headers from the dataframe
# 根據數據框中的實際標題調整列名

# 確保「族語」和「中文」列有正確的資料
# Ensure the "Tribe Language" and "Chinese" columns have the correct data
words = data['族語'].dropna().tolist()
translations = data['中文'].dropna().tolist()
sequence = data['編號'].dropna().tolist()

# 過濾掉任何未能正確對應音檔名的項目
# Filter out any items that do not match the audio file name correctly
valid_indices = [i for i, val in enumerate(words) if not pd.isnull(val) and not pd.isnull(translations[i])]
valid_filenames = [f"{seq.replace('-', '_')}.wav" for i, seq in enumerate(data['編號'].tolist()) if i in valid_indices]

# 更新對應音檔名的列表
# Update the list of corresponding audio file names
audio_urls = [f"{base_audio_urls}{user_input_id}/{filename}" for filename in valid_filenames]



print("Excel data analyzed successfully.")

# Step 3: Downloading and Renaming Audio Files
# 步驟3：下載並重新命名音頻檔案

# 生成符合特定格式的音頻URLs
# Generate audio URLs that match a specific format

valid_filenames = []  # 用於保存有效的文件名
# Used to store valid file names
for seq in sequence:
    formatted_seq = seq.replace('-', '_')
    # 檢查格式是否為下列格式 01_01, 01_100,100_100 
    # Check if the format matches the following formats: 01_01, 01_100, 100_100
    if re.match(r'^\d{2}_\d{2}$', formatted_seq) or re.match(r'^\d{2}_\d{3}$', formatted_seq):
        audio_urls.append(f"{base_audio_urls}{user_input_id}/{formatted_seq}.wav")
        valid_filenames.append(formatted_seq + ".wav")  # 保存有效的文件名
        # Save valid file names
    else:
        print(f"Skipping download for invalid format: {formatted_seq}")

audio_folder = '/content/audio/'

# Create a directory for audio files
# 創建音頻文件的目錄
os.makedirs(audio_folder, exist_ok=True)
print("Audio folder created.")

# Download and rename audio files if they do not exist
# 如果音頻文件不存在，則下載並重新命名

for i, (url, filename) in enumerate(zip(audio_urls, valid_filenames)):
    new_filename = f"{user_input_dialect}_{valid_filenames[i]}"
    audio_file_path = os.path.join(audio_folder, new_filename)
    # If file does not exist, download and rename
    # 如果文件不存在，則下載並重新命名
    if not os.path.exists(audio_file_path):  
        try:
            response = requests.get(url)
            # Raise an error for bad status codes
            # 對於錯誤的狀態碼引發錯誤
            response.raise_for_status()  
            with open(audio_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded and renamed to {new_filename}")
        except requests.HTTPError as e:
            print(f"Failed to download {filename}: {e}")
    else:
        print(f"File {new_filename} already exists, skipping download.")



# Step 4: Creating an Anki Deck (apkg)
# 步驟4：創建Anki詞彙卡片包（apkg）

# Create an Anki deck
# 創建Anki牌組
my_deck = genanki.Deck(
    123756789,
    f'{user_input_dialect} Vocabulary 2022'
)

model = genanki.Model(
    1607392319,
    'Simple Model with Audio',
    fields=[
        {'name': 'Word'},
        {'name': 'Translation'},
        {'name': 'MyMedia'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Word}}<br>{{MyMedia}}',  # Show the word and play audio
            'afmt': '{{FrontSide}}<hr id="answer">{{Translation}}',  # Show the translation on the answer side
        },
    ],
    css='''
      .card {
       font-family: arial;
       font-size: 40px;
       text-align: center;
       color: black;
       background-color: white;
      }
    '''
)


# 收集所有聲音文件的完整路徑，同時檢查文件是否存在
# Collect the full paths of all audio files and check if the files exist
media_files = []
for filename in valid_filenames:
    full_path = os.path.join(audio_folder, f"{user_input_dialect}_{filename}")
    if os.path.exists(full_path):
        media_files.append(full_path)
    else:
        print(f"File {full_path} does not exist, skipping.")

# 創建 Anki 卡片，僅包含存在的音檔
# Create Anki cards, including only existing audio files
for word, translation, filename in zip(words, translations, valid_filenames):
    full_path = os.path.join(audio_folder, f"{user_input_dialect}_{filename}")
    if os.path.exists(full_path):
        # 確保 word 和 translation 是字符串類型
        # Ensure word and translation are string types       
        translation = str(translation) if pd.notnull(translation) else ""
        word = str(word) if pd.notnull(word) else ""
        if (translation != '無此詞彙') or (word != ""):
          my_note = genanki.Note(
              model=model,
              fields=[word, translation, f'[sound:{user_input_dialect}_{filename}]']
          )
          my_deck.add_note(my_note)
          print(f"Added card for {word}, {translation}, {user_input_dialect}_{filename}")
    
    else:
        print(f"Skipping card for {word} due to missing audio file: {filename}")

# 打包時包括聲音文件
# Include audio files when packaging
genanki_package = genanki.Package(my_deck)
genanki_package.media_files = media_files

# Save the Anki package with the new file name
# 使用新的檔案名稱儲存Anki套件
apkg_file_path = f'/content/{user_input_dialect}{base_apkg_file_name}'

try:
    genanki_package.write_to_file(apkg_file_path)
    print(f"Anki deck created and saved as {apkg_file_path}.")
    files.download(apkg_file_path)
except Exception as e:
    print(f"Failed to create Anki package: {e}")