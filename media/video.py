# -*- coding: utf-8 -*-
#
#    references: http://www.xavierdupre.fr/blog/2016-03-30_nojs.html
#                http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
#
#    Create a video from a list of images.
#
#    @param      outvid      output video
#    @param      images      list of images to use in the video
#    @param      fps         frame per second
#    @param      size        size of each frame
#    @param      is_color    color
#    @param      vformat     see http://www.fourcc.org/codecs.php
#    @param      "XVID"
#    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
#
#    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
#    By default, the video will have the size of the first image.
#    It will resize every image to this size before adding them to the video.
#
import os
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize


def make_video(images, outvid=None, fps=5, size=None,
               is_color=True, vformat="XVID"):

    fourcc = VideoWriter_fourcc(*vformat)
    vid = None
    for image in images:
        if not os.path.exists(image):
            raise FileNotFoundError(image)
        img = imread(image)
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid, fourcc, float(fps), size, is_color)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)

    vid.release()
    return vid
