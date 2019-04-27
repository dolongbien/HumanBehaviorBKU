clc
clear all
close all
 

C3D_CNN_Path='/home/dlbien/Documents/AnomalyDetectionCVPR2018/Testing_FC_RoadAccident'; % C3D features for videos
Testing_VideoPath='/home/dlbien/Documents/AnomalyDetectionCVPR2018/TestingVideo_RoadAccident'; % Path of mp4 videos
AllAnn_Path='/home/dlbien/Documents/AnomalyDetectionCVPR2018/Temporal_Annotation_RoadAccident'; % Path of Temporal Annotations
Model_Score_Folder='/home/dlbien/Documents/AnomalyDetectionCVPR2018/EvalRoadAcc_Architect02_20K';  % Path of Pretrained Model score on Testing videos (32 numbers for 32 temporal segments)
Paper_Results='/home/dlbien/Documents/AnomalyDetectionCVPR2018/Eval_Res';   % Path to save results.
 
All_Videos_scores=dir(Model_Score_Folder);
All_Videos_scores=All_Videos_scores(3:end);
nVideos=length(All_Videos_scores);
frm_counter=1;
All_Detect=zeros(1,1000000); % array preallocated to speedup allocatd complexity
All_GT=zeros(1,1000000);
% test whether All_Detect variable holds score of all Testing videos
% HOW?: compare length of All_Detect with cumsum of total frame in all Testing
% videos
total_frame_all_video = 0;
for ivideo=1:nVideos
    ivideo

    Ann_Path=[AllAnn_Path,'/',All_Videos_scores(ivideo).name(1:end-4),'.mat'];
    load(Ann_Path)
    check=strmatch(All_Videos_scores(ivideo).name(1:end-6),Annotation_file.VideoName(1:end-3));
    if isempty(check)
         error('????') 
    end

    VideoPath=[Testing_VideoPath,'/', All_Videos_scores(ivideo).name(1:end-4),'.mp4'];
    ScorePath=[Model_Score_Folder,'/', All_Videos_scores(ivideo).name(1:end-4),'.mat'];

  %% Load Video
    %xyloObj = VideoReader(VideoPath);
    
    try
        xyloObj = VideoReader(VideoPath);
    catch
       error(strcat('Load video error???', VideoPath))
       
    end

    Predic_scores=load(ScorePath); % from model, 1x32 segment
    fps=30;
    Actual_frames=round(xyloObj.Duration*fps);
    % BIEN: cumsum to compare at the end
    total_frame_all_video = total_frame_all_video + Actual_frames;
    Folder_Path=[C3D_CNN_Path,'/',All_Videos_scores(ivideo).name(1:end-4)];
    AllFiles=dir([Folder_Path,'/*.fc6-1']);
    nFileNumbers=length(AllFiles); % number of fc-6 file
    nFrames_C3D=nFileNumbers*16;  % As the features were computed for every 16 frames
    % between 2 fc-6 file is 16 frames --> total frame is 16*(total fc6 file)

%% 32 Shots
    Detection_score_32shots=zeros(1,nFrames_C3D); % all every single frames 1xtotalframe
    Thirty2_shots= round(linspace(1,length(AllFiles),33)); % 32 segments 1x33
    Shots_Features=[]; % score for each segment
    p_c=0;

    for ishots=1:length(Thirty2_shots)-1

        p_c=p_c+1;
        ss=Thirty2_shots(ishots); %ss = start??
        ee=Thirty2_shots(ishots+1)-1; %%ee = end??

        if ishots==length(Thirty2_shots)
            ee=Thirty2_shots(ishots+1);
        end

        if ee<ss
            Detection_score_32shots((ss-1)*16+1:(ss-1)*16+1+15)=Predic_scores.predictions(p_c);   
        else
            Detection_score_32shots=Predic_scores.predictions(p_c);
        end

    end


    Final_score=  [Detection_score_32shots,repmat(Detection_score_32shots(end),[1,Actual_frames-length(Detection_score_32shots)])];
    GT=zeros(1,Actual_frames);

    for ik=1:size(Annotation_file.Anno,1)
            st_fr=max(Annotation_file.Anno(ik,1),1); % starting frame
            end_fr=min(Annotation_file.Anno(ik,2),Actual_frames); % ending frame
            GT(st_fr:end_fr)=1;
    end


    if Annotation_file.Anno(1,1)== -1   % For Normal Videos  WHY 0.05 ??? 
        GT=zeros(1,Actual_frames);
    end

    % All_Detect is the score for all Testing video (i.e 63 videos), each
    % video score is appended to All_Detect variable then increase the
    % frm_counter to go to the begining index of the next video (for loop)
    All_Detect(frm_counter:frm_counter+length(Final_score)-1)=Final_score; % score for current video
    All_GT(frm_counter:frm_counter+length(Final_score)-1)=GT;% Groud truth for all Testing videos
    frm_counter=frm_counter+length(Final_score); % starting index of the next video


end
frm_counter
total_frame_all_video %  exactly, size of All_Detect = size of cumsum frame = frame counter here
All_Detect=(All_Detect(1:frm_counter-1));
All_GT=All_GT(1:frm_counter-1);
scores=All_Detect;
[so,si] = sort(scores,'descend'); % score order and score index; In that way, scores(si) = so
tp=All_GT(si)>0;
fp=All_GT(si)==0;
tp=cumsum(tp);
fp=cumsum(fp);
nrpos=sum(All_GT); % number of positive
rec=tp/nrpos; 
fpr=fp/sum(All_GT==0);
prec=tp./(fp+tp);
AUC1 = trapz(fpr ,rec );
% You can also use the following codes
[X,Y,T,AUC] = perfcurve(All_GT,All_Detect,1);
% LABELS, SCORES, POSITIVE CLASS LABEL
[X2,Y2,T2,AUC2] = perfcurve(All_GT,All_Detect,1, 'tvals', 0.5);
missrate = 1-Y2;
[X3,Y3,T3,AUC3] = perfcurve(All_GT,All_Detect,1, 'xcrit', 'fnr');
save RoadArch02_20K_L1 AUC X Y
