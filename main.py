import random
import sys

import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
import squarify
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PrettyWidget(QWidget):
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 480)

        grid = QGridLayout()
        self.setLayout(grid)

        btn1 = QPushButton('Plot 1 ', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(self.plot1)
        grid.addWidget(btn1, 5, 0)

        btn2 = QPushButton('Plot 2 ', self)
        btn2.resize(btn2.sizeHint())
        btn2.clicked.connect(self.plot2)
        grid.addWidget(btn2, 5, 1)

        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 3, 0, 1, 2)

        self.show()

    def plot1(self):
        self.canvas.draw()


    def plot2(self):
        self.figure.clf()

        ax5 = self.figure.add_subplot(211)

        data = np.array([[588, 265, 93], [342, 154, 54], [930, 419, 147]])

        length = len(data)
        x_labels = ['Secteur 1', 'Secteur 2', 'Total']

        # Set plot parameters
        width = 0.2  # width of bar
        x = np.arange(length)

        ax5.bar(x, data[:, 0], width, color='#3498db', label='Capital constant (C)')
        ax5.bar(x + width, data[:, 1], width, color='#e74c3c', label='Capital variable (V)')
        ax5.bar(x + (2 * width), data[:, 2], width, color='#f1c40f', label='Surplus (S)')

        ax5.set_ylabel('Milliards de CHF')
        #ax5.set_ylim(0, 75)
        ax5.set_xticks(x + width + width / 2)
        ax5.set_xticklabels(x_labels)
        #ax5.set_Title()
        ax5.legend()

        ax5.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

        ax5.plot()

        ax2 = self.figure.add_subplot(234)

        squarify.plot(sizes=[1, 2], label=["Total", ""], color=["#3498db", "white"], alpha=.8, ax=ax2)
        ax2.axis('off')

        ax3 = self.figure.add_subplot(235)
        squarify.plot(sizes=[2, 1], label=['Total', ""], color=['#e74c3c', "white"], alpha=.8, ax=ax3)
        ax3.axis('off')

        ax4 = self.figure.add_subplot(236)
        squarify.plot(sizes=[1], label=['Total'], color=['#7f8c8d'], alpha=.8, ax=ax4)
        ax4.axis('off')

        self.canvas.draw()


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
GUI = PrettyWidget()
sys.exit(app.exec_())