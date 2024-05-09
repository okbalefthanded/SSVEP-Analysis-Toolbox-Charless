    % 噪聲水平，這裡假設 SNR 為 20 dB
    snr = 0.001;
    
    % 為每個 channel, frequency, 和 block 添加噪聲
    for ch = 1:nChannels
        for f = 1:nFrequencies
            for blk = 1:nBlocks
                % 當前信號
                currentSignal = squeeze(data(ch, :, f, blk));
                % 計算信號功率
                signalPower = var(currentSignal);
                % 計算噪聲功率
                noisePower = signalPower / (10^(snr/10));
                % 生成噪聲
                noise = sqrt(noisePower) * randn(size(currentSignal));
                % 加入噪聲
                data(ch, :, f, blk) = currentSignal + noise;
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
