import cv2
import numpy as np
import sys
import platform
from tkinter import Tk, filedialog
from image_tools import process_image

if platform.system() == 'Windows':
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

CANVAS = "Mini Photoshop"
CONTROLS = "Controls"

DRAW_COLORS = [
    (0, 0, 255), (0, 255, 0), (255, 0, 0),
    (0, 255, 255), (255, 255, 0), (255, 255, 255),
]
COLOR_NAMES = ['Red', 'Green', 'Blue', 'Yellow', 'Cyan', 'White']

TRACKBAR_SPECS = [
    ("Brighten", 100, 200),
    ("Contrast", 100, 200),
    ("Saturate", 100, 200),
    ("Hue", 0, 180),
    ("Temp", 100, 200),
    ("Rotate", 0, 360),
    ("Zoom", 100, 200),
    ("Flip", 0, 3),
    ("Blur", 0, 10),
    ("Sharpen", 0, 10),
    ("Pen Width", 2, 10),
    ("Pen Color", 0, 5),
]

state = {
    'draw_mode': False,
    'draw_tool': 'rect',
    'drawing': False,
    'start_pt': None,
    'current_pt': None,
    'annotations': [],
}


def get_screen_size():
    root = Tk()
    root.withdraw()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.destroy()
    return w, h


def open_file_dialog():
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Open Image",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    root.destroy()
    return path if path else None


def load_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    h, w = img.shape[:2]
    max_dim = 1024
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    return img


def create_windows(img_w, img_h):
    screen_w, screen_h = get_screen_size()

    cv2.namedWindow(CANVAS, cv2.WINDOW_NORMAL)
    cv2.namedWindow(CONTROLS, cv2.WINDOW_NORMAL)

    canvas_h = img_h + 60
    canvas_w = img_w
    panel_w = 500
    panel_x = canvas_w + 60

    if panel_x + panel_w > screen_w - 30:
        panel_x = screen_w - panel_w - 30
        canvas_w = max(panel_x - 60, 300)

    cv2.moveWindow(CANVAS, 20, 40)
    cv2.resizeWindow(CANVAS, canvas_w, canvas_h)

    cv2.moveWindow(CONTROLS, panel_x, 40)


def create_trackbars():
    for name, default, max_val in TRACKBAR_SPECS:
        cv2.createTrackbar(name, CONTROLS, default, max_val, lambda x: None)


def reset_trackbars():
    for name, default, _ in TRACKBAR_SPECS:
        cv2.setTrackbarPos(name, CONTROLS, default)


def get_params():
    return {
        'brightness': cv2.getTrackbarPos("Brighten", CONTROLS),
        'contrast': cv2.getTrackbarPos("Contrast", CONTROLS),
        'saturation': cv2.getTrackbarPos("Saturate", CONTROLS),
        'hue': cv2.getTrackbarPos("Hue", CONTROLS),
        'temperature': cv2.getTrackbarPos("Temp", CONTROLS),
        'rotation': cv2.getTrackbarPos("Rotate", CONTROLS),
        'zoom': cv2.getTrackbarPos("Zoom", CONTROLS),
        'flip': cv2.getTrackbarPos("Flip", CONTROLS),
        'blur': cv2.getTrackbarPos("Blur", CONTROLS),
        'sharpen': cv2.getTrackbarPos("Sharpen", CONTROLS),
    }


def get_active_effects(params):
    active = []
    if params['brightness'] != 100:
        diff = params['brightness'] - 100
        active.append(f"Bright {'+' if diff > 0 else ''}{diff}")
    if params['contrast'] != 100:
        active.append(f"Contrast {params['contrast'] / 100:.1f}x")
    if params['saturation'] != 100:
        active.append(f"Sat {params['saturation'] / 100:.1f}x")
    if params['hue'] != 0:
        active.append(f"Hue +{params['hue']}")
    if params['temperature'] != 100:
        active.append("Temp Warm" if params['temperature'] > 100 else "Temp Cool")
    if params['rotation'] != 0:
        active.append(f"Rot {params['rotation']}")
    if params['zoom'] != 100:
        active.append(f"Zoom {params['zoom']}%")
    if params['flip'] != 0:
        names = {1: 'Flip H', 2: 'Flip V', 3: 'Flip HV'}
        active.append(names[params['flip']])
    if params['blur'] > 0:
        k = params['blur'] * 2 + 1
        active.append(f"Blur {k}x{k}")
    if params['sharpen'] > 0:
        active.append(f"Sharp {params['sharpen']}")
    return active


