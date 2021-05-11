import sys

import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
import squarify
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QInputDialog, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#Définition des variables
#Pour le moment statique, a faire en sorte qu'elles ne le soit pas par
Compo_org_1 = 2.22
Compo_org_2 = 2.22
Taux_expl_1 = 0.35
Taux_expl_2 = 0.35
Total_t = 1496
RapportSecteurs = 1.72


def plotGraphSectors(figure, data):
    """
    Dessine le graphs des secteurs économiques
    :param figure: La figure sur laquelle le graph est crée
    :param data: Les données à afficher
    :return:
    """
    #Crée le graphique
    sectorsGraph = figure.add_subplot(211)

    #Définit la largeur des barres
    width = 0.2

    x = np.arange(len(data))

    #Définit les trois bares de secteur
    sectorsGraph.bar(x, data[:, 0], width, color='#3498db', label='Capital constant (C)')
    sectorsGraph.bar(x + width, data[:, 1], width, color='#e74c3c', label='Capital variable (V)')
    sectorsGraph.bar(x + (2 * width), data[:, 2], width, color='#f1c40f', label='Surplus (S)')

    #Définit les légendes en X
    sectorsGraph.set_xticks(x + width + width / 2)
    sectorsGraph.set_xticklabels(['Secteur 1', 'Secteur 2', 'Total'])

    #Définit la légende en y
    sectorsGraph.set_ylabel('Milliards de CHF')

    #titre
    sectorsGraph.set_title('Année X')

    #Définit la grille
    sectorsGraph.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    #Affiche les légendes des barres
    sectorsGraph.legend()

def CalcYear():
    C_1_t = (Total_t / (RapportSecteurs + 1)) * RapportSecteurs
    V_1_t = C_1_t / Compo_org_1
    S_1_t = V_1_t * Taux_expl_1
    Tot_1_t = C_1_t + V_1_t + S_1_t

    C_2_t = Total_t / (RapportSecteurs + 1)
    V_2_t = C_2_t / Compo_org_2
    S_2_t = V_2_t * Taux_expl_2
    Tot_2_t = C_2_t + V_2_t + S_2_t

    C_3_t = C_1_t + C_2_t
    V_3_t = V_1_t + V_2_t
    S_3_t = S_1_t + S_2_t
    Tot_3_t = C_3_t + V_3_t + S_3_t

    Acc_t = Tot_1_t - (C_1_t + C_2_t)
    """""
    #On convertit tout en int
    C_1_t = int(C_1_t)
    V_1_t = int(V_1_t)
    S_1_t = int(S_1_t)
    C_2_t = int(C_2_t)
    V_2_t = int(V_2_t)
    S_2_t = int(S_2_t)
    C_3_t = int(C_3_t)
    V_3_t = int(V_3_t)
    S_3_t = int(S_3_t)
    """""

    TabResultat = [[C_1_t, V_1_t, S_1_t], [C_2_t, V_2_t, S_2_t], [C_3_t, V_3_t, S_3_t]]
    return TabResultat

def gettotal(TabResultats):
    Total = 0
    for i in range(len(TabResultats)):
        Total =  Total + TabResultats[i]
    return Total


def dynemisesizeaquar(value, total):
    AffValue = value / total
    AffPro = (1 - AffValue) / 3
    AffichageDynamique = [AffPro, AffValue, AffPro, AffPro]
    return AffichageDynamique

