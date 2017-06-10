function [mx tmx smx]=fixserial()
[FileName,PathName] = uigetfile('*.xlsx','Select the excel-file');
fprintf('Reading file %s ...\n',strcat(PathName,FileName));
[NUM,TXT,RAW]=xlsread(strcat(PathName,FileName),'matlab');
var=RAW(1,:);
dat=RAW(2:end,:);

%set range and bin
bin=100;
range=2:15;

%set file name
%fname_total = 'total2.xlsx';
%fname_trial = 'trials.xlsx';
%fname_sub = 'subs.xlsx';
fname_mix = 'mix.xlsx';

%search for mix data
[mx]=searchProportionMix(dat(:,[1,4,5:7]),bin,range);
xlswrite(fname_mix,mx);


%search for total data
%[mx]=searchProportion(dat(:,5:7),bin,range);
%xlswrite(fname_total,mx);

%search for trail index
%[tmx]=searchProportionTrial(dat(:,[1,4,5:7]),bin,range);
%xlswrite(fname_trial,tmx);

%search for subject index
%[smx]=searchProportionSub(dat(:,[1,4,5:7]),bin,range);
%xlswrite(fname_sub,smx);
end


function [mx]=searchProportion(dat,bin,range)
fprintf('Search for total data...\n');
for i=1:length(range)
    fprintf('Bin : %d\n',i);
    r=find(strcmp(dat(:,3),'a') & cell2mat(dat(:,1)) < (range(i)+1)*bin & cell2mat(dat(:,2)) > range(i)*bin);
    mx(i,1)=length(r);
    
    r=find(strcmp(dat(:,3),'b') & cell2mat(dat(:,1))<(range(i)+1)*bin & cell2mat(dat(:,2))>range(i)*bin);
    mx(i,2)=length(r);
    
    r=find(strcmp(dat(:,3),'c') & cell2mat(dat(:,1))<(range(i)+1)*bin & cell2mat(dat(:,2))>range(i)*bin);
    mx(i,3)=length(r);
    
    r=find(strcmp(dat(:,3),'d') & cell2mat(dat(:,1))<(range(i)+1)*bin & cell2mat(dat(:,2))>range(i)*bin);
    mx(i,4)=length(r);
    
    r=find(cell2mat(dat(:,1))<(range(i)+1)*bin & cell2mat(dat(:,2))>range(i)*bin);
    mx(i,5)=length(r)-sum(mx(i,1:4));
    
    %第6列存放bin的id
    mx(i,6)=i;
    
    %计算比例，1-5列的比例对应存放在7-11列
    isum = mx(i,1)+mx(i,2)+mx(i,3)+mx(i,4)+mx(i,5);
    
    mx(i,7) = mx(i,1)/isum;
    mx(i,8) = mx(i,2)/isum;
    mx(i,9) = mx(i,3)/isum;
    mx(i,10) = mx(i,4)/isum;
    mx(i,11) = mx(i,5)/isum;
end
end

