# NAVIO

把NAVIO電子目錄轉換成一頁式的HTML網頁。

## Usage

### Config
1. 進入NAVIOイベント網頁，要先「入室する」後才能抓到cookies。
2. 打開F12 > 應用程式 > 儲存空間 > Cookie > https://www.b2-web-pamphlet.jp/ 。

以下config內容以 **HARU COMIC CITY 34** 為例。

```json
{
  "event_name": "haru34",
  "pages": {
    "start": 1,
    "end": 225
  },
  "cookies": {
    "name": "B2_WEBPAMPHLET_HARU34",
    "value": "nofdzzwxc33ylfdfnjtnehpbs2qqr6so"
  }
}
```

### Run
```python
python main.py
```

跑完後會產生 *html/index.html*。
