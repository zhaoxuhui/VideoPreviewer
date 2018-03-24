# coding=utf-8
import os


# 读取目录下所有视频的路径，返回一个list
def findAllVideos(root_dir):
    paths = []
    # 遍历
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            # 这里只选择了两种最常用的视频格式
            if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".MP4") or filename.endswith(".AVI"):
                paths.append(parent + "\\" + filename)
    return paths


# 用户指定目录
root_dir = input("Input the parent path of videos:\n")

paths = findAllVideos(root_dir)

for i in range(paths.__len__()):
    print("Video", (i + 1), "/", paths.__len__().__str__())
    command = "python preview_py3.py " + '"' + paths[i] + '"' + " 400 " + (i + 1).__str__() + ".jpg"
    print(command)
    os.system(command)
    print("\n")
