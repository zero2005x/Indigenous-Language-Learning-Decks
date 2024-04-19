# 台灣原住民語言Anki牌組生成器
# Taiwan Indigenous Language Anki Deck Generator

這個專案旨在根據台灣原住民族語言的詞彙表，自動生成對應的Anki學習牌組。使用者可以選擇特定的方言，程式會下載對應的Excel詞彙表和音頻文件，並基於這些資源創建一個Anki牌組（.apkg文件）供使用者下載。

This project aims to automatically generate corresponding Anki learning decks based on the vocabulary lists of Taiwanese indigenous languages. Users can choose a specific dialect, and the program will download the corresponding Excel vocabulary list and audio files to create an Anki deck (.apkg file) for users to download.

## 功能特點
- 支持多種台灣原住民族語言方言
- 自動下載詞彙表Excel文件和對應的音頻文件
- 根據詞彙表和音頻文件生成Anki學習牌組
- 牌組包含原住民語言單詞、中文翻譯以及音頻發音
- 生成的牌組文件可直接導入Anki進行學習

## Features
- Supports various dialects of Taiwanese indigenous languages
- Automatically downloads vocabulary list Excel files and corresponding audio files
- Generates Anki learning decks based on vocabulary lists and audio files
- Decks include indigenous language words, Chinese translations, and audio pronunciations
- Generated deck files can be directly imported into Anki for learning

## 使用說明
- 確保您已安裝了必要的Python庫：requests、pandas、genanki。
- 在程式的Step 1部分，輸入您想要生成牌組的方言ID。方言ID與名稱的對照表已提供在程式中。
- 運行程式，等待其自動下載詞彙表和音頻文件並生成Anki牌組。
- 生成的.apkg文件將保存在您的Google Colab環境中，您可以直接下載該文件。
- 將下載的.apkg文件導入您的Anki應用程式，即可開始學習原住民語言詞彙。

## Instructions
- Ensure that you have installed the necessary Python libraries: requests, pandas, genanki.
- In the Step 1 part of the program, enter the dialect ID for which you want to generate the deck. The mapping table of dialect IDs and names is provided in the program.
- Run the program and wait for it to automatically download the vocabulary list and audio files and generate the Anki deck.
- The generated .apkg file will be saved in your Google Colab environment, and you can directly download the file.
- Import the downloaded .apkg file into your Anki application to start learning indigenous language vocabulary.

## 注意事項
- 確保您有穩定的網絡連接，以便程式能夠成功下載詞彙表和音頻文件。
- 生成的Anki牌組僅供個人學習使用，不得用於商業用途。
- 音頻文件的版權歸原所有者所有，請尊重知識產權。

## Notes
- Ensure that you have a stable internet connection for the program to successfully download the vocabulary list and audio files.
- The generated Anki decks are for personal learning use only and should not be used for commercial purposes.
- The copyright of the audio files belongs to the original owners. Please respect intellectual property rights.

## 貢獻
如果您對這個專案有任何改進或建議，歡迎提出Issue或提交Pull Request。

## Contribution
If you have any improvements or suggestions for this project, please feel free to raise an Issue or submit a Pull Request.

## 許可證
本專案採用MIT許可證。詳情請參閱LICENSE文件。

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
