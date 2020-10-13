# About
This solution is based on [Kaldi](http://kaldi-asr.org) toolkit. 
It uses [gstreamer plugin](https://github.com/alumae/gst-kaldi-nnet2-online) that wraps Kaldi's SingleUtteranceNnet*Decoder. 
Requires iVector-adapted DNN acoustic models.

# Supported Platforms

- Ubuntu

# Installation (Estimated time: 2-3 hours)
This Kaldi installation [tutorial](http://jrmeyer.github.io/asr/2016/01/26/Installing-Kaldi.html) might be useful as well (note that you do not need iRLSTM).
## 1. Ubuntu packages
* `sudo apt-get update`
* `sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools libgstreamer1.0-dev gstreamer1.0-libav libtool-bin`
* `sudo apt install pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev libatlas3-base`

## 2. Kaldi
1. Clone [repo](https://github.com/kaldi-asr/kaldi): `git clone https://github.com/kaldi-asr/kaldi.git`
2. Use the stable revision `6c816e5` for compilation: `git checkout 6c816e5`
3. Compile it. [Read](https://github.com/kaldi-asr/kaldi/blob/master/INSTALL) `INSTALL` file for instructions

## 3. Kaldi GStream Plugin
1. Clone [repo](https://github.com/alumae/gst-kaldi-nnet2-online) `git clone https://github.com/alumae/gst-kaldi-nnet2-online.git`
2. Use the revision `14cd7c3d`
3. Compile it. Follow the [instructions](https://github.com/alumae/gst-kaldi-nnet2-online/blob/master/README.md#how-to-compile-it) in `README.md`
4. Set `GST_PLUGIN_PATH` environment variable pointing to directory containg `libgstkaldinnet2onlinedecoder.so` (by default `/path/to/gst-kaldi-nnet2-online/src`)

## 4. Pre-trained Models
The models are located at out local git-lfs storage thus you need to fetch them.
* `git lfs checkout`