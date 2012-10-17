gr-pyserial
===========

Serial Port I/O For GNU Radio.  Simple pyserial wrapper.

===========


For more information:

http://github.com/buoyboy/gr-pyserial/wiki 


Requirements

GNU 
Radio 
gr-extras 
python 
pyserial

*** Installing GNU Radio

See this page:
http://gnuradio.org/redmine/projects/gnuradio/wiki/InstallingGR

*run:
sudo ldconfig (for good measure)


*** Installing grextras

git clone https://github.com/guruofquality/grextras.git
cd grextras
mkdir build
cd build
cmake ../
make 
sudo make install
sudo ldconfig

****Installing pyserial

See this page for up-to-date install instructions:
http://pyserial.sourceforge.net/pyserial.html

But basically:

pip pyserial

**** Installing gr-pyserial

git clone http://github.com/buoyboy/gr-pyserial.git
cd gr-pyserial
mkdir build
cd build
cmake ../
sudo make install

