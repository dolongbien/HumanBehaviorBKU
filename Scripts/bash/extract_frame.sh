ffmpeg -i RoadAccidents002_x264.mp4 -filter:v     "select='lt(prev_pts*TB\,7)*gte(pts*TB\,7) \
            +lt(prev_pts*TB\,8)*gte(pts*TB\,8)   \
            +lt(prev_pts*TB\,9)*gte(pts*TB\,9) \ + lt(prev_pts*TB\,10)*gte(pts*TB\,10)'"     -vsync drop RA_002_FR_%03d.png
# extract multiple frames in a video with specific timestamp (seconds).
# here is 4 frames at the 7,8,9,10th second.
