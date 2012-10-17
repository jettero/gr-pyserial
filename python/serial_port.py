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
from math import pi
from gnuradio import gr
from gruel import pmt
import gnuradio.extras #brings in gr.block
import serial
import thread


NONE = 0
EVEN = 1 
ODD = 2

STOPBITS_ONE = 0
STOPBITS_TWO = 1

WORD_SIZE_7 = 0 
WORD_SIZE_8 = 1

# /////////////////////////////////////////////////////////////////////////////
#                   Serial Port
# /////////////////////////////////////////////////////////////////////////////

class serial_port(gr.block):
    """
    Provides serial port connection within GNU Radio flowgraph
    """
    def __init__(
        self,device,parity,baudrate,stopbits,bytesize,wait_for_newline
    ):
        """
        Serial port w/ blobs in and out
        """

        gr.block.__init__(
            self,
            name = "serial_port",
            in_sig = None,
            out_sig = None,
            num_msg_inputs = 1,
            num_msg_outputs = 1,
        )
    
        self.mgr = pmt.pmt_mgr()
        for i in range(64):
            self.mgr.set(pmt.pmt_make_blob(10000))
        
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

    def rx_work(self,ser):
        while(1):
            try: msg = self.pop_msg_queue()
            except: return -1

            if not pmt.pmt_is_blob(msg.value):
                continue

            blob = pmt.pmt_blob_data(msg.value)
            
            tx_string = pmt.pmt_blob_data(msg.value).tostring()
            
            ser.write(tx_string)

    def tx_work(self,ser):
        while(1):
            if(self.wait_for_newline):
                rx_buf = ser.readline()
            else:
                rx_buf = ser.read()
            blob = self.mgr.acquire(True) #block
            pmt.pmt_blob_resize(blob, len(rx_buf))
            pmt.pmt_blob_rw_data(blob)[:] = numpy.fromstring(rx_buf, dtype='uint8')
            self.post_msg(0, pmt.pmt_string_to_symbol('serial'), blob)

    def work(self, input_items, output_items):
                
        thread.start_new_thread( self.rx_work,  (self.ser , ))
        thread.start_new_thread( self.tx_work, (self.ser , ))

        while(1): 
            try:
                a =0
            except:
                print "exiting"
                return -1
