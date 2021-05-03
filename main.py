import sys
import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rc

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # y-axis in bold
        rc('font', weight='bold')

        # Values of each group
        bars1 = [12, 28, 1, 8, 22]
        bars2 = [28, 7, 16, 4, 10]
        bars3 = [25, 3, 23, 25, 17]

        # Heights of bars1 + bars2
        bars = np.add(bars1, bars2).tolist()

        # The position of the bars on the x-axis
        r = [0, 1, 2, 3, 4]

        # Names of group and bar width
        names = ['A', 'B', 'C', 'D', 'E']
        barWidth = 1

        # Create brown bars
        plt.bar(r, bars1, color='#7f6d5f', edgecolor='white', width=barWidth)
        # Create green bars (middle), on top of the first ones
        plt.bar(r, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=barWidth)
        # Create green bars (top)
        plt.bar(r, bars3, bottom=bars, color='#2d7f5e', edgecolor='white', width=barWidth)

        # Custom X axis
        plt.xticks(r, names, fontweight='bold')
        plt.xlabel("group")

        # Show graphic
        plt.show()

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(plt, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)


        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()