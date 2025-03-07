#!/bin/bash

# Source directory (replace with your actual directory)
SOURCE_DIR="./raw"

# Target directory
TARGET_DIR="files/musics"

# Check if the target directory exists, create it if not
if [ ! -d "$TARGET_DIR" ]; then
  mkdir -p "$TARGET_DIR"
fi

# Find all files in the source directory
find "$SOURCE_DIR" -type f -print0 | while IFS= read -r -d $'\0' file; do
  # Determine if the file is an audio file (using ffmpeg's ability to probe)
  if ffmpeg -i "$file" -f null - 2>/dev/null; then # ffmpeg returns 0 if it can read the file
      # Extract the filename without the extension
      filename=$(basename "$file")
      extension="${filename##*.}"
      filename="${filename%.*}"

      # Construct the output filename
      output_file="$TARGET_DIR/$filename.opus"

      # Convert the file using ffmpeg
      ffmpeg -i "$file" -c:a libopus "$output_file"

      # Check if the conversion was successful
      if [ $? -eq 0 ]; then
        echo "Converted: $file -> $output_file"
      else
        echo "Error converting: $file"
      fi
  else
    echo "Skipping non-audio file: $file"
  fi
done

echo "Conversion process completed."