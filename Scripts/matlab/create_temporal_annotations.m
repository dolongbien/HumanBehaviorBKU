clc
clear all
close all


fid = fopen('Temporal_Annotations_1\Temporal_RoadAccidents_Annotation.txt','r');
tline = fgetl(fid);

while ischar(tline)
    X_data = textscan(tline,'%s');
    celldisp(X_data);
    A = [str2double(X_data{1}{3}) str2double(X_data{1}{4})];
    Annotation_file = struct('VideoName', X_data{1}{1}, 'Anno', A, 'EventName', X_data{1}{2});
    
    if str2double(X_data{1}{5}) ~= -1
        A = [str2double(X_data{1}{3}) str2double(X_data{1}{4}); str2double(X_data{1}{5}) str2double(X_data{1}{6})]; 
        Annotation_file = struct('VideoName', X_data{1}{1}, 'Anno', A, 'EventName', X_data{1}{2});
    end
    
    path=['Temporal_Annotations_2/',X_data{1}{1}(1:end-4),'.mat'];
    save(path, 'Annotation_file');
    tline = fgetl(fid);
end