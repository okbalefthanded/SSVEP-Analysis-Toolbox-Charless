% 初始化參數
fs = 500; % 取樣頻率
nChannels = 32; % 頻道數
nPoints = 10000; % 每個頻道的取樣點數
nFrequencies = 8; % 頻率範圍的數量
nBlocks = 5; % 每個實驗的 block 數

% 創建時間向量
t = (0:nPoints-1) / fs;

% 預分配模板信號矩陣
data = zeros(nChannels, nPoints, nFrequencies, nBlocks);

% 生成模板信號
for f = 1:nFrequencies
    freq = 7 + f; % 從 8 Hz 到 15 Hz
    for ch = 1:nChannels
        % 生成正弦和餘弦波形
        cosWave = cos(2 * pi * freq * t);
        sinWave = sin(2 * pi * freq * t);
        
        % 將這些波形複製到所有 block
        for blk = 1:nBlocks
            data(ch, :, f, blk) = cosWave + sinWave;
        end
    end
end

% 選取第一頻道、第一個 block 的數據
selectedData = squeeze(data(1, :, :, 1));

% 預分配 FFT 結果空間
fftResults = zeros(size(selectedData));

% 執行 FFT    
for f = 1:nFrequencies
    fftResults(:, f) = fft(selectedData(:, f));
end

% 計算頻譜
nfft = size(fftResults, 1);
f = fs * (0:(nfft/2)) / nfft; % 頻率軸
magnitude = abs(fftResults(1:nfft/2+1, :)); % 取模

% 繪圖
figure;
plot(f, magnitude);
title('FFT Result of Each Frequency Component');
xlabel('Frequency (Hz)');
ylabel('Magnitude');
xlim([1 20]);
legend('8Hz', '9Hz', '10Hz', '11Hz', '12Hz', '13Hz', '14Hz', '15Hz');

size(data)
