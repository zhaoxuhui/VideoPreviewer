# coding=utf-8
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
import sys


# 批量保存关键帧，这里没用到
def saveImages(images, indices, out_path):
    for i in range(images.__len__()):
        cv2.imwrite(out_path + "\\" + "%05d" % (indices[i]) + ".jpg", images[i])


# 批量给关键帧添加时间戳
def txtImages(images, frames_save, frames, fps):
    for i in range(images.__len__()):
        txt = (frames_save[i] * 1.0 / frames) * (frames * 1.0 / fps)

        m, s = divmod(txt, 60)
        h, m = divmod(m, 60)

        cv2.putText(images[i],
                    "%02d:%02d:%02d" % (h, m, s),
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA)


max_width = 400
num_sample = 16
cols = 4
rows = 4
interval = 20
margin = 20
top = 100
bottom = 30
out_path = "content.jpg"

# 程序启动逻辑
# 如果启动时没有参数，则启动后手动输入参数
# 如果启动时有一个参数，默认缩略图大小为400
# 如果启动时有两个参数，输出文件名为默认
# 如果启动时有三个参数，则按照指定参数运行
# 否则，报错退出，并给出运行提示
if sys.argv.__len__() == 1:
    # 输入需要处理的视频文件
    video_path = input("Input path of video:\n")

    # 输入视频每一帧的缩略图大小，默认为400
    input_width = input("Input width for frame thumbnail(press 'd' use 400 as default):")
    if input_width == "d":
        max_width = 400
    else:
        max_width = int(input_width)
    out_path = input("Input the name of output jpg file(press 'd' use 'content.jpg' as default):")
    if out_path == "d":
        out_path = 'content.jpg'
elif sys.argv.__len__() == 2:
    video_path = sys.argv[1]
    max_width = 400
elif sys.argv.__len__() == 3:
    video_path = sys.argv[1]
    max_width = int(sys.argv[2])
elif sys.argv.__len__() == 4:
    video_path = sys.argv[1]
    max_width = int(sys.argv[2])
    out_path = sys.argv[3]
else:
    print("Wrong params.")
    print("You can run the script directly with no params and input them manually later.\n" \
          "Or you can give params to script before running using these following formats:\n" \
          "[1]python script.py video_path\n" \
          "[2]python script.py video_path thumbnail_width\n" \
          "[3]python script.py video_path thumbnail_width out_filename" \
          "If you don't give the param 'thumbnail_width' , it will be 400 as default." \
          "If you don't give the param 'out_filename', it will be 'content.jpg' as default.")
    exit()

cap = cv2.VideoCapture(video_path)
frames = int(cap.get(7))
fps = int(cap.get(5))
video_width = int(cap.get(3))
video_height = int(cap.get(4))

print(frames, 'frames in total.')

ratio = max_width * 1.0 / video_width
delta_frame = int(frames / num_sample)

frames_save = []
images = []

t1 = time.time()

for i in range(num_sample):
    i = i * delta_frame
    frames_save.append(i)

for item in frames_save:
    cap.set(cv2.CAP_PROP_POS_FRAMES, item)
    ret, frame = cap.read()
    if frame is None:
        break
    else:
        images.append(cv2.resize(frame, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_LINEAR))
        print("processing...", round((item * 1.0 / frames) * 100, 2), " %")

# 释放对象
cap.release()

txtImages(images, frames_save, frames, fps)

max_height = images[0].shape[0]

width = max_width * cols + interval * (cols - 1) + margin * 2
height = max_height * rows + interval * (rows - 1) + margin * 2 + bottom

result = np.zeros((height, width, 3), np.uint8) + 255

# 输出文件相关信息
info = Image.fromarray(np.zeros((top, width, 3), np.uint8) + 230)
draw = ImageDraw.Draw(info)
font = ImageFont.truetype('hwxh.ttf', 24)
draw.text((1 * margin, 20), u'文件名：' + video_path.split("\\")[-1], (0, 0, 0), font=font)
draw.text((1 * margin, 50), u'分辨率：' + video_width.__str__() + u" × " + video_height.__str__(), (0, 0, 0), font=font)
draw.text((1 * margin + 1 * max_width, 50), u'时长：' + round(frames * 1.0 / fps, 3).__str__() + " s", (0, 0, 0),
          font=font)
draw.text((3 * margin + 2 * max_width, 50), u'帧率：' + fps.__str__(), (0, 0, 0), font=font)
draw.text((4 * margin + 3 * max_width, 50), u'帧计数：' + frames.__str__(), (0, 0, 0), font=font)

for i in range(rows):
    for j in range(cols):
        result[margin + i * interval + i * max_height:margin + i * interval + i * max_height + max_height,
        margin + j * interval + j * max_width:margin + j * interval + j * max_width + max_width] = \
            images[i * 4 + j * 1]

if width - 500 <= 0:
    loc_x = 0
else:
    loc_x = width - 500

cv2.putText(result,
            "Created by video previewer written by Zhao Xuhui.",
            (loc_x, height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            1,
            cv2.LINE_AA)

res = np.vstack([info, result])
cv2.imwrite(out_path, res)

t2 = time.time()

print("process...finished.")
print("Total time cost:", round(t2 - t1, 2), "s")
