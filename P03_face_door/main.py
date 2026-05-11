import cv2
import numpy as np
import os
import time
import requests

YUNET_PATH = "face_detection_yunet_2023mar.onnx"
SFACE_PATH = "face_recognition_sface_2021dec.onnx"
DATABASE_PATH = "faces"  # 人臉資料庫目錄，子目錄名稱即為人名
THRESHOLD = 0.363  # SFace 餘弦相似度門檻，高於此值才視為同一人
# 兩次通知之間的最短間隔（秒），避免同一人連續觸發
ALERT_COOLDOWN = 30.0
# 填入 Telegram Bot Token 和 Chat ID
TELEGRAM_TOKEN = "你的Token"
TELEGRAM_CHAT_ID = "你的ChatID"

def send_telegram_alert(message):
    # Token 未設定時 fallback 到 console，方便開發測試
    if TELEGRAM_TOKEN is None or TELEGRAM_CHAT_ID is None:
        print(message)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)


def detect_faces(img, detector):
    h, w = img.shape[:2]
    detector.setInputSize((w, h))  # 每次偵測前需同步圖片尺寸
    _, faces = detector.detect(img)
    return faces


def extract_feature(img, face, recognizer):
    # 對齊裁切後提取 128 維特徵向量
    aligned = recognizer.alignCrop(img, face)
    return recognizer.feature(aligned)


def build_database(detector, recognizer):
    # 掃描 faces/ 目錄，每個子目錄為一個人，取所有照片特徵的平均值
    database = {}
    for name in os.listdir(DATABASE_PATH):
        folder = os.path.join(DATABASE_PATH, name)
        if not os.path.isdir(folder):
            continue
        features = []
        for fname in os.listdir(folder):
            img = cv2.imread(os.path.join(folder, fname))
            if img is None:
                continue
            faces = detect_faces(img, detector)
            if faces is not None:
                features.append(extract_feature(img, faces[0], recognizer))
        if features:
            database[name] = np.mean(features, axis=0)  # 多張照片取平均，提升辨識穩定性
    return database


def recognize_face(feature, database, recognizer):
    best_name, best_score = "Unknown", 0.0
    for name, db_feature in database.items():
        score = recognizer.match(
            feature, db_feature, 0  # 0 = 餘弦相似度比對
        )
        if score > best_score:
            best_score, best_name = score, name
    if best_score >= THRESHOLD:
        return best_name, best_score
    return "Unknown", best_score


def check_access(name, log_path="access_log.txt"):
    allowed = name != "Unknown"
    status = "ALLOWED" if allowed else "DENIED"
    # 每次辨識結果都記錄到 access_log.txt，附帶時間戳
    with open(log_path, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {name} | {status}\n")
    return allowed


def draw_result(frame, face, name, score, allowed):
    x, y, w, h = face[:4].astype(int)
    color = (0, 255, 0) if allowed else (0, 0, 255)  # 通過綠色，拒絕紅色
    label = f"{name} ({score:.2f})"
    status_text = "ALLOWED" if allowed else "DENIED"
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    cv2.putText(frame, label, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, status_text, (x, y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


def run_door_access(cap, detector, recognizer, database):
    last_alert = 0.0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = detect_faces(frame, detector)
        if faces is not None:
            for face in faces:
                feature = extract_feature(frame, face, recognizer)
                name, score = recognize_face(feature, database, recognizer)
                allowed = check_access(name)
                draw_result(frame, face, name, score, allowed)
                # 冷卻時間已過才發送 Telegram 通知（ALLOWED 和 DENIED 都通知）
                if time.time() - last_alert > ALERT_COOLDOWN:
                    status = "已通過門禁" if allowed else "被拒絕進入"
                    send_telegram_alert(
                        f"{name} {status}！時間：{time.strftime('%H:%M:%S')}"
                    )
                    last_alert = time.time()
        cv2.imshow("Face Door Access", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    print("=== Face Door Access ===")
    detector = cv2.FaceDetectorYN.create(YUNET_PATH, "", (320, 320), score_threshold=0.7)
    recognizer = cv2.FaceRecognizerSF.create(SFACE_PATH, "")
    database = build_database(detector, recognizer)
    print(f"資料庫載入完成，共 {len(database)} 人")
    cap = cv2.VideoCapture(0)
    run_door_access(cap, detector, recognizer, database)


if __name__ == "__main__":
    main()
