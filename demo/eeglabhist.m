% EEGLAB history file generated on the 04-Apr-2024
% ------------------------------------------------
[ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
EEG = pop_biosig('C:\Users\USER\ArtiseBio\0327_8-15hz_20sec_trail1.edf');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 0,'gui','off'); 
EEG = pop_eegfiltnew(EEG, 'locutoff',1,'hicutoff',200,'plotfreqz',1);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'setname','filter 1~200','gui','off'); 
EEG = pop_eegfiltnew(EEG, 'locutoff',40,'hicutoff',60,'revfilt',1,'plotfreqz',1);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'setname','notch 40~60','gui','off'); 
EEG = pop_select( EEG, 'channel',{'TP7','CP3','CPz','CP4','TP8','P7','P3','Pz','P4','P8','O1','Oz','O2'});
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 3,'setname','select channel','gui','off'); 
EEG = pop_rmdat( EEG, {'10, Expr 20s'},[0 20] ,0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4,'setname','10hz','gui','off'); 
pop_saveh( ALLCOM, 'eeglabhist.m', 'C:\Users\USER\Downloads\');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 5,'retrieve',4,'study',0); 
eeglab redraw;
