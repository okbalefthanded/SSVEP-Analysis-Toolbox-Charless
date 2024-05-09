# -*- coding: utf-8 -*-

import os
import numpy as np
import py7zr


from typing import Union, Optional, Dict, List, Tuple
from numpy import ndarray, transpose

from .basedatasetNodownload import BaseDatasetNoDownload
from .subjectinfo import SubInfo
from ..utils.download import download_single_file
from ..utils.io import loadmat
from ..utils.algsupport import floor

class CharlessDataset(BaseDatasetNoDownload):
    """
        This is handsome charless's dataset.

        # Targets(Trails) = 8  (from 8 hz to 15 hz)
        # Channels = 31 ('Fp1', 'Fp2', 'AF3', 'AF4', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FT7',
                         'FC3', 'FCz', 'FC4', 'FT8', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP7',
                         'CP3', 'CP4', 'TP8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'O1',
                         'Oz', 'O2')                                                    # * Notice: CPz was used for Re-reference
        # Sampling rate = 500hz
        # Sampling points = 10000 per epoch
        # Block = 5

        Assume there's no phase difference.
        Currently only 1 subject, the handsome Charless :(
    """
 
    # * Notice: CPz was used for Rereference
    _CHANNELS = [
        'Fp1', 'Fp2', 'AF3', 'AF4', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FT7',
        'FC3', 'FCz', 'FC4', 'FT8', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP7',
        'CP3', 'CPz', 'CP4', 'TP8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'O1',
        'Oz', 'O2'
    ]

    _FREQS = [
        8, 9, 10, 11, 12, 13, 14, 15
    ]

    _PHASES = [
        0, 0, 0, 0, 0, 0, 0, 0
    ]
    
    _SUBJECTS = [SubInfo(ID = 'Sfake')]
    
    def __init__(self, 
                 path: Optional[str] = None,
                 path_support_file: Optional[str] = None):
        super().__init__(subjects = self._SUBJECTS, 
                         ID = 'Charless\'s Dataset', 
                         url = '', 
                         paths = path, 
                         channels = self._CHANNELS, 
                         srate = 500, 
                         block_num = 5, 
                         trial_num = len(self._FREQS),
                         trial_len = 20, 
                         stim_info = {'stim_num': len(self._FREQS),
                                      'freqs': self._FREQS,
                                      'phases': [i * np.pi for i in self._PHASES]},
                         support_files = ['Readme.txt',
                                          'Sub_info.txt',
                                          'Freq_Phase.mat'],
                         path_support_file = path_support_file,
                         t_prestim = 0,
                         t_break = 0,
                         default_t_latency = 0.)
    
    def download_single_subject(self,
                                subject: SubInfo):
        download_flag = False
        source_url = "not support"
        desertation = "not support"

        return download_flag, source_url, desertation
    
    def download_file(self,
                      file_name: str):
        download_flag = False
        source_url = "not support"
        desertation = "not support"
        
        return download_flag, source_url, desertation
        
    def get_sub_data(self, 
                     sub_idx: int) -> ndarray:
        if sub_idx < 0:
            raise ValueError('Subject index cannot be negative')
        if sub_idx > len(self.subjects)-1:
            raise ValueError('Subject index should be smaller than {:d}'.format(len(self.subjects)))
        
        sub_info = self.subjects[sub_idx]
        file_path = os.path.join(sub_info.path, sub_info.ID + '.mat')
        
        mat_data = loadmat(file_path)
        data = mat_data['data']
        data = transpose(data, (3,2,0,1)) # block_num * stimulus_num * ch_num * whole_trial_samples
        
        return data

# ! TODO  
    def get_label_single_trial(self,
                               sub_idx: int,
                               block_idx: int,
                               trial_idx: int,
                               sig_len: float) -> int:

        # ! TODO by handsome Charless        
        # sig_len = floor(sig_len * self.srate)
        # ret = []
        # for i in range (1,floor(10000/int(sig_len)) + 1):
        #     ret.append(trial_idx)
        
        return trial_idx
        