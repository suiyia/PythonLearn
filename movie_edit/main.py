#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

from moviepy.editor import VideoFileClip, concatenate_videoclips, ffmpeg_tools, CompositeVideoClip
from moviepy.video.fx.resize import resize

def addHeader():

    # 片头素材 位置 帧高度 帧宽度
    clip1 = VideoFileClip("头条号片头.mp4")
    pre_width = 1444
    pre_height = 820

    path = os.path.abspath('.')
    filenames = os.listdir('movie/')  # 源视频路径
    for filename in filenames:
        clip2 = VideoFileClip(path+'/movie/'+filename)
        width_temp = clip2.size[0]  # 目标视频帧宽
        height_temp = clip2.size[1]
        rate1 = pre_width/width_temp
        rate2 = pre_height/height_temp
        rate = rate1 if (rate1 > rate2) else rate2 # 缩放比例，选择缩放程度较大的
        clip1 = clip1.resize(1/rate)
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.resize(newsize=(width_temp, height_temp)).write_videofile('movie1/'+filename)


if __name__ == '__main__':
    addHeader()
