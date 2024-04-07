signal = data(31,:,1,1)      % sample 8 hz, Oz, 1st block

N = length(signal       )

Fs = 500; % 採樣率

% 進行FFT
Y = fft(signal);

% 計算雙側頻譜
P2 = abs(Y/N);

% 計算單側頻譜
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);

% 定義頻率範圍
f = Fs*(0:(N/2))/N;

% 篩選1到20Hz的頻率範圍
ind = f >= 1 & f <= 20;
f_focus = f(ind);

P1_focus = P1(ind);

% 繪製頻譜，僅顯示1到20Hz的部分
figure;
plot(f_focus,P1_focus) 
title('Signal Frequency Spectrum (1 to 20 Hz)')
xlabel('Frequency (f) [Hz]')
ylabel('|P1(f)|')