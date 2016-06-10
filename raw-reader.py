#!/usr/bin/python
import struct
import time
import sys
import json
from multiprocessing import Process
from publish import publish


def input1():
    waitInput("input1")
def input2():
    waitInput("input2")


def waitInput(key):
    # Open the configuration file and put content in config variable
    with open('config.json', 'r') as content_file:
        config = content_file.read()

    config = json.loads(config)
    infile_path = config[key]

    #long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    #open file in binary mode
    in_file = open(infile_path, "rb")

    event  = in_file.read(EVENT_SIZE)
    event2 = in_file.read(EVENT_SIZE)
    codigo = ""

    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event2)

        if type != 0 or code != 0 or value != 0:
            if type==4 and code==4 and str(value) in config[infile_path]:

                tvalue = config[infile_path][str(value)]

                if tvalue == "/":
                    if len(codigo) != 0:
                        if (codigo.find(tvalue) == -1) and (codigo.find(".") == -1):
                            codigo = codigo + tvalue
                elif tvalue == ".":
                    if len(codigo) != 0:
                        if (codigo.find(tvalue) == -1) and (codigo.find("/") == -1):
                            codigo = codigo + tvalue
                elif tvalue=="ENTER":
                    if len(codigo) >= 1:
                        publish(codigo, key)
                    codigo = ""
                else:
                    codigo = codigo +  tvalue


        event = in_file.read(EVENT_SIZE)
        event2 = in_file.read(EVENT_SIZE)

    in_file.close()

if __name__=='__main__':
    p1 = Process(target = input1)
    p1.start()
    p2 = Process(target = input2)
    p2.start()
