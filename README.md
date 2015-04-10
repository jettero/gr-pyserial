gr-pyserial
===========

Serial Port I/O For GNU Radio.  Simple pyserial wrapper.

This branch is all jacked up by jettero.  The original package wouldn't work at
all in GNU Radio 3.7 — gr.extras was removed and pmt (etc) was made native.  The
pmt stuff couldn't be made to work without a lotta research and I only needed a
serial source … I had no idea what the circular serial setup was even for.

So I stripped out most of the gr.extras stuff (and the pmt stuff) and even
stripped out the inputs (that wouldn't have been easy to fix anyway).

I made a straight-up boring byte source that I'll feed to other blocks.

Please see the original gr-pyserial if you need their setup or are using GNU
Radio 3.6.  The original original is gone, near as I can tell, but you can look
at the branch I forked from or my master branch.

===========

Requirements

GNU Radio 3.7
python 
pyserial

*Installing GNU Radio*

maybe just run:
sudo apt-get install gnuradio

or maybe see this page:
http://gnuradio.org/redmine/projects/gnuradio/wiki/InstallingGR


*Installing pyserial*

See this page for up-to-date install instructions:
http://pyserial.sourceforge.net/pyserial.html

But basically:

pip pyserial


*Installing gr-pyserial*

git clone http://github.com/jettero/gr-pyserial.git
cd gr-pyserial
grwd="$(pwd)"
mkdir /tmp/gr-pyserial
cd /tmp/gr-pyserial
# skip the -DMAKE_INSTALL_PREFIX if you want /usr/local
cmake -DCMAKE_INSTALL_PREFIX=/usr "$grwd"
sudo make install

# *or* just use my build script
bash build.sh /my/install/prefix/here
