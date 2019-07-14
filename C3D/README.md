
# Extract video feature

## Instruction

We use C3D model to extract video feature (use Google Colab for free GPU). 
See more on [C3D User guide](https://docs.google.com/document/d/1-QqZ3JHd76JfimY4QKqOojcEaf5g3JS0lNh-FHTxLag/edit).

- Input: video raw mp4
- Output: all fc-6 clip (16 frames) features in video

 1. Compile C3D: see [C3DV0.ipynb](https://github.com/dolongbien/HumanBehaviorBKU/blob/master/C3D/C3DV0.ipynb "C3DV0.ipynb")
 3. Prepare 2 input files from mp4 videos: *input_list_video.txt* and *output_list_video_prefix.txt*. Check out this Python script [generate_inout_file.py](https://github.com/dolongbien/HumanBehaviorBKU/blob/master/C3D/generate_inout_file.py)
 4. Extract C3D feature (use the same jupyter notebook)


After extracting video feature, use Matlab script to convert fc-6 files to txt format of 32 video segments to form a video feature. Check out this Matlab script [Save_C3DFeatures_32Segments.m](https://github.com/dolongbien/HumanBehaviorBKU/blob/master/C3D/Save_C3DFeatures_32Segments.m)
