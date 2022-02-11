# khò-ji̍t 課日

一個把台大課程網產生的預選課程清單轉成 .ics 格式，方便匯入 Google Calendar、Apple iCloud Calendar 等行事曆軟體的小工具

## 它可以做到...

- 自訂學期起始日（預設為 110-2 開學日）
- 自訂學期週數（預設 16 週）
- 上課節數不連貫時分拆行事曆行程
- 記錄上課地點、課號、授課教師
- 活動名稱即為課名，活動描述包括授課教師、課號及課程備註

功能非常簡陋，但對我來說夠用ㄌ。

## 它還不能...

- 檢查、清除衝堂課程
- 自定活動描述輸出格式
- 容許大部分非預期的輸入格式

## 使用它無比簡單

```shell
pip install -r requirements.txt
python3 main.py 課表檔案.csv [輸出檔名.ics]
```

其中，課表檔案暫時可以透過[複製課程網預選清單](https://nol.ntu.edu.tw/nol/coursesearch/myschedule.php)，貼上到試算表軟體後存為 CSV 格式產生，格式可以參考 [sample.csv](./sample.csv)。基本上把整個表格複製貼上格式就會是對的了。