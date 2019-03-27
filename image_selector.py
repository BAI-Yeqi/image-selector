#!/usr/bin/env python
##############################################################################
# Copyright (c) 2012 Hajime Nakagami<nakagami@gmail.com>
# All rights reserved.
# Licensed under the New BSD License
# (http://www.freebsd.org/copyright/freebsd-license.html)
#
# A image viewer. Require Pillow ( https://pypi.python.org/pypi/Pillow/ ).
##############################################################################
import PIL.Image
try:
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError:
    from tkinter import *
    from tkinter import filedialog
import PIL.ImageTk
import os
from shutil import copyfile
import numpy as np


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Image Viewer')

        self.num_page=0
        self.num_page_tv = StringVar()

        # define the path to the folders
        # scene graph directory
        self.sg_dir = "./output_sg"
        # baseline image
        self.base_dir = "./vg128"
        # vg model top 1
        self.top1_dir = "./result_image_1"
        # vg model top 2
        self.top2_dir = "./result_image_2"

        # define output folder
        self.sel_dir = "./selected_images"
        try:
            # Create target Directory
            os.mkdir(self.sel_dir)
            print("Directory " , self.sel_dir ,  " Created ")
        except FileExistsError:
            print("Directory " , self.sel_dir ,  " already exists")

        self.im_id = 0

        fram = Frame(self)
        # Button(fram, text="Open File", command=self.open).pack(side=LEFT)
        Button(fram, text="Prev", command=self.seek_prev).pack(side=LEFT)
        Button(fram, text="Next", command=self.seek_next).pack(side=LEFT)
        Button(fram, text="Save", command=self.save).pack(side=LEFT)
        Label(fram, textvariable=self.num_page_tv).pack(side=LEFT)
        fram.pack(side=TOP, fill=BOTH)

        self.sg_la = Label(self)
        self.base_la = Label(self)
        self.top1_la = Label(self)
        self.top2_la = Label(self)
        self.base_la.pack(side=LEFT)
        self.top1_la.pack(side=LEFT)
        self.top2_la.pack(side=LEFT)
        self.sg_la.pack()
        # self.sg_la.grid(row=1, column=0)

        self.pack()

        self.open_folders()

    '''
    def chg_image(self):
        if self.im.mode == "1": # bitmap image
            self.img = PIL.ImageTk.BitmapImage(self.im, foreground="white")
        else:              # photo image
            self.img = PIL.ImageTk.PhotoImage(self.im)
        self.la.config(image=self.img, bg="#000000",
            width=self.img.width(), height=self.img.height())
    '''

    def chg_images(self):
        '''
        for im, la in [(self.sg_im, self.sg_la), (self.base_im, self.base_la), (self.top1_im, self.top1_la), (self.top2_im, self.top2_la)]:
            if im.mode == "1": # bitmap image
                img = PIL.ImageTk.BitmapImage(im, foreground="white")
            else:              # photo image
                img = PIL.ImageTk.PhotoImage(im)
            la.config(image=img, bg="#000000",
                width=img.width(), height=img.height())
        '''

        if self.sg_im.mode == "1": # bitmap image
            self.sg_img = PIL.ImageTk.BitmapImage(self.sg_im, foreground="white", background="white")
        else:              # photo image
            self.sg_img = PIL.ImageTk.PhotoImage(self.sg_im)
        self.sg_la.config(image=self.sg_img, bg="#000000",
            width=self.sg_img.width(), height=self.sg_img.height())

        if self.base_im.mode == "1": # bitmap image
            self.base_img = PIL.ImageTk.BitmapImage(self.base_im, foreground="white")
        else:              # photo image
            self.base_img = PIL.ImageTk.PhotoImage(self.base_im)
        self.base_la.config(image=self.base_img, bg="#000000",
            width=self.base_img.width(), height=self.base_img.height())

        if self.top1_im.mode == "1": # bitmap image
            self.top1_img = PIL.ImageTk.BitmapImage(self.top1_im, foreground="white")
        else:              # photo image
            self.top1_img = PIL.ImageTk.PhotoImage(self.top1_im)
        self.top1_la.config(image=self.top1_img, bg="#000000",
            width=self.top1_img.width(), height=self.top1_img.height())

        if self.top2_im.mode == "1": # bitmap image
            self.top2_img = PIL.ImageTk.BitmapImage(self.top2_im, foreground="white")
        else:              # photo image
            self.top2_img = PIL.ImageTk.PhotoImage(self.top2_im)
        self.top2_la.config(image=self.top2_img, bg="#000000",
            width=self.top2_img.width(), height=self.top2_img.height())

    def open_folders(self):
        sg_filename = os.path.join(self.sg_dir, "sg_" + str(self.im_id) + ".png")
        base_filename = os.path.join(self.base_dir, "img_" + str(self.im_id) + ".png")
        top1_filename = os.path.join(self.top1_dir, "img_" + str(self.im_id) + ".png")
        top2_filename = os.path.join(self.top2_dir, "img_" + str(self.im_id) + ".png")
        self.sg_im = PIL.Image.open(sg_filename)
        self.sg_im = self.sg_im.resize((self.sg_im.width // 2, self.sg_im.height // 2), PIL.Image.ANTIALIAS)
        self.sg_im = self.white_background(self.sg_im)
        self.base_im = PIL.Image.open(base_filename)
        self.base_im = self.base_im.resize((self.base_im.width * 1, self.base_im.height * 1), PIL.Image.ANTIALIAS)
        self.top1_im = PIL.Image.open(top1_filename)
        self.top1_im = self.top1_im.resize((self.top1_im.width * 1, self.top1_im.height * 1), PIL.Image.ANTIALIAS)
        self.top2_im = PIL.Image.open(top2_filename)
        self.top2_im = self.top2_im.resize((self.top2_im.width * 1, self.top2_im.height * 1), PIL.Image.ANTIALIAS)
        self.chg_images()

    def white_background(self, im):
        data = np.array(im)
        alpha1 = 0 # Original value
        r2, g2, b2, alpha2 = 255, 255, 255, 255 # Value that we want to replace it with
        red, green, blue,alpha = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
        mask = (alpha==alpha1)
        data[:,:,:][mask] = [r2, g2, b2, alpha2]
        im = PIL.Image.fromarray(data)

        return im

    def seek_prev(self):
        self.im_id = self.im_id - 1
        if self.im_id < 0:
            self.im_id = 0
        self.open_folders()
        self.chg_images()
        self.num_page_tv.set(str(self.im_id))

    def seek_next(self):
        self.im_id = self.im_id + 1
        if self.im_id < 0:
            self.im_id = 0
        self.open_folders()
        self.chg_images()
        self.num_page_tv.set(str(self.im_id))

    def save(self):
        sg_filename = os.path.join(self.sg_dir, "sg_" + str(self.im_id) + ".png")
        base_filename = os.path.join(self.base_dir, "img_" + str(self.im_id) + ".png")
        top1_filename = os.path.join(self.top1_dir, "img_" + str(self.im_id) + ".png")
        top2_filename = os.path.join(self.top2_dir, "img_" + str(self.im_id) + ".png")
        copyfile(sg_filename, os.path.join(self.sel_dir, str(self.im_id) + "_sg" + ".png"))
        copyfile(base_filename, os.path.join(self.sel_dir, str(self.im_id) + "_base" + ".png"))
        copyfile(top1_filename, os.path.join(self.sel_dir, str(self.im_id) + "_top1" + ".png"))
        copyfile(top2_filename, os.path.join(self.sel_dir, str(self.im_id) + "_top2" + ".png"))

    '''
    def open(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.im = PIL.Image.open(filename)
        self.chg_image()
        self.num_page=0
        self.num_page_tv.set(str(self.num_page+1))

    def seek_prev(self):
        self.num_page=self.num_page-1
        if self.num_page < 0:
            self.num_page = 0
        self.im.seek(self.num_page)
        self.chg_image()
        self.num_page_tv.set(str(self.num_page+1))

    def seek_next(self):
        self.num_page=self.num_page+1
        try:
            self.im.seek(self.num_page)
        except:
            self.num_page=self.num_page-1
        self.chg_image()
        self.num_page_tv.set(str(self.num_page+1))
    '''


if __name__ == "__main__":
    app = App(); app.mainloop()
