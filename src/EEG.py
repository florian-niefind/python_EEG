#usr/bin/python
#-*- encoding: utf-8 -*-

import numpy as np

class EEG_dataset():
    """
    Class to hold EEG data. It is based on EEGLABs way of doing things. 
    """

    def __init__(self):
        """
        Empty init stub.
        """
        self.data = None
        self.sample_rate = 500
        self.channels = {'F3':(1,1), 'Fz':(1,2), 'F4':(1,3), 
                            'C3':(2,1), 'Cz':(2,2), 'C4':(2,3), 
                            'P3':(3,1), 'Pz':(2,2), 'P4':(3,3)}
        self.events = []
    
    def read_data(self, file):
        '''
        Read text from a csv file. Columns are samples, rows are channels.
        @param: file - input file
        '''
        self.data = np.genfromtxt(file, delimiter = ',', dtype = float)
