
class lineplot_panel_TestCase(TestCase):
    
    def set_up(self, data):
        
        fig = plt.figure()
        
        ax1 = fig.add_subplot(231)
        test_data = np.mean(gavg.data[36,:,0:3,:], axis = 2)  
        lineplot_panel(gavg.times, test_data, ax1)

        ax2 = fig.add_subplot(232)
        lineplot_panel(gavg.times, test_data, ax2, 
                        linespecs = ['m-', 'y-', 'c-'], title = 'New Colors')

        ax3 = fig.add_subplot(233)
        lineplot_panel(gavg.times, test_data, ax3, 
                       title = 'Labels and Limits',
                       xlim = [-200, 800], ylim = [-6, 6],
                       xlabel = u'Time since stimulus onset [ms]', ylabel = u'Amplitude [µV]')

        ax4 = fig.add_subplot(234)
        lineplot_panel(gavg.times, test_data, ax4, 
                       title = 'ROI',
                       ROI = [(200, -6),100,12])

        ax5 = fig.add_subplot(235)
        lineplot_panel(gavg.times, test_data, ax5, 
                       title = 'Diff no ylim',
                       difference = [0, 1])

        ax6 = fig.add_subplot(236)
        lineplot_panel(gavg.times, test_data, ax6, 
                       title = 'Diff ylim',
                       difference = [0,1],
                       xlim = [-200, 800], ylim = [-6, 6])

