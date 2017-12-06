close all; clear all; clc;
 
% get number of evaluations
num_evals = size(dir('*.txt'));
num_evals = num_evals(1);

%%
% go through all evals
for i = 1:num_evals
    % scan file
    raw_i = fscanf(fopen(['eval',num2str(i),'.txt']),'%f');
    
    ctr = 1;
    % get baseline wpm
    baseline_wpm = raw_i(ctr);
    ctr = ctr+1;
    
    % iterate through all tests
    for j = 1:4
        eval_mode = raw_i(ctr); ctr=ctr+1;
        
    end
end