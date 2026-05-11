# 動手做 OpenCV！— 範例程式碼

《**動手做 OpenCV！Python 影像處理 × AI 視覺辨識 × 5 大生活實戰專案**》（旗標科技，2026）的全書範例程式碼。

📚 **書籍專頁**（含勘誤、補充與留言交流）：[wongwongnotes.com/opencv-book/](https://wongwongnotes.com/opencv-book/)

---

## 章節列表

| 章 | 主題 | 對應 Jupyter Notebook |
|---|---|---|
| 第 0 章 | 建置 OpenCV 開發環境 | `ch00-建置 OpenCV 開發環境.ipynb` |
| 第 1 章 | OpenCV 影像讀取、顯示與儲存 | `ch01-OpenCV 影像讀取、顯示與儲存.ipynb` |
| 第 2 章 | 數位影像的基礎 | `ch02-數位影像的基礎.ipynb` |
| 第 3 章 | 認識 OpenCV 中的影像與色彩 | `ch03-認識 OpenCV 中的影像與色彩.ipynb` |
| 第 4 章 | OpenCV 影像變形處理 | `ch04-OpenCV 影像變形處理.ipynb` |
| 第 5 章 | OpenCV 影像繪製與標註 | `ch05-OpenCV 影像繪製與標註.ipynb` |
| 第 6 章 | OpenCV 影像數學運算 | `ch06-OpenCV 影像數學運算.ipynb` |
| 第 7 章 | OpenCV 影像模糊、銳化與馬賽克 | `ch07-OpenCV 影像模糊、銳化與馬賽克.ipynb` |
| 第 8 章 | OpenCV 影像色彩與光影調校 | `ch08-OpenCV 影像色彩與光影調校.ipynb` |
| 第 9 章 | OpenCV 影像二值化 | `ch09-OpenCV 影像二值化.ipynb` |
| 第 10 章 | OpenCV 形態學運算 | `ch10-OpenCV 形態學運算.ipynb` |
| 第 11 章 | OpenCV 邊緣偵測 | `ch11-OpenCV 邊緣偵測.ipynb` |
| 第 12 章 | OpenCV 輪廓分析 | `ch12-OpenCV 輪廓分析.ipynb` |
| 第 13 章 | OpenCV 影像分割 | `ch13-OpenCV 影像分割.ipynb` |
| 第 14 章 | OpenCV 模板匹配 | `ch14-OpenCV 模板匹配.ipynb` |
| 第 15 章 | OpenCV 特徵偵測與匹配 | `ch15-OpenCV 特徵偵測與匹配.ipynb` |
| 第 16 章 | OpenCV 視窗與使用者互動 | `ch16-OpenCV 視窗與使用者互動.ipynb` |
| 第 17 章 | OpenCV 影片處理 | `ch17-OpenCV 影片處理.ipynb` |
| 第 18 章 | OpenCV 攝影機即時影像分析 | `ch18-OpenCV 攝影機即時影像分析.ipynb` |
| 第 19 章 | 從「傳統影像處理」邁向「AI 影像辨識」的 OpenCV | （純概念章，無 Notebook） |
| 第 20 章 | OpenCV 人臉偵測 | `ch20-OpenCV 人臉偵測.ipynb` + `ch20-OpenCV 人臉偵測_模型下載.ipynb` |
| 第 21 章 | OpenCV 人臉辨識 | `ch21-OpenCV 人臉辨識.ipynb` + `ch21-OpenCV 人臉辨識_模型下載.ipynb` |
| 第 22 章 | OpenCV 物件偵測 | `ch22-OpenCV 物件偵測.ipynb` |
| 第 23 章 | OpenCV 物件追蹤 | `ch23-OpenCV 物件追蹤.ipynb` |

## 5 大生活實戰專案

| 專案 | 主題 | 資料夾 |
|---|---|---|
| 專案 01 | 讓電腦自己玩遊戲！挑戰 Chrome 小恐龍 | `P01_dino_cv_auto/` |
| 專案 02 | 當電腦學會「看懂」遊戲：自動玩 2048 | `P02_auto_2048_solver/` |
| 專案 03 | 刷臉就開門？自製居家智慧人臉門禁 | `P03_face_door/` |
| 專案 04 | 貓咪偷進廚房怎麼辦？自製智慧寵物攝影機 | `P04_pet_monitor/` |
| 專案 05 | 動手做自己的簡易版 Photoshop！ | `P05_mini_photoshop/` |

---

## 資料夾架構

```
opencv-book-code/
├── ch00-XXX.ipynb 到 ch23-XXX.ipynb  # 各章對應 Jupyter Notebook（部分純概念章節除外）
├── ch20-XXX_模型下載.ipynb            # 第 20 章預訓練模型下載工具
├── ch21-XXX_模型下載.ipynb            # 第 21 章預訓練模型下載工具
├── P01_dino_cv_auto/                  # 專案 01：讓電腦自己玩遊戲！挑戰 Chrome 小恐龍
├── P02_auto_2048_solver/              # 專案 02：當電腦學會「看懂」遊戲：自動玩 2048
├── P03_face_door/                     # 專案 03：刷臉就開門？自製居家智慧人臉門禁
├── P04_pet_monitor/                   # 專案 04：貓咪偷進廚房怎麼辦？自製智慧寵物攝影機
├── P05_mini_photoshop/                # 專案 05：動手做自己的簡易版 Photoshop！
├── sample/                            # 全書跨章節共用的範例影像 / 影片素材
└── opencv_tools.py                    # 第 1 章封裝、全書通用的影像顯示工具
```

---

## 開發環境

完整安裝步驟請參閱書中第 0 章與第 1 章。簡要流程：

```bash
# 建立獨立 Python 環境（建議用 Anaconda）
conda create -n opencv-book python=3.10
conda activate opencv-book

# 安裝核心套件
pip install opencv-python numpy matplotlib jupyterlab
```

後半段 AI 章節（第 19 章起）會用到 `opencv-contrib-python` 與 `Ultralytics YOLO` 套件，因為與前段環境有相依性衝突，建議另建獨立環境：

```bash
conda create -n opencv-book-ai python=3.10
conda activate opencv-book-ai
pip install opencv-contrib-python ultralytics
```

各章節開頭都會註明所需環境，相關步驟在書中也有完整說明。

---

## 預訓練模型下載

書的後半段（第 20–23 章、專案 03、專案 04）會用到 Haar Cascade、SSD、YuNet、SFace、YOLOv8 等預訓練模型。**模型檔案沒打包進範例檔中**，原因是檔案多半較大、各自有授權條款。

每個會用到模型的章節，書中內文都會附上對應的下載連結，讀者也可以直接執行範例檔提供的「**模型下載 Notebook**」（檔名格式 `chXX-XXXX_模型下載.ipynb`），就會把當章需要的模型一次抓好。

YOLOv8 weights（第 22、23 章與專案 04 用到）會由 `ultralytics` 套件自動下載，不需手動處理。

---

## 授權與使用提醒

- 範例檔內的軟體、模型與素材皆屬原作者所有，僅提供本書讀者學習練習用。其他用途請依各個工具或模型本身的授權條款處理。使用過程中若發生任何錯誤或損失，作者與出版商不負相關責任。

- **特別提醒**：書中的自動化遊戲專案（專案 01、02）僅供技術學習示範。若將相關技術應用至其他遊戲（線上、手機等各類遊戲），可能違反該遊戲的服務條款而導致帳號被封鎖等後果，相關責任請讀者自行承擔。

- 程式碼授權：MIT License（詳見 `LICENSE` 檔案）。

---

## 勘誤、提問與交流

如果在學習過程中發現任何錯字、程式碼錯誤、解釋不清楚的地方，或有問題想問，歡迎透過以下方式聯繫：

- **書籍專頁留言**：[wongwongnotes.com/opencv-book/](https://wongwongnotes.com/opencv-book/)（留言區登入 Disqus / Google / Facebook 即可發言）
- **Email**：[howarder3@gmail.com](mailto:howarder3@gmail.com)
- **GitHub Issues**：歡迎開 Issue 回報

如果用書裡學到的技術做出了自己的作品，超歡迎也回來分享 — 那會是這本書帶給筆者最大的成就感。

---

## 作者

**翁健豪（嗡嗡，Howard Weng）**

- 個人技術部落格：[wongwongnotes.com](https://wongwongnotes.com/)
- Email：[howarder3@gmail.com](mailto:howarder3@gmail.com)