function [mx]=searchProportionMix(dat,bin,range)
subs=unique(cell2mat(dat(:,1)));
trials=unique(cell2mat(dat(:,2)));
fprintf('Search for subjects and trials indexing...\n');
for i=1:length(range)
    fprintf('Bin : %d\n',i);
    for s=1:length(subs)
        for t=1:length(trials)
            r=find(cell2mat(dat(:,1))==subs(s) & cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'a') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
            row_id = i+(s-1)*length(trials)*length(range)+(t-1)*length(range);
            mx(row_id,1)=length(r);
            
            r=find(cell2mat(dat(:,1))==subs(s) & cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'b') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
            mx(row_id,2)=length(r);
            
            r=find(cell2mat(dat(:,1))==subs(s) & cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'c') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
            mx(row_id,3)=length(r);
            
            r=find(cell2mat(dat(:,1))==subs(s) & cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'d') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
            mx(row_id,4)=length(r);
            
            r=find(cell2mat(dat(:,1))==subs(s) & cell2mat(dat(:,2))==trials(t) & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
            mx(row_id,5)=length(r)-sum(mx(row_id,1:4));
            
            %第6列是subs的名字
            mx(row_id,6)=subs(s);
            
            %第7列是trials的名字
            mx(row_id,7)=trials(t);

            %第8列是bin id
            mx(row_id,8)=i;
            
            %计算比例，1-5列的比例对应存放在9-13列
            isum = mx(row_id,1)...
                +mx(row_id,2)...
                +mx(row_id,3)...
                +mx(row_id,4)...
                +mx(row_id,5);
            
            mx(row_id,9) = mx(row_id,1)/isum;
            mx(row_id,10) = mx(row_id,2)/isum;
            mx(row_id,11) = mx(row_id,3)/isum;
            mx(row_id,12) = mx(row_id,4)/isum;
            mx(row_id,13) = mx(row_id,5)/isum;
            
        end
    end
end
end

function [mx]=searchProportionTrial(dat,bin,range)
trials=unique(cell2mat(dat(:,2)));
fprintf('Search for trails indexing...\n');
for i=1:length(range)
    fprintf('Bin : %d\n',i);
    for t=1:length(trials)
        r=find(cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'a') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(t-1)*length(range),1)=length(r);
        
        r=find(cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'b') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(t-1)*length(range),2)=length(r);
        
        r=find(cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'c') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(t-1)*length(range),3)=length(r);
        
        r=find(cell2mat(dat(:,2))==trials(t) & strcmp(dat(:,5),'d') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(t-1)*length(range),4)=length(r);
        
        r=find(cell2mat(dat(:,2))==trials(t) & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(t-1)*length(range),5)=length(r)-sum(mx(i+(t-1)*length(range),1:4));
        
        %第6列是trail的ID号，第7列放bin的序列号
        mx(i+(t-1)*length(range),6)=trials(t);
        mx(i+(t-1)*length(range),7)=i;
        
        %计算比例，1-5列的比例对应存放在8-12列
        isum = mx(i+(t-1)*length(range),1)+mx(i+(t-1)*length(range),2)+mx(i+(t-1)*length(range),3)+mx(i+(t-1)*length(range),4)+mx(i+(t-1)*length(range),5);
        
        mx(i+(t-1)*length(range),8) = mx(i+(t-1)*length(range),1)/isum;
        mx(i+(t-1)*length(range),9) = mx(i+(t-1)*length(range),2)/isum;
        mx(i+(t-1)*length(range),10) = mx(i+(t-1)*length(range),3)/isum;
        mx(i+(t-1)*length(range),11) = mx(i+(t-1)*length(range),4)/isum;
        mx(i+(t-1)*length(range),12) = mx(i+(t-1)*length(range),5)/isum;
    end
end
end

function [mx]=searchProportionSub(dat,bin,range)
subs=unique(cell2mat(dat(:,1)));
subs
fprintf('Search for subjects indexing...\n');
for i=1:length(range)
    fprintf('Bin : %d\n',i);
    for s=1:length(subs)
        r=find(cell2mat(dat(:,1))==subs(s) & strcmp(dat(:,5),'a') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(s-1)*length(range),1)=length(r);
        
        r=find(cell2mat(dat(:,1))==subs(s) & strcmp(dat(:,5),'b') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(s-1)*length(range),2)=length(r);
        
        r=find(cell2mat(dat(:,1))==subs(s) & strcmp(dat(:,5),'c') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(s-1)*length(range),3)=length(r);
        
        r=find(cell2mat(dat(:,1))==subs(s) & strcmp(dat(:,5),'d') & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(s-1)*length(range),4)=length(r);
        
        r=find(cell2mat(dat(:,1))==subs(s) & cell2mat(dat(:,3))<(range(i)+1)*bin & cell2mat(dat(:,4))>range(i)*bin);
        mx(i+(s-1)*length(range),5)=length(r)-sum(mx(i+(s-1)*length(range),1:4));
        
        %第6列是subs的名字，第7列是bin的顺序号
        %mx(i+(s-1)*length(range),6)=cell2mat(subs(s));
        mx(i+(s-1)*length(range),6)=subs(s);
        mx(i+(s-1)*length(range),7)=i;
        
        %计算比例，1-5列的比例对应存放在8-12列
        isum = mx(i+(s-1)*length(range),1)+mx(i+(s-1)*length(range),2)+mx(i+(s-1)*length(range),3)+mx(i+(s-1)*length(range),4)+mx(i+(s-1)*length(range),5);
        
        mx(i+(s-1)*length(range),8) = mx(i+(s-1)*length(range),1)/isum;
        mx(i+(s-1)*length(range),9) = mx(i+(s-1)*length(range),2)/isum;
        mx(i+(s-1)*length(range),10) = mx(i+(s-1)*length(range),3)/isum;
        mx(i+(s-1)*length(range),11) = mx(i+(s-1)*length(range),4)/isum;
        mx(i+(s-1)*length(range),12) = mx(i+(s-1)*length(range),5)/isum;
    end
end
end


