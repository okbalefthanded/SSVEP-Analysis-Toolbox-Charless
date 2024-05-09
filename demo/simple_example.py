# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from SSVEPAnalysisToolbox.datasets import BenchmarkDataset
from SSVEPAnalysisToolbox.utils.benchmarkpreprocess import (
    preprocess, filterbank, suggested_ch, suggested_weights_filterbank
)
from SSVEPAnalysisToolbox.algorithms import (
    SCCA_qr, SCCA_canoncorr, ECCA, MSCCA, MsetCCA, MsetCCAwithR,
    TRCA, ETRCA, MSETRCA, MSCCA_and_MSETRCA, TRCAwithR, ETRCAwithR, SSCOR, ESSCOR,
    TDCA
)
from SSVEPAnalysisToolbox.evaluator import cal_acc,cal_itr

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft

num_subbands = 5

# Prepare dataset
dataset = BenchmarkDataset(path = '2016_Tsinghua_SSVEP_database')
dataset.regist_preprocess(preprocess)
dataset.regist_filterbank(filterbank)

print(dataset)
print(dataset.stim_info['freqs'])

# Prepare recognition model
weights_filterbank = suggested_weights_filterbank()
recog_model = SCCA_qr(weights_filterbank = weights_filterbank)

# Set simulation parameters
ch_used = suggested_ch()

# print(ch_used)

all_trials = [i for i in range(dataset.trial_num)]

# print(all_trials)

harmonic_num = 5
tw = 1
sub_idx = 1
test_block_idx = 0
test_block_list, train_block_list = dataset.leave_one_block_out(block_idx = test_block_idx)

# Get training data and train the recognition model
ref_sig = dataset.get_ref_sig(tw, harmonic_num)
freqs = dataset.stim_info['freqs']
X_train, Y_train = dataset.get_data(sub_idx = sub_idx,
                                    blocks = train_block_list,
                                    trials = all_trials,
                                    channels = ch_used,
                                    sig_len = tw)

print(len(X_train[0][0]))

tic = time.time()
recog_model.fit(X=X_train, Y=Y_train, ref_sig=ref_sig, freqs=freqs) 
toc_train = time.time()-tic

# Get testing data and test the recognition model
X_test, Y_test = dataset.get_data(sub_idx = sub_idx,
                                    blocks = test_block_list,
                                    trials = all_trials,
                                    channels = ch_used,
                                    sig_len = tw)

tic = time.time()
pred_label, _ = recog_model.predict(X_test)
toc_test = time.time()-tic
toc_test_onetrial = toc_test/len(Y_test)

# 獲取所有信號的時域資料，並畫圖
fig, axes = plt.subplots(8, 1, figsize=(10, 20))  # 假設有8個信號

for i in range(8):
    # 對每個信號進行FFT
    n = len(X_test[i][0][0])
    freq = np.fft.fftfreq(n, 1/250)
    sig_fft = fft(X_test[i][0][0])

    # 頻域信號繪圖
    axes[i].plot(freq[:n // 2], np.abs(sig_fft)[:n // 2])
    axes[i].set_title(f'Signal {i+8} Frequency Domain')
    axes[i].set_xlabel('Frequency (Hz)')
    axes[i].set_ylabel('Magnitude')

    # 限制頻率範圍並設定刻度
    axes[i].set_xlim([5, 20])
    axes[i].set_xticks(np.arange(5, 21, 1))  # 5 到 20 Hz, 每 1 Hz 一個刻度

plt.tight_layout()
plt.show()



print(f"Test_y = {Y_test}, Pred_y = {pred_label}")

# Calculate performance
acc = cal_acc(Y_true = Y_test, Y_pred = pred_label)
itr = cal_itr(tw = tw, t_break = dataset.t_break, t_latency = dataset.default_t_latency, t_comp = toc_test_onetrial,
              N = len(freqs), acc = acc)
print("""
Simulation Information:
    Method Name: {:s}
    Dataset: {:s}
    Signal length: {:.3f} s
    Channel: {:s}
    Subject index: {:n}
    Testing block: {:s}
    Training block: {:s}
    Training time: {:.5f} s
    Total Testing time: {:.5f} s
    Testing time of single trial: {:.5f} s

Performance:
    Acc: {:.3f} %
    ITR: {:.3f} bits/min
""".format(recog_model.ID,
           dataset.ID,
           tw,
           str(ch_used),
           sub_idx,
           str(test_block_list),
           str(train_block_list),
           toc_train,
           toc_test,
           toc_test_onetrial,
           acc*100,
           itr))
