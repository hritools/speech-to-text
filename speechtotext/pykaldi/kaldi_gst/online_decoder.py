#!/usr/bin/env python
#
# Copyright (c) 2013 Tanel Alumae
# Copyright (c) 2008 Carnegie Mellon University.
#
# Inspired by the CMU Sphinx's Pocketsphinx Gstreamer plugin demo (which has BSD license)
#
# Licence: BSD
import asyncio
import sys
import os
import threading
from threading import Thread

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initializing threads used by the Gst various elements
# GObject.threads_init()
# Initializes the GStreamer library, setting up internal path lists, registering built-in elements, and loading
# standard plugins.
Gst.init(None)


class Decoder(object):
    """GStreamer/Kaldi Demo Application"""

    def __init__(self, appsrc, ws):
        """Initialize the speech components"""
        self.send = threading.Event()
        self.ws = ws
        self.hyp = []
        self.alive = True
        Thread(target=self.send_result, args=()).start()

        self.pipeline = Gst.Pipeline()
        self.appsrc = appsrc

        if self.appsrc is None:
            print("Error loading appsrc")
            sys.exit()

        self.decodebin = Gst.ElementFactory.make("decodebin", "decodebin")
        self.decodebin.connect("pad-added", self.decode_src_created)

        self.audioconvert = Gst.ElementFactory.make("audioconvert", "audioconvert")
        self.audioresample = Gst.ElementFactory.make("audioresample", "audioresample")

        self.asr = Gst.ElementFactory.make("kaldinnet2onlinedecoder", "asr")
        self.sink = Gst.ElementFactory.make("filesink", "filesink")
        self.sink.set_property('location', 'audio/output.txt')
        self.sink.set_property('buffer-mode', 2)
        self.setup_asr()

        # initially silence the decoder
        self.asr.set_property("silent", True)

        for element in [self.appsrc, self.decodebin, self.audioconvert,
                        self.audioresample, self.asr, self.sink]:
            self.pipeline.add(element)
        self.appsrc.link(self.decodebin)
        # self.decodebin.link(self.audioconvert)
        self.audioconvert.link(self.audioresample)
        self.audioresample.link(self.asr)
        self.asr.link(self.sink)

        self.asr.connect('partial-result', self._on_partial_result)
        self.asr.connect('final-result', self._on_final_result)

    def close_gst(self):
        print('destroying decoder')
        # To switch sending thread off
        self.alive = False
        self.send.set()

        self.appsrc.unref()
        self.decodebin.unref()
        self.audioconvert.unref()
        self.audioresample.unref()
        self.asr.unref()
        self.sink.unref()
        self.pipeline.unref()

    # handler taking care of linking the decoder's newly created source pad to the sink
    def decode_src_created(self, element, pad):
        print('created the decodebin pad')
        pad.link(self.audioconvert.get_static_pad("sink"))

    def setup_asr(self):
        if self.asr:
            # IMPORTANT!! Do not touch the order of these parameters -
            #   it may slow down your program by a factor of 30, or even crash it
            self.asr.set_property("use-threaded-decoder", False)
            self.asr.set_property("nnet-mode", 3)
            self.asr.set_property("word-syms", "kaldi_gst/tdnn/graph/words.txt")
            self.asr.set_property("feature-type", "mfcc")
            self.asr.set_property("mfcc-config", "kaldi_gst/tdnn/conf/mfcc.conf")
            self.asr.set_property("ivector-extraction-config", "kaldi_gst/tdnn/conf/ivector_extractor.conf")

            self.asr.set_property("max-active", 10000)
            self.asr.set_property("beam", 12.0)
            self.asr.set_property("lattice-beam", 6.0)
            self.asr.set_property("do-endpointing", True)
            self.asr.set_property("endpoint-silence-phones", "1:2:3:4:5:6:7:8:9:10")

            self.asr.set_property("acoustic-scale", 1.0)
            self.asr.set_property("frame-subsampling-factor", 3)
            self.asr.set_property("frames-per-chunk", 51)

            self.asr.set_property("fst", "kaldi_gst/tdnn/graph/HCLG.fst")
            self.asr.set_property("model", "kaldi_gst/tdnn/final.mdl")
            # self.asr.set_property("chunk-length-in-secs", 0.2)
        else:
            print("Couldn't create the kaldinnet2onlinedecoder element. ")
            if "GST_PLUGIN_PATH" in os.environ:
                print("Have you compiled the Kaldi GStreamer plugin?", os.environ["GST_PLUGIN_PATH"])
            else:
                print("You probably need to set the GST_PLUGIN_PATH envoronment variable")
                print("Try running: GST_PLUGIN_PATH=../src %s" % sys.argv[0])
            sys.exit()

    def send_result(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.send.clear()
        while self.alive:
            self.send.wait()
            self.send.clear()
            while self.hyp:
                self.ws.send(self.hyp.pop(0))
        print('finalizing send result')
        loop.close()

    def _on_partial_result(self, asr, hyp):
        """Delete any previous selection, insert text and select it."""
        self.hyp.append('p ' + hyp)
        self.send.set()

    def _on_final_result(self, asr, hyp):
        """Insert the final result."""
        self.hyp.append('f ' + hyp)
        self.send.set()

    def listen(self):
        """Start listening."""
        print('listening')
        self.asr.set_property("silent", False)
        self.pipeline.set_state(Gst.State.PLAYING)

    def silence(self):
        """Stop listening."""
        print('stop listening')
        self.asr.set_property("silent", True)

    def eos(self):
        self.pipeline.send_event(Gst.Event.new_eos())

    def _on_error(self, bus, msg):
        print('Error {}: {}, {}'.format(msg.src.name, *msg.parse_error()))
