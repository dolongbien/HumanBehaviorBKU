clc
clear all
close all


fid = fopen('Temporal_Annotations_1\Temporal_Anomaly_Annotation.txt','r');
tline = fgetl(fid);

while ischar(tline)
    X_data = textscan(tline,'%s');
    celldisp(X_data)
    A = [str2num(X_data{1}{3}) str2num(X_data{1}{4})]
    Annotation_file = struct('VideoName', X_data{1}{1}, 'Anno', A, 'EventName', X_data{1}{2})
    
    if str2num(X_data{1}{5}) ~= -1
        A = [str2num(X_data{1}{3}) str2num(X_data{1}{4}); str2num(X_data{1}{5}) str2num(X_data{1}{6})] 
        Annotation_file = struct('VideoName', X_data{1}{1}, 'Anno', A, 'EventName', X_data{1}{2})
    end
    
    path=['Temporal_Annotations/',X_data{1}{1}(1:end-4),'.mat'];
    save(path, 'Annotation_file')
    tline = fgetl(fid);
end