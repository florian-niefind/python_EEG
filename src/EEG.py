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
        self.header_info = {}
        self.data = None
        self.channels = {}
        self.times = [1,2,3,4]
        self.sample_rate = None
        self.reference = None
        self.events = []
        
    def __str__(self):
        return 'Header: %s\nData: %s\nChannels: %s\n Times: %s array - %i,%i...%i\nSample rate: %i\nReference: %s\nEvents: %i' %(self.header_info, self.data.shape, self.channels, len(self.times), self.times[0], self.times[1], self.times[-1], self.sample_rate, self.reference, len(self.events))
#        print self.header_info
 #       print self.data.shape
  #      print self.channels
   #     print self.times
    #    print self.sample_rate
     #   print self.reference
      #  print len(self.events)
    
    def read_data(self, hdr_infile, ref = 'noref!', add_ref = False):
        '''
        Read BVA.vhdr file and collect info in dictionary. Then read data file 
        and marker file.
        @param: hdr_infile - filename of BVA.vhdr file
        @param: ref - String with name of the reference channel. Somehow not 
                      provided in vhdr file
        @param: add_ref -  If True, empty reference channel is added to data
        '''
        self.ref = ref

        with open(hdr_infile,'r') as infile:
            for line in infile:
                if line[0:2] == '; ':
                    continue
                else:
                    line = line.strip()
                    if line == '[Comment]': #do not read on from here
                        break
                    elif '=' in line:
                        line = line.split('=')
                        if ',' in line[1]: #if it is a channel info line
                            self.channels[line[1].split(',')[0]] = int(line[0].strip('Ch'))
                        else: #if it is header info
                            self.header_info[line[0]] = line[1]
                    else:
                        continue
        #pre-process some of the header info
        self.header_info['NumberOfChannels'] = int(self.header_info['NumberOfChannels'])
        self.sample_rate = 1000000 / int(self.header_info['SamplingInterval'])
                
        #read data
        self.read_data_file(self.header_info['DataFile'], self.header_info['NumberOfChannels'], add_ref)
        
        
    def read_data_file(self, data_infile, no_channels, add_ref = None):
        '''
        Read text from a binary file.
        @param: data_file - filename of BVA.eeg file
        @param: no_channels - number of recorded channels
        @param: add_ref - string with name of the reference channel. If None, 
                          no reference channel is added
        '''
        with open(data_infile,'rb') as infile:
            #read data
            data_formats = {'INT_16': np.uint16}
            self.data = np.fromfile(infile, dtype = data_formats[self.header_info['BinaryFormat']])
            
            #reshape
            if self.header_info['DataOrientation'] == 'MULTIPLEXED':
                self.data = np.reshape(self.data, (-1, no_channels))
                #transpose so it is channels * samples
                self.data = np.transpose(self.data)
            else: #VECTORIZED
                self.data = np.reshape(self.data, (no_channels, -1))
            
            #convert to floats in muVolt
            self.data = self.data.astype(np.float32)/100
            
            #add an empty reference channel which will be filled upon 
            #re-referencing
            if add_ref:
                self.channels[self.ref] = len(self.channels) + 1
                self.data = np.vstack((self.data, np.zeros((1,self.data.shape[1]),dtype = np.float32)))

                
    def edit_channel_info(self):
        """
        @TODO
        """
        pass


    def filter_bandpass(self):
        """
        @TODO
        """
        pass


    def rereference(self, channels):
        """
        Re-reference data to a certain channel/ mean of channels
        @param: channels - channels to re-reference to. If [] is given, average
                           reference is computed.
        """
        import numpy.matlib as np_ml
        
        if channels == []:
            ref = np.mean(self.data, axis=0)
        elif len(channels) > 1:
            ref = np.mean(self.data[channels,:], axis=0)
        else: #if it is just a single channel simply select it
            ref = self.data[channels,:]
        
        #reref
        ref = np.transpose(np_ml.repmat(ref, self.data.shape[1], 1))
        self.data = self.data - ref


    def MSEC_correct(self, corr_matrix_file):
        """
        Perform MSEC correction based on a BESA correction file. 
        NOTE: Automatically removes artefact channels for now
        @param: corr_matrix_file - File holding a correction matrix.
        """
        #read corr matrix
        with open(corr_matrix_file, 'rb') as infile:
            corr_matrix = np.genfromtxt(infile, dtype = np.float32, delimiter = '\t', skip_header = 1)[:,1:]

        #correct
        self.data = np.dot(corr_matrix,self.data)
        
        #remove artefact channels
        self.data = self.data[0:len(channels)+1,:]


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
    Returns Global Field Power (GFP) and Global Map Dissimilarity (GMD) for a 
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
