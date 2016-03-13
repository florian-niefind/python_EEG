#usr/bin/python
#-*- encoding: utf-8 -*-
# @author: Florian Niefind
# @contact: nifflor@googlemail.com
# @date: 2016-03-11
 
import numpy as np

class EEG_dataset():
    """
    Class to hold EEG data of a single subject. It is based on EEGLABs way of 
    doing things, but grand averaging uses a different data structure.
    """

    def __init__(self):
        """
        Empty init stub.
        """
        self.data = None
        self.sample_rate = 500
        self.times = np.arange(-200, 800, 2, dtype = int)
        self.channels = {'F3':(1,1), 'Fz':(1,2), 'F4':(1,3), 
                            'C3':(2,1), 'Cz':(2,2), 'C4':(2,3), 
                            'P3':(3,1), 'Pz':(2,2), 'P4':(3,3)}
        self.events = []
    
    def read_data(self, infile):
        '''
        Read text from a csv file. Columns are samples, rows are channels.
        @param: file - input filename
        '''
        self.data = np.genfromtxt(infile, delimiter = ',', dtype = float)
        
    def edit_channel_names(self):
        """
        @TODO
        """
        pass

    def filter_bandpass(self):
        """
        @TODO
        """
        pass

    def re_reference(self):
        """
        @TODO
        """
        pass

    def MSEC_correct(self):
        """
        @TODO
        """
        pass


class EEG_grand_average():
    """
    Multidimensional array to hold averaged data. 
    Dimensions: 1:channels, 2:samples, 3:subjects, 4-x:conditions
    @TODO: Remove hard coded stuff once there is data from python.
    """
    def __init__(self):
        """
        Empty init stub
        """
        self.data = None
        self.dim_info = {"Channels":70, "Samples":625, "Conds":9, "Subjects":0}
        self.sample_rate = None
        self.times = np.arange(-250, 1000, 2, dtype = int)
        
    def read_data(self, infile):
        """
        Read data from MATLAB file, so I can quickly work with some data.
        @param: file - input filename
        @TODO: Choose a sensible file format.
        """
        import scipy.io as mat2py
        inputs = mat2py.loadmat(infile)
        self.data = inputs["subavg"]

     
def GFP_GMD(data):
    """
    Returns Global Field Power (GFP) and Globale Map Dissimilarity (GMD) for a 
    Channels * Samples dataset.
    
    @subset: data - subset from grand average. Channels must be first dimension,
                    samples in the second dimension
    @return: GFP, GMD: np-arrays with GFP and GMD
    """
    import numpy.matlib as np_ml

    #calculate global field power
    GFP = np.std(data, axis = 0)

    #norm data
    norm_factor = np_ml.repmat(GFP, data.shape[0],1)
    data_normed = data / norm_factor

    #calculate GMD
    GMD = np.hstack((np.zeros((data_normed.shape[0],1),dtype = float), 
                        np.diff(data_normed,1,1)))
    GMD = np.std(GMD, axis = 0)
    return GFP, GMD
