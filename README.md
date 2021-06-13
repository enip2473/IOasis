# IOasis

## Web

## Discord_bot

使用方法：裝完 requirements.txt 後運行 main.py

```
pip install -r requirements.txt
python main.py
```

途中可能會遇到有關 wheel 的問題，把問題複製起來丟 stack overflow 就解決了

- cf.py
  - 負責與 cf 的 api 溝通的地方
  - 跟 cf 要資料的功能通常都在那裡

- cf_cog.py
  - discord 關於 cf 的指令們
  - 如註冊、發起挑戰等

- userdata.py
  - 負責與資料庫溝通的地方
  - 對資料庫進行操作 / 查詢會在這裡 