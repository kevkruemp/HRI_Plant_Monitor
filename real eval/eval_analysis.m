close all; clear all; clc;
 
% get number of evaluations
num_evals = size(dir('*.txt'));
num_evals = num_evals(1);

%% process raw data
close all; 
% go through all evals
wpm = zeros(num_evals,5);
t_delay = cell(num_evals,4);
t_delay_mean = zeros(num_evals,4);
num_cmd = zeros(num_evals,4);
for i = 1:num_evals
    % scan file
    raw_i = fscanf(fopen(['eval',num2str(i),'.txt']),'%f');
    
    ctr = 1;
    % get baseline wpm
    baseline_wpm = raw_i(ctr);
    wpm(i,1) = baseline_wpm;
    ctr = ctr+1;
    
    % iterate through all tests
    for j = 1:4
        eval_mode = raw_i(ctr); ctr=ctr+1;
        t_delay_i = [];
        while(raw_i(ctr)~=floor(raw_i(ctr)))
            t_delay_i = [t_delay_i, raw_i(ctr)]
            ctr=ctr+1;
        end
        % time delay
        t_delay{i,eval_mode} = t_delay_i;
        t_delay_mean(i,eval_mode) = mean(t_delay_i);
        
        % wpm
        wpm_em = raw_i(ctr); ctr=ctr+1;
        wpm(i,eval_mode+1) = wpm_em;
        
        % number commands
        num_cmd(i,eval_mode) = length(t_delay_i);
    end
    
    % plot wpm change
    subplot(3,1,1); hold on; grid on;
    plot([1:4],wpm(i,2:end)-baseline_wpm,'-');
    xlabel('Evaluation mode');
    ylabel('Mean \Delta wpm');
    
    % plot mean delays
    subplot(3,1,2); hold on; grid on;
    plot([1:4],t_delay_mean(i,:),'-');
    xlabel('Evaluation mode');
    ylabel('Mean time delay (s)');
    
    % plot num cmds
    subplot(3,1,3); hold on; grid on;
    plot([1:4],num_cmd(i,:),'-');
    xlabel('Evaluation mode');
    ylabel('Mean number of commands');
end
t_delay_mean
del_wpm = wpm(:,2:5)-repmat(wpm(:,1),[1,4]);
%% comparisons between eval modes
if (length(t_delay_mean)==num_evals)
    % add avg delay in new row
    t_delay_mean = [t_delay_mean; zeros(1,4)];
    del_wpm = [del_wpm; zeros(1,4)];
    for i = 1:4
        t_delay_mean(num_evals+1,i) = mean(t_delay_mean(1:num_evals,i));
        del_wpm(num_evals+1,i) = mean(del_wpm(1:num_evals,i));
        num_cmd(num_evals+1,i) = mean(num_cmd(1:num_evals,i));
    end
end
t_delay_mean
del_wpm
num_cmd

subplot(3,2,1); grid on;
plot([1:4],t_delay_mean(end,:),'-'); grid on;
ylabel('Mean time delay (s)');
% pbaspect([2 1 1])

subplot(3,2,3); grid on;
plot([1:4],del_wpm(end,:),'-'); grid on;
ylabel('Mean \Delta wpm');
% pbaspect([2 1 1])

subplot(3,2,5); grid on;
plot([1:4],num_cmd(end,:),'-');
ylabel('Mean # cmds'); grid on;
xlabel('Evaluation mode');
% pbaspect([2 1 1])

% saveas(gcf,'raw_data.jpg');

%% stats
% close all;
t_delay_tbl = [t_delay_mean(end,1:2);t_delay_mean(end,3:4)];
del_wpm_tbl = [del_wpm(end,1:2);del_wpm(end,3:4)];
num_cmd_tbl = [num_cmd(end,1:2);num_cmd(end,3:4)];

[p_t_delay_mean,tbl_t_delay_mean] = anova2(t_delay_tbl,1);
[p_del_wpm,tbl_del_wpm] = anova2(del_wpm_tbl,1);
[p_num_cmd,tbl_num_cmd] = anova2(num_cmd_tbl,1);

figure;
subplot(3,2,1); grid on;
plot([1:4],t_delay_mean(end,:),'-'); grid on;
ylabel('Mean time delay (s)');
% pbaspect([2 1 1])

subplot(3,2,3); grid on;
plot([1:4],del_wpm(end,:),'-'); grid on;
ylabel('Mean \Delta wpm');
% pbaspect([2 1 1])

subplot(3,2,5); grid on;
plot([1:4],num_cmd(end,:),'-');
ylabel('Mean # cmds'); grid on;
xlabel('Evaluation mode');
% pbaspect([2 1 1])

% saveas(gcf,'raw_data.jpg');

