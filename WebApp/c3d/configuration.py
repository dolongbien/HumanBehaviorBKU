# c3d_model_weights = 'c3d/trained_models/c3d_sports1m.h5'
# classifier_model_json = './trained_models/model.json'

# input_folder  = './input'
# output_folder = './output'

c3d_mean_path = 'c3d/trained_models/c3d_mean.npy'

# sample_video_path = 'media/RoadAccidents310_x264.mp4'

no_segment = 32
model_dir = 'c3d/trained_models/'

weight32_path = model_dir + 'weights_32_AnomalyL1L2_10000_roadaccidents2.mat'
weight64_path = model_dir + 'weights_64_Seg_RoadAccident_Loss1_15000.mat'

weight_default_path = weight32_path

model_name = "model.json"
feature32_alias = '_C.txt'
feature64_alias = '_64seg_C.txt'

c3d_model_weights = model_dir + 'c3d_sports1m.h5'
