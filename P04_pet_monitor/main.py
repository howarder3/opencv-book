import cv2
import time
import requests
from ultralytics import YOLO

# YOLO COCO 資料集中，cat=15、dog=16（0-indexed）
PET_CLASSES = {15: "cat", 16: "dog"}
CONFIDENCE = 0.5
# 兩次警報之間的最短間隔（秒），避免連續發送通知
ALERT_COOLDOWN = 10.0
# 填入 Telegram Bot Token 和 Chat ID
TELEGRAM_TOKEN = None
TELEGRAM_CHAT_ID = None


def get_forbidden_zone(cap):
    # 讀取第一幀畫面，讓使用者用滑鼠框選禁區範圍
    ret, frame = cap.read()
    if not ret:
        print("無法讀取攝影機畫面")
        return None
    print("請在彈出的視窗中用滑鼠框選禁區範圍")
    print("按 Enter 確認選區，按 c 取消")
    r = cv2.selectROI("Select Forbidden Zone", frame,
                      fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select Forbidden Zone")
    if r == (0, 0, 0, 0):
        print("未選取區域，程式結束")
        return None
    # selectROI 回傳 (x, y, w, h)，轉為 (x1, y1, x2, y2)
    x, y, w, h = r
    roi = (x, y, x + w, y + h)
    print(f"禁區範圍: {roi}")
    return roi


def send_telegram_alert(frame, message):
    # Token 未設定時 fallback 到 console，方便開發測試
    if TELEGRAM_TOKEN is None or TELEGRAM_CHAT_ID is None:
        print(message)
        return
    # 先存成本機截圖，再上傳到 Telegram
    path = f"alert_{time.time():.0f}.jpg"
    cv2.imwrite(path, frame)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(path, "rb") as f:
        requests.post(url,
                      data={"chat_id": TELEGRAM_CHAT_ID, "caption": message},
                      files={"photo": f})


def check_intrusion(box, roi):
    x1, y1, x2, y2 = map(int, box)
    rx1, ry1, rx2, ry2 = roi
    # AABB 碰撞：四種「完全不重疊」條件只要有一個成立就不入侵，反轉得到重疊
    return not (x2 < rx1 or x1 > rx2 or y2 < ry1 or y1 > ry2)


def draw_pet(frame, box, roi):
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cls_name = PET_CLASSES.get(int(box.cls[0]), "pet")
    intruding = check_intrusion(box.xyxy[0], roi)
    # 入侵禁區顯示紅色，安全區域顯示綠色
    color = (0, 0, 255) if intruding else (0, 255, 0)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, cls_name, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return intruding


def monitor_pets(cap, model, roi):
    last_alert = 0.0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 只偵測貓和狗，過濾其他類別以減少誤報
        results = model(frame, classes=list(PET_CLASSES.keys()),
                        conf=CONFIDENCE, verbose=False)

        # 在畫面上繪製禁區邊框（紅色）
        rx1, ry1, rx2, ry2 = roi
        cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)

        if results[0].boxes is not None:
            for box in results[0].boxes:
                intruding = draw_pet(frame, box, roi)
                # 入侵且冷卻時間已過，才發送截圖警報
                if intruding and time.time() - last_alert > ALERT_COOLDOWN:
                    now = time.time()
                    send_telegram_alert(
                        frame,
                        f"寵物進入警戒區域！時間：{time.strftime('%H:%M:%S')}"
                    )
                    last_alert = now

        cv2.imshow("Pet Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    print("=== Pet Monitor ===")
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("../sample/video/kitchen_cat.mp4")  # 影片測試
    roi = get_forbidden_zone(cap)
    if roi is None:
        cap.release()
        return
    monitor_pets(cap, model, roi)


if __name__ == "__main__":
    main()
