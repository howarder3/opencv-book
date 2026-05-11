import cv2
import numpy as np
import mss
import pyautogui
import keyboard


def get_user_roi(sct):
    print("請確保瀏覽器已開啟 Google Dino 遊戲 (chrome://dino)")
    print("程式將截取全螢幕，請在彈出的視窗中框選偵測區域")
    print("建議框選恐龍前方一段距離，高度涵蓋仙人掌的區域")
    input("確認目前的螢幕有包含恐龍畫面，按 Enter 進行截圖 ...")

    monitor_full = sct.monitors[1]
    full_screen = np.array(sct.grab(monitor_full))
    full_screen = cv2.cvtColor(full_screen, cv2.COLOR_BGRA2BGR)

    r = cv2.selectROI("Select ROI", full_screen, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")

    if r == (0, 0, 0, 0):
        print("未選取區域，程式結束")
        return None

    # 將 ROI 座標轉為 mss 螢幕格式，加上螢幕原點偏移
    monitor_roi = {
        "top": int(r[1] + monitor_full["top"]),
        "left": int(r[0] + monitor_full["left"]),
        "width": int(r[2]),
        "height": int(r[3])
    }
    print(f"偵測區域: {monitor_roi}")
    return monitor_roi


def process_frame(sct, monitor_roi, initial_blurred):
    JUMP_THRESHOLD = 500  # 差異像素數超過此值，判定為障礙物出現

    curr_img = np.array(sct.grab(monitor_roi))
    curr_gray = cv2.cvtColor(curr_img, cv2.COLOR_BGRA2GRAY)
    curr_blurred = cv2.GaussianBlur(curr_gray, (5, 5), 0)  # 模糊降噪，避免細微紋理觸發誤判

    diff = cv2.absdiff(curr_blurred, initial_blurred)  # 與初始背景比較，凸顯移動的障礙物
    _, binary = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  # 開運算去除雜訊小點

    diff_count = cv2.countNonZero(cleaned)
    should_jump = diff_count > JUMP_THRESHOLD

    # 疊加紅色遮罩顯示偵測到的變化區域
    display_img = cv2.cvtColor(curr_gray, cv2.COLOR_GRAY2BGR)
    display_img[cleaned > 0] = [0, 0, 255]
    return should_jump, display_img, diff_count


def zoom_preview(display_img, scale=5):
    # 偵測 ROI 很小，放大 5 倍方便觀察
    h, w = display_img.shape[:2]
    return cv2.resize(display_img, (w * scale, h * scale), interpolation=cv2.INTER_NEAREST)


def game_loop(sct, monitor_roi):
    print("捕捉初始背景，請確認偵測區域內沒有障礙物...")
    initial_img = np.array(sct.grab(monitor_roi))
    initial_gray = cv2.cvtColor(initial_img, cv2.COLOR_BGRA2GRAY)
    initial_blurred = cv2.GaussianBlur(initial_gray, (5, 5), 0)  # 鎖定乾淨背景作為比對基準
    print("背景鎖定完成，開始自動遊玩 (按 q 離開)")

    while True:
        should_jump, display_img, diff_count = process_frame(sct, monitor_roi, initial_blurred)

        if should_jump:
            pyautogui.press('space')
            print(f"[JUMP] 差異值: {diff_count}")

        zoomed = zoom_preview(display_img, scale=5)
        cv2.imshow("Dino Detector", zoomed)

        # 同時監聽 OpenCV 視窗按鍵與全域鍵盤，確保任一方式都能退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if keyboard.is_pressed('q'):
            break

    cv2.destroyAllWindows()


def main():
    print("=== Google Dino Auto Play ===")
    sct = mss.mss()
    monitor_roi = get_user_roi(sct)
    if monitor_roi:
        game_loop(sct, monitor_roi)

if __name__ == "__main__":
    main()
