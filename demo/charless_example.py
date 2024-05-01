# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from SSVEPAnalysisToolbox.datasets import CharlessDataset
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

num_subbands = 5

# Prepare dataset
dataset = CharlessDataset(path = 'Charless_database')
dataset.regist_preprocess(preprocess)
dataset.regist_filterbank(filterbank)

print(dataset)
print(dataset.stim_info['freqs'])

# Prepare recognition model
weights_filterbank = suggested_weights_filterbank()
recog_model = SCCA_qr(weights_filterbank = weights_filterbank)

# Set simulation parameters
ch_used = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

all_trials = [i for i in range(dataset.trial_num)]

harmonic_num = 5
tw = 20
sub_idx = 0
test_block_idx = 0
test_block_list, train_block_list = dataset.leave_one_block_out(block_idx = test_block_idx)

# Get training data and train the recognition model
ref_sig = dataset.get_ref_sig(tw, harmonic_num,ignore_stim_phase=True)

freqs = dataset.stim_info['freqs']
X_train, Y_train = dataset.get_data(sub_idx = sub_idx,
                                    blocks = train_block_list,
                                    trials = all_trials,
                                    channels = ch_used,
                                    sig_len = tw,
                                    shuffle=True)
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

print(f"Test_y = {Y_test}")
print(f"Pred_y = {pred_label}")

toc_test = time.time()-tic
toc_test_onetrial = toc_test/len(Y_test)

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
