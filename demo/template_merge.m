% 初始化參數
fs = 500; % 取樣頻率
nChannels = 32; % 頻道數
nPoints = 5000; % 每個頻道的取樣點數，10秒的數據點數
nFrequencies = 8; % 頻率範圍的數量
nBlocks = 5; % 每個實驗的 block 數
minSNR_dB = 0; % 最小 SNR 值 (dB)
maxSNR_dB = 20; % 最大 SNR 值 (dB)

% 創建時間向量
t = (0:nPoints-1) / fs;

% 預分配模板信號矩陣
data_tmp = zeros(nChannels, nPoints, nFrequencies, nBlocks);
data = zeros(nChannels, nPoints, nFrequencies, nBlocks);

% 生成模板信號
for f = 1:nFrequencies
    freq = 7 + f; % 從 8 Hz 到 15 Hz
    for ch = 1:nChannels
        cosWave = cos(2 * pi * freq * t);
        sinWave = sin(2 * pi * freq * t);
        for blk = 1:nBlocks
            data_tmp(ch, :, f, blk) = cosWave + sinWave;
        end
    end
end

% 為每個 channel, frequency, 和 block 添加噪聲
for ch = 1:nChannels
    for f = 1:nFrequencies
        for blk = 1:nBlocks
            currentSignal = squeeze(data_tmp(ch, :, f, blk));
            signalPower = var(currentSignal); % 計算當前信號的方差，作為信號功率
            % 隨機選擇 SNR 級別
            randomSNR_dB = minSNR_dB + (maxSNR_dB - minSNR_dB) * rand();
            noisePower = signalPower / (10^(randomSNR_dB/10)); % 根據隨機 SNR 計算噪聲功率
            noise = sqrt(noisePower) * randn(size(currentSignal)); % 生成正態分佈噪聲
            data(ch, :, f, blk) = currentSignal + noise; % 將噪聲加到原信號上
        end
    end
end


% 選取頻率 8 Hz 的信號
originalSignal = squeeze(data_tmp(1, :, 1, 1));
noisySignal = squeeze(data(1, :, 1, 1));

% 繪製原始信號和有噪聲的信號
figure;
plot(originalSignal);
title('Original Signal at 8 Hz');
xlabel('Sample Points');
ylabel('Amplitude');

figure;
plot(noisySignal);
title('Noisy Signal at 8 Hz');
xlabel('Sample Points');
ylabel('Amplitude');

% 合併兩個信號的繪製
figure;
hold on;
plot(originalSignal, 'b', 'DisplayName', 'Original');
plot(noisySignal, 'r', 'DisplayName', 'Noisy');
hold off;
title('Comparison of Original and Noisy Signals at 8 Hz');
xlabel('Sample Points');
ylabel('Amplitude');
legend show;

% FFT 計算
nfft = 2048;
fftOriginal = fft(originalSignal, nfft);
fftNoisy = fft(noisySignal, nfft);

f = fs * (0:(nfft/2)) / nfft;
magnitudeOriginal = abs(fftOriginal(1:nfft/2+1));
magnitudeNoisy = abs(fftNoisy(1:nfft/2+1));

% 繪製 FFT 結果
figure;
plot(f, magnitudeOriginal);
title('FFT of Original Signal at 8 Hz');
xlabel('Frequency (Hz)');
ylabel('Magnitude');
xlim([0 20]);

figure;
plot(f, magnitudeNoisy);
title('FFT of Noisy Signal at 8 Hz');
xlabel('Frequency (Hz)');
ylabel('Magnitude');
xlim([0 20]);

% 合併的 FFT 結果
figure;
hold on;
plot(f, magnitudeOriginal, 'b', 'DisplayName', 'Original FFT');
plot(f, magnitudeNoisy, 'r', 'DisplayName', 'Noisy FFT');
hold off;
title('Comparison of FFT Results at 8 Hz');
xlabel('Frequency (Hz)');
ylabel('Magnitude');
xlim([0 20]);
legend show;
