=======
mkdir -p output/c3d/Shoplifting028_x264
mkdir -p output/c3d/Shoplifting033_x264
mkdir -p output/Shoplifting033_x264
>>>>>>> 8a98b66f0aa551e5978bc0b223277b327383eb75
GLOG_logtosterr=1 ../../build/tools/extract_image_features.bin prototxt/c3d_sport1m_feature_extractor_video.prototxt conv3d_deepnetA_sport1m_iter_1900000 0 50 1 prototxt/output_list_video_prefix.txt fc7-1 fc6-1 prob
