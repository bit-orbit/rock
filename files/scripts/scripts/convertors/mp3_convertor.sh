#!/bin/bash

SOURCE_DIR="./raw"

# Target directory
TARGET_DIR="files/musics"

# Check if the target directory exists, create it if not
if [ ! -d "$TARGET_DIR" ]; then
  mkdir -p "$TARGET_DIR"
fi

# Find all files in the source directory
find "$SOURCE_DIR" -type f -iname "*mp3" -exec ffmpeg -y -i {} {}.opus \;

# Move all opus file to musics dir
mv "$SOURCE_DIR"/*opus files/musics/
