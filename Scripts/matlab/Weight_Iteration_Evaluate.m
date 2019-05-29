ScorePath='RoadAccidents002_x264.mat'; % predicted score
VideoPath='RoadAccidents002_x264.mp4';

% Input: video + predicted score
% Output: score for all frame in video --> plot it

%% Load Video
try
    xyloObj = VideoReader(VideoPath);
catch

   error('???')
end

Predic_scores=load(ScorePath);
fps=30;
Actual_frames=round(xyloObj.Duration*fps);

Folder_Path='RoadAccidents002_x264';
AllFiles=dir([Folder_Path,'/*.fc6-1']);
nFileNumbers=length(AllFiles);
nFrames_C3D=nFileNumbers*16;  % As the features were computed for every 16 frames


%% 32 Shots
Detection_score_32shots=zeros(1,nFrames_C3D);
Thirty2_shots= round(linspace(1,length(AllFiles),33));
Shots_Features=[];
p_c=0;

for ishots=1:length(Thirty2_shots)-1

    p_c=p_c+1;
    ss=Thirty2_shots(ishots);
    ee=Thirty2_shots(ishots+1)-1;

    if ishots==length(Thirty2_shots)
        ee=Thirty2_shots(ishots+1);
    end

    if ee<ss
        Detection_score_32shots((ss-1)*16+1:(ss-1)*16+1+15)=Predic_scores.predictions(p_c);   
    else
        Detection_score_32shots((ss-1)*16+1:(ee-1)*16+16)=Predic_scores.predictions(p_c);
    end

end

% Score of video
Final_score=  [Detection_score_32shots,repmat(Detection_score_32shots(end),[1,Actual_frames-length(Detection_score_32shots)])];

% Plot the score
feature('DefaultCharacterSet', 'UTF8') % for Vietnamese suport
figure
plot(Final_score)
title('?i?m s? c?a video ? vòng l?p 1000')
xlabel('S? khung hình') 
ylabel('?i?m s? b?t th??ng')


