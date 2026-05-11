import cv2
import platform # 新增：作為判斷 macOS 使用
import matplotlib.pyplot as plt


class opencv_tools(object):
    # 封裝 1-1 利用 matplotlib 顯示圖片
    @staticmethod
    def show_img_by_matplotlib(img):
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(image_rgb)
        plt.show()
        
    # 封裝 1-4 利用 OpenCV 內建的函式顯示圖片
    @staticmethod
    def show_img_by_opencv(img):
        window_name = "Image window"
        cv2.imshow(window_name, img)
        while True:
            key = cv2.waitKey(1)  # 每 1ms 檢查一次
            # 防呆：檢查視窗是否被手動關閉
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("視窗已被手動關閉！")  # 提示使用者
                break
            # 防呆：檢查是否按下 q 鍵
            if key == ord('q'):
                print("按下 Q 鍵，視窗即將關閉！")  # 提示使用者
                break
        cv2.destroyAllWindows()  
        
        # 新增：針對 macOS 的額外處理，使用額外的 waitKey 協助清理視窗
        if platform.system() == "Darwin":
            cv2.waitKey(1)      
    
    # 使用 matplitlib subplot 功能同時顯示 2 組結果
    @staticmethod
    def show_img_by_matplotlib_1x2(title1, img1, title2, img2):
        imgs = [img1, img2]
        titles = [title1, title2]
        plt.figure(figsize=(10, 5))
        for i in range(2):
            img_rgb = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2RGB)
            plt.subplot(1, 2, i+1)
            plt.imshow(img_rgb)
            plt.title(titles[i], fontsize=20)
        plt.tight_layout()
        plt.show()
        
    # 使用 matplitlib subplot 功能同時顯示 3 組結果
    @staticmethod
    def show_img_by_matplotlib_1x3(title1, img1, title2, img2, title3, img3):
        imgs = [img1, img2, img3]
        titles = [title1, title2, title3]
        plt.figure(figsize=(15, 5))
        for i in range(3):
            img_rgb = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2RGB)
            plt.subplot(1, 3, i+1)
            plt.imshow(img_rgb)
            plt.title(titles[i], fontsize=20)
        plt.tight_layout()
        plt.show()

    # 使用 matplitlib subplot 功能同時顯示 4 組結果
    @staticmethod
    def show_img_by_matplotlib_2x2(title1, img1, title2, img2, title3, img3, title4, img4):
        imgs = [img1, img2, img3, img4]
        titles = [title1, title2, title3, title4]
        plt.figure(figsize=(15, 15))
        for i in range(4):
            img_rgb = cv2.cvtColor(imgs[i], cv2.COLOR_BGR2RGB)
            plt.subplot(2, 2, i+1)
            plt.imshow(img_rgb)
            plt.title(titles[i], fontsize=20)
        plt.tight_layout()
        plt.show()




        