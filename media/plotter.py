# -*- coding: utf-8 -*-
#
# Class Plotter: used to create output images and/or videos. An instance of
# it must be sent to the SimulationControl class if we want it to generate
# images. Only afterwards, optionally, a video can be generated using those
# images.
#

import os
import numpy as np
import matplotlib.pyplot as plt
from media.video import make_video


class Plotter:

    # The 'columns' parameter here indicates the attributes we want
    # shown on the output images. MUST be a list of strings that
    # were previously defined on the current universe's df-columns, otherwise
    # an exception will happen
    def __init__(self, title, path, columns, n_simuls, parent_path=None):
        self.columns = columns
        self.title = title

        if parent_path is not None:
            if not os.path.exists(parent_path):
                os.mkdir(parent_path)
            self.path = os.path.join(parent_path, path)
        else:
            self.path = os.path.join(path, path)
        self.n_simuls_prec = max([1, int(np.ceil(np.log10(n_simuls + 1)))])
        self.n_simuls = n_simuls

    def save_image(self, df, idx=0):
        df[self.columns].plot()
        plt.title(self.title + (' {0:0{1}}'.format(idx, self.n_simuls_prec)))
        plt.savefig(self.path + ('_{0:0{1}}'.format(idx, self.n_simuls_prec)))
        plt.close()

    def make_video(self, out_path, fps=None):

        images = [(self.path + '_{0:0{1}}.png'.format(i, self.n_simuls_prec)) for i in range(self.n_simuls)]

        if fps is None:
            fps = self.n_simuls / 10

        make_video(images, outvid=(out_path + '.avi'), fps=fps)

