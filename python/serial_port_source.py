#
# Copyright 1980-2012 Free Software Foundation, Inc.
# 
# This file is part of GNU Radio
# 
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import serial
#import os

NONE = 0
EVEN = 1 
ODD = 2

STOPBITS_ONE = 0
STOPBITS_TWO = 1

WORD_SIZE_7 = 0 
WORD_SIZE_8 = 1

class serial_port_source(gr.basic_block):
    """
    Provides serial port connection within GNU Radio flowgraph
    """
    def __init__(
        self,device,parity,baudrate,stopbits,bytesize,wait_for_newline
    ):
        """
        Serial port w/ blobs in and out
        """

        gr.basic_block.__init__(
            self,
            "serial_port_source",
            None,
            [numpy.byte]
        )
    
        self.device = device
        self.parity = parity
        self.baudrate = baudrate 
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.wait_for_newline = wait_for_newline
        
        #set parity
        
        if self.parity == NONE:
            self.parity = serial.PARITY_NONE
        elif self.parity == EVEN:
            self.parity = serial.PARITY_EVEN
        else:
            self.parity = serial.PARITY_ODD
        
        if self.stopbits == STOPBITS_ONE:
            self.stopbits = serial.STOPBITS_ONE
        elif self.stopbits == STOPBITS_TWO:
            self.stopbits = serial.STOPBITS_TWO
        
        if self.bytesize == WORD_SIZE_7:
            self.bytesize = serial.SEVENBITS
        else:
            self.bytesize = serial.EIGHTBITS
        
        # configure the serial connections (the parameters differs on the device you are connecting to)
        
        self.ser = serial.Serial(
            port=self.device,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize
        )

        '''
        self.ser = serial.Serial(
            port=self.device,
            baudrate=self.baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        '''
        print "Opened: ",self.ser.portstr       # check which port was really used
        self.ser.write("hel;lkfsdsa;lkfjdsaflo\n\r")      # write a string
        #ser.close()             # close port

    def general_work(self,input_items, output_items):
        out = output_items[0]
        to_read = len(out)

        if to_read > 10:
            to_read = 10

        if(self.wait_for_newline):
            #os.write(2, "spam: about to read %d chars from a line …" % to_read)
            rx = list( self.ser.readline(to_read).rstrip() )
        else:
            #os.write(2, "spam: about to read %d chars …" % to_read)
            rx = list( self.ser.read(to_read) )

        #os.write(2, "\nspam: read this: %s\napplying to out=%s …" % (rx,out))

        out[0:len(rx)] = map(ord,rx)

        #os.write(2, "∎")

        return len(rx)