% Alexa
% figure;
subplot(3,2,2); hold on; grid on;
plot([1:2],t_delay_tbl(1,1:2),'b');
plot([1:2],t_delay_tbl(2,1:2),'b-.');
legend({'B=0','B=1'},'location','northwest');
axis([0, 3, min(min(t_delay_tbl)),max(max(t_delay_tbl))])
xticks([0, 1, 2, 3]);
xticklabels({'','A=0','A=1',''});
ylabel('Mean time delay (s)');
% pbaspect([2 1 1])

subplot(3,2,4); hold on; grid on;
plot([1:2],del_wpm_tbl(1,1:2),'b');
plot([1:2],del_wpm_tbl(2,1:2),'b-.');
legend({'B=0','B=1'},'location','northwest');
axis([0, 3, min(min(del_wpm_tbl)),max(max(del_wpm_tbl))])
xticks([0, 1, 2, 3]);
xticklabels({'','A=0','A=1',''});
ylabel('Mean \Delta wpm');
% pbaspect([2 1 1])

subplot(3,2,6); hold on; grid on;
plot([1:2],num_cmd_tbl(1,1:2),'b');
plot([1:2],num_cmd_tbl(2,1:2),'b-.');
legend({'B=0','B=1'},'location','northwest');
axis([0, 3, min(min(num_cmd_tbl)),max(max(num_cmd_tbl))])
xticks([0, 1, 2, 3]);
xticklabels({'','A=0','A=1',''});
ylabel('Mean # cmds');
% pbaspect([2 1 1])

fig = gcf;
% fig.PaperPosition = [0,0,300,100];
saveas(gcf,'raw_interaction.jpg')
% 
% % Blossom
% subplot(3,2,2); hold on; grid on;
% plot([1:2],t_delay_tbl(1:2,1),'b');
% plot([1:2],t_delay_tbl(1:2,2),'b-.');
% legend({'A=0','A=1'},'location','southwest');
% axis([0, 3, min(min(t_delay_tbl)),max(max(t_delay_tbl))])
% xticks([0, 1, 2, 3]);
% xticklabels({'','B=0','B=1',''});
% 
% subplot(3,2,4); hold on; grid on;
% plot([1:2],del_wpm_tbl(1:2,1),'b');
% plot([1:2],del_wpm_tbl(1:2,2),'b-.');
% legend({'A=0','A=1'},'location','northwest');
% axis([0, 3, min(min(del_wpm_tbl)),max(max(del_wpm_tbl))])
% xticks([0, 1, 2, 3]);
% xticklabels({'','B=0','B=1',''});
% 
% subplot(3,2,6); hold on; grid on;
% plot([1:2],num_cmd_tbl(1:2,1),'b');
% plot([1:2],num_cmd_tbl(1:2,2),'b-.');
% legend({'A=0','A=1'},'location','northwest');
% axis([0, 3, min(min(num_cmd_tbl)),max(max(num_cmd_tbl))])
% xticks([0, 1, 2, 3]);
% xticklabels({'','B=0','B=1',''});


%% survey
close all
% order
% alexa - blossom
% useful, beneficial, valuable, helpful
% sociable, personal, life-like, sensitive
s = csvread('survey.csv',1)

% sum all columns
s_sums = sum(s,1);
% split into sections
alexa_sur = s(:,1:8);
alexa_use = alexa_sur(:,1:4);
alexa_per = alexa_sur(:,5:8);
blossom_sur = s(:,9:16);
blossom_use = blossom_sur(:,1:4);
blossom_per = blossom_sur(:,5:8);
enjoy_tbl = [s_sums(19:20);s_sums(21:22)]
use_tbl = [s_sums(23:24);s_sums(25:26)]

figure; hold on;
b1 = bar([1:8],[s_sums(1:8);s_sums(9:16)]');
xticks(1:8);
xticklabels({'Useful','Beneficial','Valuable','Helpful',...
            'Sociable','Personal','Life-like','Sensitive'});
ylabel('Sum of scores');
set(b1(1), 'FaceColor','b')
set(b1(2), 'FaceColor','r')
legend('Alexa', 'Blossom')
saveas(gcf,'survey.jpg');
% bar([1:8],s_sums(9:16),'r');

%
figure; hold on;
b2 = bar([1:4],[s_sums(19:22);s_sums(23:26)]');
xlabel('Evaluation mode');
ylabel('Sum of ranks');
set(b2(1), 'FaceColor','b')
set(b2(2), 'FaceColor','r')
legend('Enjoyment','Usefulness')
saveas(gcf,'enjoy_use.jpg');

%% stats
clc;
for i = 1:8
    [h,p,ci,stats]=ttest(alexa_sur(:,i),blossom_sur(:,i),'alpha',0.1);
    if (h)
        i
    end
end
for i = 19:22
    [h,p,ci,stats]=ttest(s(:,i),s(:,i+4),'alpha',0.1);
    if (h)
        i-18
    end
end