import os
import time
import threading
from picamera2 import Picamera2

class CyclicCameraCapture(threading.Thread):
    def __init__(self, save_dir, max_files=100, interval=300):
        super().__init__()
        self.save_dir = save_dir
        self.max_files = max_files
        self.interval = interval
        self.running = True

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.picam2 = Picamera2()
        self.picam2.start()

    def shift_files(self):
        # 从末尾往前移动文件：image_098.jpg -> image_099.jpg ... image_000.jpg -> image_001.jpg
        for i in reversed(range(self.max_files - 1)):
            src = os.path.join(self.save_dir, f"image_{i:03d}.jpg")
            dst = os.path.join(self.save_dir, f"image_{i + 1:03d}.jpg")
            if os.path.exists(src):
                os.rename(src, dst)

    def run(self):
        while self.running:
            self.shift_files()  # 所有旧照片编号往后移一位

            filename = os.path.join(self.save_dir, "image_000.jpg")  # 始终保存为最新图
            self.picam2.capture_file(filename)

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Captured: {filename}")
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.picam2.stop()
        print("Camera thread stopped.")

if __name__ == "__main__":
    save_path = "/home/pi/camera_images"
    camera_thread = CyclicCameraCapture(save_path, max_files=100, interval=300)

    try:
        camera_thread.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping camera thread...")
        camera_thread.stop()
        camera_thread.join() 那我这个应该怎么改