def create_status_bar(img_w, params):
    bar_h = 60
    bar = np.zeros((bar_h, img_w, 3), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    white = (255, 255, 255)
    cyan = (255, 255, 0)
    gray = (128, 128, 128)

    if state['draw_mode']:
        tool_name = "Rect" if state['draw_tool'] == 'rect' else "Line"
        color_idx = cv2.getTrackbarPos("Pen Color", CONTROLS)
        width = max(cv2.getTrackbarPos("Pen Width", CONTROLS), 1)
        cv2.putText(bar, f"DRAW: {tool_name} | {COLOR_NAMES[color_idx]} W:{width}",
                    (10, 20), font, 0.5, cyan, 1)
        cv2.putText(bar, "1=Rect 2=Line  d=Exit  c=Clear  s=Save  q=Quit",
                    (10, 45), font, 0.45, white, 1)
    else:
        active = get_active_effects(params)
        if active:
            line = " | ".join(active)
            cv2.putText(bar, line, (10, 20), font, 0.45, cyan, 1)
        else:
            cv2.putText(bar, "(Original)", (10, 20), font, 0.5, gray, 1)
        cv2.putText(bar, "o=Open  d=Draw  r=Reset  s=Save  q=Quit",
                    (10, 45), font, 0.45, white, 1)

    return bar


def draw_annotations(img, annotations):
    for ann in annotations:
        if ann['type'] == 'rect':
            cv2.rectangle(img, ann['pt1'], ann['pt2'], ann['color'], ann['thickness'])
        else:
            cv2.line(img, ann['pt1'], ann['pt2'], ann['color'], ann['thickness'])


def mouse_handler(event, x, y, flags, param):
    if not state['draw_mode']:
        return
    img_h = state.get('img_h', 99999)
    if y >= img_h:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        state['drawing'] = True
        state['start_pt'] = (x, y)
        state['current_pt'] = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        state['current_pt'] = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        if state['drawing'] and state['start_pt']:
            color = DRAW_COLORS[cv2.getTrackbarPos("Pen Color", CONTROLS)]
            thickness = max(cv2.getTrackbarPos("Pen Width", CONTROLS), 1)
            state['annotations'].append({
                'type': state['draw_tool'],
                'pt1': state['start_pt'],
                'pt2': (x, y),
                'color': color,
                'thickness': thickness,
            })
        state['drawing'] = False
        state['start_pt'] = None


def run_editor(img):
    h, w = img.shape[:2]
    create_windows(w, h)
    create_trackbars()
    cv2.setMouseCallback(CANVAS, mouse_handler)

    while True:
        params = get_params()
        result = process_image(img, params)
        display = result.copy()
        state['img_h'] = display.shape[0]

        draw_annotations(display, state['annotations'])

        if state['draw_mode']:
            tool_name = "Rect" if state['draw_tool'] == 'rect' else "Line"
            cv2.putText(display, f"[DRAW: {tool_name}]", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            if state['drawing'] and state['start_pt'] and state['current_pt']:
                color = DRAW_COLORS[cv2.getTrackbarPos("Pen Color", CONTROLS)]
                thickness = max(cv2.getTrackbarPos("Pen Width", CONTROLS), 1)
                if state['draw_tool'] == 'rect':
                    cv2.rectangle(display, state['start_pt'], state['current_pt'],
                                  color, thickness)
                else:
                    cv2.line(display, state['start_pt'], state['current_pt'],
                             color, thickness)

        status_bar = create_status_bar(display.shape[1], params)
        canvas_img = np.vstack([display, status_bar])
        cv2.imshow(CANVAS, canvas_img)

        key = cv2.waitKey(30) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            save_img = result.copy()
            draw_annotations(save_img, state['annotations'])
            cv2.imwrite("result.jpg", save_img)
            print("Saved: result.jpg")
        elif key == ord('r'):
            reset_trackbars()
        elif key == ord('o'):
            path = open_file_dialog()
            if path:
                new_img = load_image(path)
                if new_img is not None:
                    img = new_img
                    state['annotations'].clear()
                    reset_trackbars()
        elif key == ord('d'):
            state['draw_mode'] = not state['draw_mode']
            state['drawing'] = False
            state['start_pt'] = None
        elif key == ord('1') and state['draw_mode']:
            state['draw_tool'] = 'rect'
        elif key == ord('2') and state['draw_mode']:
            state['draw_tool'] = 'line'
        elif key == ord('c'):
            state['annotations'].clear()

    cv2.destroyAllWindows()


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = open_file_dialog()
        if not path:
            print("No image selected.")
            return

    img = load_image(path)
    if img is None:
        print(f"Cannot read: {path}")
        return

    h, w = img.shape[:2]
    print(f"=== Mini Photoshop === ({w}x{h})")
    run_editor(img)


if __name__ == "__main__":
    main()
