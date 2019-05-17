import os
from .c3d import *
from .classifier import *
from .utils.visualization_util import *
from celery import task
from keras import backend as K 

@task
def extract_feature_video(video_path):

    K.clear_session()
    video_name = os.path.basename(video_path).split('.')[0]

    # read video
    video_clips, num_frames = get_video_clips(video_path)

    print("Number of clips in the video : ", len(video_clips))

    # build models
    feature_extractor = c3d_feature_extractor()
    classifier_model = build_classifier_model()

    print("Models initialized")

    # extract features
    rgb_features = []
    for i, clip in enumerate(video_clips):
        clip = np.array(clip)
        if len(clip) < params.frame_count:
            continue

        clip = preprocess_input(clip)
        rgb_feature = feature_extractor.predict(clip)[0]
        rgb_features.append(rgb_feature)

        print("Processed clip : ", i)

    rgb_features = np.array(rgb_features)
    
    # bag features
    rgb_feature_bag = interpolate(rgb_features, params.features_per_bag)

    # classify using the trained classifier model
    predictions = classifier_model.predict(rgb_feature_bag)

    predictions = np.array(predictions).squeeze()

    predictions = extrapolate(predictions, num_frames)

    np.save('media/features/{}'.format(video_name), predictions)

    # save_path = os.path.join(cfg.output_folder, video_name + '.gif')
    # visualize predictions
    # visualize_predictions(cfg.sample_video_path, predictions, save_path)


def load_npy(file_path):
    return np.load(file_path)

# extract_feature_video('media/RoadAccidents310_x264.mp4')