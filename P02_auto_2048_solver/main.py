import cv2
import numpy as np
import mss
import pyautogui
import os
import time


# ── 遊戲邏輯 ──

def compress(grid):
    # 將每一行的非零數字往左推，消除中間的空格
    new_grid = np.zeros((4, 4), dtype=int)
    for i in range(4):
        pos = 0
        for j in range(4):
            if grid[i][j] != 0:
                new_grid[i][pos] = grid[i][j]
                pos += 1
    return new_grid


def merge(grid):
    # 從左到右掃描，相鄰相同的數字合併（左邊加倍、右邊歸零），並累計得分
    score = 0
    for i in range(4):
        for j in range(3):
            if grid[i][j] != 0 and grid[i][j] == grid[i][j + 1]:
                grid[i][j] *= 2
                score += grid[i][j]
                grid[i][j + 1] = 0
    return grid, score


def move_left(grid):
    # 向左移動：壓縮 → 合併 → 再壓縮（處理合併後產生的新空格）
    temp = compress(grid)
    temp, score = merge(temp)
    return compress(temp), score


def move_right(grid):
    # 向右移動：左右翻轉後執行 move_left，再翻轉回來
    temp, score = move_left(np.fliplr(grid))
    return np.fliplr(temp), score


def move_up(grid):
    # 向上移動：轉置後執行 move_left，再轉置回來
    temp, score = move_left(grid.T)
    return temp.T, score


def move_down(grid):
    # 向下移動：轉置後執行 move_right，再轉置回來
    temp, score = move_right(grid.T)
    return temp.T, score


MOVE_FUNCS = [move_up, move_down, move_left, move_right]
MOVE_KEYS = ["up", "down", "left", "right"]


def get_available_moves(grid):
    # 嘗試四個方向，只回傳移動後棋盤確實發生變化的方向
    moves = []
    for i, func in enumerate(MOVE_FUNCS):
        new_grid, _ = func(grid.copy())
        if not np.array_equal(grid, new_grid):
            moves.append(i)
    return moves


# ── AI 策略 ──

def evaluate(grid):
    # 評估盤面分數：空格數（×10）+ 最大磁磚值 + 最大磁磚在角落的額外獎勵
    empty_count = np.count_nonzero(grid == 0)
    max_tile = np.max(grid)
    corners = [grid[0][0], grid[0][3], grid[3][0], grid[3][3]]
    corner_bonus = max_tile if max_tile in corners else 0
    return empty_count * 10 + max_tile + corner_bonus


def best_move(grid):
    # 貪婪策略：嘗試每個可用方向，選出合併得分 + 盤面評估分數最高的那一步
    best_score, best_dir = -1, None
    for i in get_available_moves(grid):
        new_grid, merge_score = MOVE_FUNCS[i](grid.copy())
        score = merge_score + evaluate(new_grid)
        if score > best_score:
            best_score = score
            best_dir = i
    return best_dir


# ── 模板辨識 ──

def load_templates(template_dir):
    # 載入 assets/ 中所有純數字命名的圖片，以數字值為 key 存入字典
    templates = {}
    for filename in sorted(os.listdir(template_dir)):
        name = filename.split(".")[0]
        if not name.isdigit():
            continue
        img = cv2.imread(os.path.join(template_dir, filename))
        if img is not None:
            templates[int(name)] = img
    return templates


def recognize_grid(img, roi, templates):
    x, y, w, h = roi
    grid_img = img[y:y+h, x:x+w]       # 從截圖裁切出棋盤區域
    grid = np.zeros((4, 4), dtype=int)
    cell_w, cell_h = w / 4.0, h / 4.0  # 每格的寬高

    # 對每個模板在整個棋盤影像中搜尋，收集所有相似度 >= 0.8 的匹配位置
    matches = []
    for val, tmpl in templates.items():
        if tmpl.shape[0] > grid_img.shape[0] or tmpl.shape[1] > grid_img.shape[1]:
            continue
        result = cv2.matchTemplate(grid_img, tmpl, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.8)
        h_t, w_t = tmpl.shape[:2]
        for pt in zip(*loc[::-1]):
            cx = pt[0] + w_t // 2  # 匹配中心點 x
            cy = pt[1] + h_t // 2  # 匹配中心點 y
            score = result[pt[1], pt[0]]
            matches.append((val, score, cx, cy))

    # 依分數由高到低排序，每格只填入最高分的匹配結果
    matches.sort(key=lambda m: m[1], reverse=True)
    for val, score, cx, cy in matches:
        col = int(cx / cell_w)  # 中心點換算成格子欄索引
        row = int(cy / cell_h)  # 中心點換算成格子列索引
        if 0 <= col < 4 and 0 <= row < 4 and grid[row][col] == 0:
            grid[row][col] = val

    return grid


# ── 校準與截圖 ──

def get_board_roi():
    # 倒數 5 秒讓使用者切換至遊戲視窗，截圖後讓使用者框選棋盤範圍
    print("請切換至 2048 遊戲視窗，5 秒後自動截圖...")
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[1]))
    img = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)  # BGRA → BGR
    win_name = "Draw a box around the 4x4 grid"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)   # 視窗置頂
    cv2.resizeWindow(win_name, img.shape[1], img.shape[0])      # 與截圖同尺寸，避免壓縮
    roi = cv2.selectROI(win_name, img, showCrosshair=True)
    cv2.destroyAllWindows()
    return roi


# ── 視覺化 ──

def visualize_grid(grid):
    # 在 400×400 畫布上繪製 4×4 格線，並將辨識到的數字置中顯示
    canvas = np.zeros((400, 400, 3), dtype=np.uint8)
    for r in range(4):
        for c in range(4):
            x1, y1 = c * 100, r * 100
            cv2.rectangle(canvas, (x1, y1), (x1 + 100, y1 + 100), (200, 200, 200), 2)
            val = grid[r][c]
            if val > 0:
                text = str(val)
                scale = 0.8 if val < 100 else 0.6  # 三位數以上縮小字體
                size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)[0]
                tx = x1 + (100 - size[0]) // 2  # 水平置中
                ty = y1 + (100 + size[1]) // 2  # 垂直置中
                cv2.putText(canvas, text, (tx, ty),
                            cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 2)
    return canvas


# ── 主迴圈 ──

def game_loop(roi, templates):
    win_name = "2048 AI"
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(win_name, cv2.WND_PROP_TOPMOST, 1)  # 監控視窗置頂
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            screenshot = np.array(sct.grab(monitor))
            img = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

            grid = recognize_grid(img, roi, templates)

            canvas = visualize_grid(grid)
            cv2.imshow(win_name, canvas)

            direction = best_move(grid)
            if direction is None:
                if np.all(grid == 0):  # 棋盤全為零 → 辨識失敗，略過此幀
                    print("辨識失敗，略過此幀...")
                    cv2.waitKey(150)
                    continue
                print("Game Over!")   # 無路可走 → 遊戲結束
                break

            print(f"Move: {MOVE_KEYS[direction]}")
            pyautogui.press(MOVE_KEYS[direction])

            if cv2.waitKey(150) & 0xFF == ord("q"):  # 按 q 手動終止
                break

    cv2.destroyAllWindows()


# ── 進入點 ──

assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
templates = load_templates(assets_dir)
print(f"載入了 {len(templates)} 個模板：{sorted(templates.keys())}")
roi = get_board_roi()
game_loop(roi, templates)
