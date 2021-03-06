import re
import time
import os
import wave
import struct
import threading

import json
import numpy as np
from pprint import pprint
from PIL import Image, ImageDraw

count_value = 0
folder = None
check = None
class Zapys:
    def __init__(self, element, folders):
        self.folders = folders
        elements = element.split(" ")
        self.number = elements[1]
        self.type_of = elements[0]
        self.word = elements[2]
        self.frame_num = elements[3]
        self.frame_size = elements[4]
        if element[-1] == " ":
            self.data = elements[5:-1]
        else:
            self.data = elements[5:]
        self.data = [int(item) for item in self.data]

    def draw_spectr(self, folder):
        frame_size = int(self.frame_size)
        frame_num = int(self.frame_num)
        #print(f"{self.number}:   Elements_len = {len(self.result)},\t frame_num={frame_num}, frame_size={frame_size}")
        maxi = max(self.result)

        data = [val / maxi * 255 for val in self.result]
        data = list(map(int, data))
        #print(f"{self.number}:   Elements_len = {len(data)},\t frame_num={frame_num}, frame_size={frame_size}")
        img_data = [[data[i * frame_size + j] for j in range(frame_size)] for i in range(frame_num)]
        img = Image.new("RGB", (frame_num, frame_size), (255, 0, 0))
        draw = ImageDraw.Draw(img)

        for i in range(frame_num):
            for j in range(frame_size):
                draw.point((i, j), (img_data[i][j], img_data[i][j], img_data[i][j]))
        img.save(f"{folder}/{self.number}_{self.word}.jpg", "JPEG")




    def make(self):
        self.result = []
        i = 0
        if self.type_of == 'S':
            while i < (len(self.data)):
                if self.data[i] != 0:
                    self.result.append(self.data[i])
                else:
                    zeros = [0 for j in range(self.data[i + 1])]
                    self.result.extend(zeros)
                    i += 1
                i += 1
        elif self.type_of == 'W':
            self.result = self.data

        dict = {"label": self.word, "values": self.result}
        if self.type_of == 'W':
            filename = self.number + self.type_of + self.word + str(int(self.frame_num) * int(self.frame_size))
            sub_fold = 'Waves_Json'
            sub_waves = "WAV"
            if (os.path.exists(folder + "/" + folders + "/" + sub_waves) == False):
                os.makedirs(name=folder + "/" + folders + "/" + sub_waves)

            new_file_wav = folder + "/" + folders +"/" + sub_waves + "/" + filename
            elements = len(self.result)
            sample_int = [int(element) for element in self.result]

            wav = wave.open(new_file_wav + ".wav", "wb")
            wav.setnchannels(1)     #mono - one channel
            wav.setsampwidth(2)     #bytes in frame
            wav.setframerate(16000.0)
            for index2 in range(0, elements):
                val = struct.pack("<h", sample_int[index2])
                wav.writeframesraw(val)
            wav.close()

        elif self.type_of == 'S':
            filename = self.number + self.type_of + self.word + str(int(self.frame_num) * int(self.frame_size) + 2)
            dict.update({"frame_num": self.frame_num, "frame_size": self.frame_size})
            sub_fold = "Spect"
            name_of_folder = folder + "/" + folders + "/img"

            if (os.path.exists(name_of_folder) == False):
                os.makedirs(name=name_of_folder)
            self.draw_spectr(name_of_folder)

        name_of_folder = folder + "/" + folders + "/" + sub_fold
        if (os.path.exists(name_of_folder) == False):
            os.makedirs(name=name_of_folder)

        with open(folder + "/" + folders +"/" + sub_fold + "/" + filename + ".json", 'w+') as fp:
            json.dump(dict, fp)


def SplitFiles(path):
    global count_value
    global folder
    global check
    global folders
    try:
        with open(path, 'r') as file:
            text = file.read()

        text = text.split('\n')


        if (text[-1] == ""):
            text = text[:-1]

        folder = "results"

        if (os.path.exists(folder) == False):
            os.makedirs(name=folder)

        couples = len(text)
        index = 0

        folders = 0
        for _, dirnames, _ in os.walk(os.getcwd() + '/' + folder):
            folders += len(dirnames)
        folders = str(folders//2)
        os.makedirs(name=folder + "/" + str(folders))

        for element in text:
            if (check == True):
                return
            zapys = Zapys(element, folders)
            zapys.make()
            count_value = (index) / (couples - 1 + 0.001) * 100
            index += 1

        check = None
        count_value = -1
    except:

        check = False


def clear_count():
    global count_value
    count_value = 0


def get_check():
    global check
    return check


def get_folder():
    global folder
    return folder


def set_check_True():
    global check
    check = True


def set_check_None():
    global check
    check = None
