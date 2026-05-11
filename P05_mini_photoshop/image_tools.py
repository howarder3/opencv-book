import cv2
import numpy as np


def adjust_brightness_contrast(img, brightness, contrast):
    if brightness == 100 and contrast == 100:
        return img
    alpha = contrast / 100.0
    beta = brightness - 100
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def adjust_saturation_hue(img, saturation, hue):
    if saturation == 100 and hue == 0:
        return img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    if saturation != 100:
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * (saturation / 100.0), 0, 255)
    if hue != 0:
        hsv[:, :, 0] = (hsv[:, :, 0] + hue) % 180
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


def adjust_temperature(img, val):
    if val == 100:
        return img
    b, g, r = cv2.split(img)
    shift = (val - 100) * 0.5
    r = np.clip(r.astype(np.float32) + shift, 0, 255).astype(np.uint8)
    b = np.clip(b.astype(np.float32) - shift, 0, 255).astype(np.uint8)
    return cv2.merge([b, g, r])


def apply_flip(img, val):
    if val == 0:
        return img
    if val == 1:
        return cv2.flip(img, 1)
    if val == 2:
        return cv2.flip(img, 0)
    return cv2.flip(img, -1)


def apply_rotation(img, val):
    if val == 0:
        return img
    h, w = img.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, -val, 1.0)
    return cv2.warpAffine(img, M, (w, h))


def apply_zoom(img, val):
    if val == 100:
        return img
    h, w = img.shape[:2]
    val = max(val, 10)
    if val > 100:
        crop_w = int(w * 100 / val)
        crop_h = int(h * 100 / val)
        x1 = (w - crop_w) // 2
        y1 = (h - crop_h) // 2
        cropped = img[y1:y1 + crop_h, x1:x1 + crop_w]
        return cv2.resize(cropped, (w, h))
    new_w = int(w * val / 100)
    new_h = int(h * val / 100)
    resized = cv2.resize(img, (new_w, new_h))
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2
    canvas[y1:y1 + new_h, x1:x1 + new_w] = resized
    return canvas


def apply_blur(img, val):
    if val == 0:
        return img
    k = val * 2 + 1
    return cv2.GaussianBlur(img, (k, k), 0)


def apply_sharpen(img, val):
    if val == 0:
        return img
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    strength = 1.0 + val / 5.0
    return cv2.addWeighted(img, strength, blurred, -(strength - 1.0), 0)


def process_image(img, params):
    result = adjust_brightness_contrast(img, params['brightness'], params['contrast'])
    result = adjust_saturation_hue(result, params['saturation'], params['hue'])
    result = adjust_temperature(result, params['temperature'])
    result = apply_flip(result, params['flip'])
    result = apply_rotation(result, params['rotation'])
    result = apply_zoom(result, params['zoom'])
    result = apply_blur(result, params['blur'])
    result = apply_sharpen(result, params['sharpen'])
    return result
