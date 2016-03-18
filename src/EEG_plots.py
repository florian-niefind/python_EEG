#usr/bin/python
#-*- encoding: utf-8 -*-
# Some encapsulated functions for common plots
# @author: Florian Niefind
# @contact: nifflor@googlemail.com
# @date: 2016-03-11

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_EEG(EEG, channels, plot_range):
    """
    Plot raw single subject eeg
    @param: EEG - EEG data set
    @param: channels - List of channels to plot
    @param: plotrange - List with minimum and maximum time value [ms] to plot
    """
    fig, ax = plt.subplots(len(channels),1,sharex=True,sharey=True)
    ax[1].set_xlim([EEG.times[plot_range[0]],EEG.times[plot_range[1]]])

    for ix in xrange(len(channels)):
        ax[ix].plot(EEG.times[plot_range[0]:plot_range[1]],EEG.data[ix,plot_range[0]:plot_range[1]] - np.mean(EEG.data[ix,plot_range[0]:plot_range[1]],axis=0))



def lineplot_panel(times, data, axes, **kwargs):
    """
    Plot a lineplot showing 2 EEG channels within an epoch
    @param: times - vector of length times
    @param: data - nparray where rows are time series to plot and columns are samples
    """
    xlim = kwargs.get('xlim', None)
    ylim = kwargs.get('ylim', None)
    
    plt.title(kwargs.get('title',''))

    #plot difference between specified lines
    diff_ix = kwargs.get('difference', (0,0))
    if diff_ix != (0,0):
        diff = data[:,diff_ix[0]] - data[:,diff_ix[1]]
        if ylim:
            fill_bottom = ylim[0]
        else:
            fill_bottom = 0
        axes.fill_between(times,abs(diff)-abs(fill_bottom),fill_bottom, facecolor=[.6,.6,.6], edgecolor=[.6,.6,.6], zorder=2, label='Difference')
    
    #plot ROI if specified
    roi = kwargs.get('ROI', None)
    if roi:
        axes.add_patch(patches.Rectangle(roi[0], roi[1], roi[2], facecolor=[.8,.8,.8], edgecolor=[.8,.8,.8], zorder=1))
    
    #plot actual time series
    linespecs = kwargs.get('linespecs', ['r-', 'k-', 'b-', 'g-'])
    for line_ix in xrange(data.shape[1]):
        plt.plot(times,data[:,line_ix],linespecs[line_ix], zorder=3, linewidth= kwargs.get('linewidth',1.6))
    
    #axis limits
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    
    #axis labels
    plt.xlabel(kwargs.get('xlabel', u''))
    plt.ylabel(kwargs.get('ylabel', u''))


