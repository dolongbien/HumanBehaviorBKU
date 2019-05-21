clc
clear all
close all

% This code save already computed C3D features into 32 (video features) segments.
% We assume that C3D features for a video are already computed. We use
% default settings for computing C3D features, i.e., we compute C3D features for
% every 16 frames and obtain the features from fc6.
 
C3D_Path='C:\Users\DLBien\Desktop\TEST_FC';
C3D_Path_Seg='C:\Users\DLBien\Desktop\OUTPUT_TXT';

 
if ~exist(C3D_Path_Seg,'dir')
     mkdir(C3D_Path_Seg)
end
 

All_Folder=dir(C3D_Path);
All_Folder=All_Folder(3:end);
subcript='_C.txt';

for ifolder=1:length(All_Folder)
    %% START 1 LOOP WITH 1 FC FOLDER, ex: Abuse028 has N=1392 frames
    
    Folder_Path=[C3D_Path,'/',All_Folder(ifolder).name];
    %Folder_Path is path of a folder which contains C3D features (for every 16 frames) for a paricular video.
    % N=1392 frames --> it has [1392/16] = 88 fc6-1 files
    
    AllFiles=dir([Folder_Path,'/*.fc6-1']); 
    % fc6-1 files in feature directory, each file = a clip in video
    % one clip = 16 frames
    if length(AllFiles) == 0
        continue
    end
    Feature_vect=zeros(length(AllFiles),4096); 
    % each fc6-1 = 1 clips 16 frames = 4096-d ==> Total is [N/16]=88 clips like that
    %% Iterate each fc6-1 file (16 frames each)
    for ifile=1:length(AllFiles) 
      FilePath=[Folder_Path,'/', AllFiles(ifile).name];  
      [s, data] = read_binary_blob(FilePath); % return s=shape of tensor, data=4096-d feature of clip
      Feature_vect(ifile,:)=data; % 1 column 4096-d in 88x4096 is assign by 1 clip feature (4096)
      clear data
    end
    %% At this point, Feature vector is filled with all actual data from
    % all 16-frame clips in video, each clip is 4096-d, therefore 88x4096
    % is now filled with actual data
      if sum( Feature_vect(:))==0
           error('??')
      end
      
      
  % Write C3D features in text file to load in
  % Training_AnomalyDetector_public ( You can directly use .mat format if you want).
   txt_file_name = [C3D_Path_Seg,'/',All_Folder(ifolder).name,subcript];
   % feature txt name i.e Abuse028_x264_C.txt
   if exist(txt_file_name, 'file')
       continue
   end
   fid1=fopen(txt_file_name,'w'); 
    % sum(x,1) = sum vertically (column)
    % sum(x,2) = sum horizontally (row)
   if ~isempty(find(sum(Feature_vect,2)==0)) % sum row --> 88x4096 results in 88 rows
         error('??')
   end


  if ~isempty(find(isnan(Feature_vect(:))))
         error('??')
  end

  if ~isempty(find(Feature_vect(:)==Inf))
         error('??')
  end
      
    
   
  %% 32 Segments
     
     Segments_Features=zeros(32,4096); %32 row, 4096 column
     thirty2_shots= round(linspace(1,length(AllFiles),33)); 
     % thirty2shots = divide 88 frames to 33 segment, start from 1 to 88
     % SO: thirty2shots = [1 , 4, 6, 10, ..... 83, 85, 88], total elements
     % is 33, vector 1x33
     count=0;
     %% WRITE 88x4096 TO 32x4096
     for ishots=1:length(thirty2_shots)-1 % ishorts starts from 1 to 32
        
        ss=thirty2_shots(ishots); % start clip index in 88x4096
        ee=thirty2_shots(ishots+1)-1; % end clip index in 88x4096
        if ishots==length(thirty2_shots)
            ee=thirty2_shots(ishots+1);
        end
        
         %% THIS IS A FEATURE FOR 1 SEGMENT
         %ALL BELOW CASE, temp_vect is always 4096-d based on value of start ss and end ee index
        if ss==ee
        
            temp_vect=Feature_vect(ss:ee,:); % ss==ee --> get 1 vector 4096-d from 88x4096
            
        elseif ee<ss
           
           temp_vect=Feature_vect(ss,:); % ee < ss --> get 1 vector 4096-d from 88x4096
            
        else
            temp_vect=mean(Feature_vect(ss:ee,:)); 
            % ss < ee --> get all clip vectors from ss to ee (ex: 3 vectors) from 88x4096
            % origin feature, than take mean value of all (i.e 3 vectors) that vectors to
            % get a new one has 4096-d (shape of result is shape of row when get mean a
            % matrix)
            %mean a vector = mean of each column = sum column/total row -->
            %shape = number of row (=4096) after this mean operation
        end
        
        %% AFTER HAS 1 SEGMENT FEATURE,  CALCULATE NORM-2 (L2)
        temp_vect=temp_vect/norm(temp_vect); % divide by norm-2 (L2) of vector (Euclidean norm)=cumsum(sqrt(x[i]^2))
        
        if norm(temp_vect)==0
           error('??')
        end
        
        
        count=count+1; % next segment (max=32)
        Segments_Features(count,:)=temp_vect; % push each segment feature to final 32 video segments feature
        
        
     end
    
  %verify
  
      if ~isempty(find(sum(Segments_Features,2)==0))
             error('??')
      end
  
     
      if ~isempty(find(isnan(Segments_Features(:))))
             error('??')
      end
    
      if ~isempty(find(Segments_Features(:)==Inf))
             error('??')
      end
      
 % save 32 segment features in text file ( You can directly save and load .mat file in python as well).
 
     for ii=1:size(Segments_Features,1)
         feat_text=Segments_Features(ii,:);%(Feature_vect(ii,:));
         fprintf (fid1,'%f ',feat_text);
         fprintf (fid1,'\n'); 
     end
     
  fclose(fid1);
  
  
  
end
    

    