class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        self.initWindows2()

    def initWindows2(self):
        self.setGeometry(100, 100, 800, 480)
        self.setWindowTitle("Window22222")

        grid = QGridLayout()
        self.setLayout(grid)

        labExp1 = QLabel("Taux d'exploitation du secteur 1:", self)
        grid.addWidget(labExp1, 1, 1)

        ediExp1 = QLineEdit(str(Taux_expl_1))
        #ediExp1.setValidator(QIntValidator())
        grid.addWidget(ediExp1, 1, 2)

        labExp2 = QLabel("Taux d'exploitation du secteur 2:", self)
        grid.addWidget(labExp2, 2, 1)

        ediExp2 = QLineEdit(str(Taux_expl_2))
        #ediExp2.setValidator(QIntValidator())
        grid.addWidget(ediExp2, 2, 2)

        labOrga1 = QLabel("Composition organique du secteur 1:", self)
        grid.addWidget(labOrga1, 3, 1)

        ediOrga1 = QLineEdit(str(Compo_org_1))
        #ediOrga1.setValidator(QIntValidator())
        grid.addWidget(ediOrga1, 3, 2)

        labOrga2 = QLabel("Composition organique du secteur 2:", self)
        grid.addWidget(labOrga2, 4, 1)

        ediOrga2 = QLineEdit(str(Compo_org_2))
        #ediOrga2.setValidator(QIntValidator())
        grid.addWidget(ediOrga2, 4, 2)

        labRapports = QLabel("Rapports entre secteur 1 et 2:", self)
        grid.addWidget(labRapports, 5, 1)

        ediRapports = QLineEdit(str(RapportSecteurs))
        #ediRapports.setValidator(QIntValidator())
        grid.addWidget(ediRapports, 5, 2)

        labTotal = QLabel("Total:", self)
        grid.addWidget(labTotal, 6, 1)

        ediTotal = QLineEdit(str(Total_t))
        #ediTotal.setValidator(QIntValidator())
        grid.addWidget(ediTotal, 6, 2)

        btnCancel = QPushButton('Cancel', self)
        btnCancel.resize(btnCancel.sizeHint())
        btnCancel.clicked.connect(self.Cancel)
        grid.addWidget(btnCancel, 7, 1)

        btnModify = QPushButton('Mofify', self)
        btnModify.resize(btnModify.sizeHint())
        btnModify.clicked.connect(lambda: self.Modify(ediOrga1.text(), ediOrga2.text(), ediExp1.text(), ediExp2.text(), ediRapports.text(), ediTotal.text()))
        grid.addWidget(btnModify, 7, 2)

    def Cancel(self):
        self.hide()

    def Modify(self, org_1, org_2, expl_1, expl_2, Secteurs, t ):
        global Compo_org_1
        Compo_org_1 = float(org_1)
        global Compo_org_2
        Compo_org_2 = float(org_2)
        global Taux_expl_1
        Taux_expl_1 = float(expl_1)
        global Taux_expl_2
        Taux_expl_2 = float(expl_2)
        global RapportSecteurs
        RapportSecteurs = float(Secteurs)
        global Total_t
        Total_t = float(t)

        self.hide()

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
        self.w = Window2()
        self.w.show()
        #self.hide()

    def plot2(self):
        self.figure.clf()

        #On fait les calculs pour l'année une
        DataYearOne = CalcYear()

        data = np.array(DataYearOne)

        #David utilise cette fonction pour dessiner le graph
        plotGraphSectors(self.figure, data)

        ####################################################

        Tot_1_t = gettotal(DataYearOne[0])
        Tot_2_t = gettotal(DataYearOne[1])
        Tot_3_t = gettotal(DataYearOne[2])

        ax2 = self.figure.add_subplot(234)

        squarify.plot(sizes=dynemisesizeaquar(Tot_1_t, Tot_3_t), label=["", "Total", "", ""], color=["white", "#3498db", "white", "white"], alpha=.8, ax=ax2)
        ax2.axis('off')

        ax3 = self.figure.add_subplot(235)
        squarify.plot(sizes=dynemisesizeaquar(Tot_2_t, Tot_3_t), label=["", "Total", "", ""], color=["white", "#e74c3c", "white", "white"], alpha=.8, ax=ax3)
        ax3.axis('off')

        ax4 = self.figure.add_subplot(236)
        squarify.plot(sizes=[Tot_1_t, Tot_2_t], label=['Total S1', 'Total S2'], color=['#3498db', '#e74c3c'], alpha=.8, ax=ax4)
        ax4.axis('off')

        self.canvas.draw()

app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
GUI = PrettyWidget()
sys.exit(app.exec_())