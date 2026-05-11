# 動手做 OpenCV！— 範例程式碼

《**動手做 OpenCV！Python 影像處理 × AI 視覺辨識 × 5 大生活實戰專案**》
（旗標科技，2026）

## 資料夾架構

```
opencv-book-code/
├── ch00-建置 OpenCV 開發環境.ipynb
├── ch01-OpenCV 影像讀取顯示與儲存.ipynb
├── ch02-數位影像的基礎.ipynb
├── ...
├── ch23-OpenCV 物件追蹤.ipynb
├── P01_dino_cv_auto/        # 專案 01：讓電腦自己玩 Chrome 小恐龍
├── P02_auto_2048_solver/    # 專案 02：讓電腦自動破關 2048
├── P03_face_door/           # 專案 03：自製智慧人臉門禁
├── P04_pet_monitor/         # 專案 04：自製智慧寵物攝影機
├── P05_mini_photoshop/      # 專案 05：自製迷你修圖軟體
├── sample/                  # 全書共用範例影像素材
└── opencv_tools.py          # 全書通用影像顯示工具模組
```

## 開發環境

完整安裝步驟請參閱書中第 0、1 章。

簡要流程：

```bash
# 建立獨立 Python 環境（建議用 Anaconda）
conda create -n opencv-book python=3.11
conda activate opencv-book

# 安裝核心套件
pip install opencv-python numpy matplotlib jupyterlab

# 後半段 AI 章節用到的另建環境
conda create -n opencv-book-ai python=3.11
conda activate opencv-book-ai
pip install opencv-contrib-python ultralytics
```

## 預訓練模型下載

書的後半段（Ch19–23、P03、P04）會用到 Haar Cascade、SSD、YuNet、SFace、YOLOv8 等預訓練模型。**模型檔案沒打包進 repo**（檔案較大、各自有授權條款）。

每個會用到模型的章節，內文都附了下載連結，也提供「模型下載 Notebook」（檔名格式 `chXX-XXXX_模型下載.ipynb`）直接執行即可。

## 授權與使用提醒

- 範例檔內的軟體、模型與素材皆屬原作者所有，僅提供本書讀者學習練習用
- 其他用途請依各個工具或模型本身的授權條款處理
- **特別提醒**：書中的自動化遊戲專案（P01、P02）僅供技術學習示範，若將相關技術應用至其他遊戲（線上、手機等），可能違反該遊戲服務條款而導致帳號被封鎖等後果，相關責任請讀者自行承擔

## 作者

翁健豪（嗡嗡，Howard Weng）

- 個人網站：[wongwongnotes.com](https://wongwongnotes.com/)
- 書籍專頁（範例下載、勘誤、留言）：[wongwongnotes.com/opencv-book/](https://wongwongnotes.com/opencv-book/)
- Email：howarder3 [at] gmail.com
