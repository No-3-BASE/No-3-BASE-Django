## No 3 BASE 第三號基地 遊戲論壇

#### 一點點摸魚

搜尋 cmd → 打開終端機

輸入 python → 確定環境

quit() → 離開python

輸入 mkdir 資料夾名稱(範例使用web) → 建立資料夾

輸入 cd  資料夾名稱 → 進入資料夾

輸入 py -m venv  資料夾名稱2(範例使用myworld) → 建立虛擬環境

輸入  資料夾名稱2\Scripts\activate.bat → 進入虛擬環境

(在虛擬環境)

輸入 python -m pip install Django → 安裝 Django

輸入 django-admin --version → 查看 Django 版本

( clone 檔案)

輸入 git clone https://github.com/No-3-BASE/No-3-BASE-Django.git → 從 git 下載

輸入 cd No-3-BASE-Django → 進入資料夾

(執行)

輸入 python manage.py runserver → 啟動 server

開啟 http://127.0.0.1:8000/player/signup → 前往註冊畫面

> 帳號和信箱都有綁唯一性、會發送驗證信

(超級帳號)

輸入 ctrl+c → 關閉執行

輸入 python manage.py migrate → 建立資料表

輸入 python manage.py createsuperuser → 建立超級帳號

輸入 python manage.py runserver → 啟動 server

開啟 http://127.0.0.1:8000/admin → 前往資料管理，可以刪除註冊過的資料
