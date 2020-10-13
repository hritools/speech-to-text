#!/bin/bash
# Move to the library first
cd $7

# Start recognizing
gst-launch-1.0 filesrc location=$1 ! \
  kaldinnet2onlinedecoder \
    use-threaded-decoder=false \
    nnet-mode=3 \
    word-syms=$2 \
    feature-type=mfcc \
    mfcc-config=$3 \
    ivector-extraction-config=$4 \
    max-active=10000 \
    beam=12.0 \
    lattice-beam=6.0 \
    do-endpointing=true \
    endpoint-silence-phones="1:2:3:4:5:6:7:8:9:10" \
    acoustic-scale=1.0 \
    frame-subsampling-factor=3 \
    frames-per-chunk=51 \
    fst=$5 \
    model=$6 \
  ! filesink location=$1.txt buffer-mode=2