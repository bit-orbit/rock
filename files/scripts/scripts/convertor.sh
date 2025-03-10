#!/bin/bash

SOURCE_DIR="files/scripts/raw"

TARGET_DIR="files/musics"

if [ ! -d "$TARGET_DIR" ]; then
  mkdir -p "$TARGET_DIR"
fi

# I did this couse that i can add/remove other convertor simply
./convertors/mp3_convertor.sh
./convertors/m4a_convertor.sh
./convertors/mp4_convertor.sh
./convertors/ogg_convertor.sh
./convertors/wav_convertor.sh
./convertors/flac_convertor.sh
