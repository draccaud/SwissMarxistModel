import sys

import matplotlib
import matplotlib.figure
import numpy as np
import pandas as pd
import squarify
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QLabel, QInputDialog, QLineEdit, \
    QVBoxLayout, QHBoxLayout, QFormLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Variables globales
DataYear = [0]
Compo_org_1 = 2.22
Compo_org_2 = 2.22
Taux_expl_1 = 0.35
Taux_expl_2 = 0.35
Total_t = 1496
RapportSecteurs = 1.72
Annee = 1


def plotSectors(figure, data):
    """
    Dessine le graphs des secteurs économiques
    :param figure: La figure sur laquelle le graph est crée
    :param data: Les données à afficher
    :return:
    """
    # Crée le graphique
    sectorsGraph = figure.add_subplot(211)

    # Définit la largeur des barres
    width = 0.2

    x = np.arange(len(data))

    # Définit les trois bares de secteur
    sectorsGraph.bar(x, data[:, 0], width, color='#3498db', label='Capital constant (C)')
    sectorsGraph.bar(x + width, data[:, 1], width, color='#e74c3c', label='Capital variable (V)')
    sectorsGraph.bar(x + (2 * width), data[:, 2], width, color='#f1c40f', label='Surplus (S)')



    # Définit les légendes en X
    sectorsGraph.set_xticks(x + width + width / 2)
    sectorsGraph.set_xticklabels(['Secteur 1', 'Secteur 2', 'Total'])

    # Définit la légende en y
    sectorsGraph.set_ylabel('Milliards de CHF')

    # titre
    sectorsGraph.set_title('Année ' + str(Annee))

    # Définit la grille
    sectorsGraph.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    # Affiche les légendes des barres
    #sectorsGraph.legend()

def CalcYear():
    #Total du secteur 1
    total1 = (Total_t / (RapportSecteurs + 1)) * RapportSecteurs
    #Diviseur permettant d'effectuer le prochain calcul
    dividor = Compo_org_1 + Taux_expl_1 + 1
    #Capital constant du secteur 1
    constantCapital1 = Compo_org_1 / dividor * total1
    #Capital variable du secteur 1
    variableCapital1 = constantCapital1 / Compo_org_1
    #Surplus du secteur 1
    surplus1 = variableCapital1 * Taux_expl_1

    #Total du secteur 2
    total2 = Total_t / (RapportSecteurs + 1)
    #Diviseur permettant d'effectuer le prochain calcul
    dividor = Compo_org_2 + Taux_expl_2 + 1
    #Capital constant du secteur 2
    constantCapital2 = Compo_org_2 / dividor * total2
    #Capital variable du secteur 2
    variableCapital2 = constantCapital2 / Compo_org_2
    # Surplus du secteur 2
    surplus2 = variableCapital2 * Taux_expl_2

    #Total de capital constant
    constantCapitalTotal = constantCapital1 + constantCapital2
    # Total de capital variable
    variableCapitalTotal = variableCapital1 + variableCapital2
    #Surplus total
    surplusTotal = surplus1 + surplus2

    #Accumulation totale
    Acc_t = total1 - (constantCapital1 + constantCapital2)
    # """""
    # #On convertit tout en int
    # C_1_t = int(C_1_t)
    # V_1_t = int(V_1_t)
    # S_1_t = int(S_1_t)
    # C_2_t = int(C_2_t)
    # V_2_t = int(V_2_t)
    # S_2_t = int(S_2_t)
    # C_3_t = int(C_3_t)
    # V_3_t = int(V_3_t)
    # S_3_t = int(S_3_t)
    # """""
    resultsTab = [[constantCapital1, variableCapital1, surplus1, total1, constantCapital2, variableCapital2, surplus2, total2, constantCapitalTotal, variableCapitalTotal, surplusTotal, Total_t, Acc_t]]
    return resultsTab

def caclanneesuivante(Tab):
    global Annee
    previousAccumulation = 0
    # Calcul du total des années précédentes
    if range(len(Tab)) == 0:
        previousAccumulation = (Tab[0] + Tab[1] + Tab[2]) - (Tab[0] + Tab[4])
    else:
        for i in range(len(Tab)):
            previousAccumulation = (Tab[i][0] + Tab[i][1] + Tab[i][2]) - (Tab[i][0] + Tab[i][4])

    #Capital constant du secteur 1
    constantCapital1 = Tab[Annee-2][0] + (previousAccumulation * (Compo_org_1 / (Compo_org_1 + 1)))
    #Capital varibale du secteur 2
    variableCapital1 = constantCapital1 / Compo_org_1
    #Surplus du secteur 1
    surplus1 = variableCapital1 * Taux_expl_1
    #Total du secteur 1
    sector1Total = constantCapital1 + variableCapital1 + surplus1

    constantCapital2 = Tab[(Annee-2)][4] + previousAccumulation - (constantCapital1 - Tab[Annee-2][0])
    variableCapital2 = constantCapital2 / Compo_org_2
    surplus2 = variableCapital2 * Taux_expl_2
    sector2Total = constantCapital2 + variableCapital2 + surplus2

    constantCapitalTotal = constantCapital1 +constantCapital2
    variableCapitalTotal = variableCapital1 + variableCapital2
    surplusTotal = surplus1 + surplus2
    sectorsTotal = constantCapitalTotal + variableCapitalTotal + surplusTotal

    # Calcule des C des années précédente pour l'accumulation total
    Accumulation = Tab[(Annee - 2)][12]
    for i in range(len(Tab) - 1, -1, -1):
        Accumulation = Accumulation - Tab[i][0]

    Acc = sector1Total - constantCapitalTotal
    NewRow = [constantCapital1, variableCapital1, surplus1, sector1Total, constantCapital2, variableCapital2, surplus2, sector2Total, constantCapitalTotal, variableCapitalTotal, surplusTotal, sectorsTotal, Acc]
    Tab.append(NewRow)
    return Tab

def gettotal(TabResultats):
    Total = 0
    for i in range(len(TabResultats)):
        Total = Total + TabResultats[i]
    return Total


# def dynemisesizeaquar(value, total):
#     AffValue = value / total
#     AffPro = (1 - AffValue) / 3
#     AffichageDynamique = [AffPro, AffValue, AffPro, AffPro]
#     return AffichageDynamique

class ParamWidget(QWidget):
    """
    Fenêtre de modification des paramètres
    """

    def __init__(self):
        """
        Constructeur de la fenêtre des paramètres
        """
        super(ParamWidget, self).__init__()
        self.initParamWidget()

    def initParamWidget(self):
        """
        Initialise la fenêtre des paramètres
        :return:
        """
        # Taille du widget
        self.setGeometry(100, 100, 800, 480)

        #Layout des paramètres
        paramLayout = QFormLayout()
        self.setLayout(paramLayout)
        paramLayout.setContentsMargins(150, 100, 150, 0)

        #Taux d'exploitation du secteur 1
        labExp1 = QLabel("Taux d'exploitation du secteur 1 :", self)
        ediExp1 = QLineEdit(str(Taux_expl_1))
        paramLayout.addRow(labExp1, ediExp1)

        #Taux d'exploitation du secteur 2
        labExp2 = QLabel("Taux d'exploitation du secteur 2 :", self)
        ediExp2 = QLineEdit(str(Taux_expl_2))
        paramLayout.addRow(labExp2, ediExp2)

        #Composition organique du secteur 1
        labOrga1 = QLabel("Composition organique du secteur 1 :", self)
        ediOrga1 = QLineEdit(str(Compo_org_1))
        paramLayout.addRow(labOrga1, ediOrga1)

        #Composition organique du secteur 2
        labOrga2 = QLabel("Composition organique du secteur 2 :", self)
        ediOrga2 = QLineEdit(str(Compo_org_2))
        paramLayout.addRow(labOrga2, ediOrga2)

        #Rapport secteurs 1 et 2
        labRapports = QLabel("Rapports entre les secteurs :", self)
        ediRapports = QLineEdit(str(RapportSecteurs))
        paramLayout.addRow(labRapports, ediRapports)

        #Total
        labTotal = QLabel("Total :", self)
        ediTotal = QLineEdit(str(Total_t))
        paramLayout.addRow(labTotal, ediTotal)

        # Bouton annuler
        btnCancel = QPushButton(self)
        btnCancel.clicked.connect(self.Cancel)
        btnCancel.setIcon(QIcon("cancel.png"))

        # Bouton enregistrer
        btnSave = QPushButton(self)
        btnSave.setIcon(QIcon("save.png"))
        btnSave.clicked.connect(
            lambda: self.Save(ediOrga1.text(), ediOrga2.text(), ediExp1.text(), ediExp2.text(), ediRapports.text(),
                              ediTotal.text()))

        paramLayout.addRow(btnCancel, btnSave)

    def Cancel(self):
        """
        Annule la modification des paramètres et ferme la fenêtre
        :return:
        """
        self.hide()

    def Save(self, orga1, orga2, expl1, expl2, sectors, total):
        """
        Enregistre les nouvelles valeurs des paramètres
        :param orga1: Nouvelle composition organique du secteur 1
        :param orga2: Nouvelle composition organique du secteur 2
        :param expl1: Nouveaux taux d'exploitation du secteur 1
        :param expl2: Nouveaux taux d'exploitation du secteur 2
        :param sectors: Nouveau rapport entre les secteurs
        :param total: Nouveau total
        :return:
        """
        # Modifie les valeurs des paramètres globaux
        global Compo_org_1
        Compo_org_1 = float(orga1)

        global Compo_org_2
        Compo_org_2 = float(orga2)

        global Taux_expl_1
        Taux_expl_1 = float(expl1)

        global Taux_expl_2
        Taux_expl_2 = float(expl2)

        global RapportSecteurs
        RapportSecteurs = float(sectors)

        global Total_t
        Total_t = float(total)

        # Réactualise les graphiques
        mainWidget.plotGraphs()

        # Ferme le widget des paramètres
        self.hide()

class MainWidget(QWidget):
    """
    Fenêtre principale de l'application
    """

    def __init__(self):
        """
        Constructeur de la fenêtre principale
        """
        super(MainWidget, self).__init__()
        self.initMainWidget()

    def initMainWidget(self):
        """
        Initialise la fenêtre principale
        :return:
        """
        self.setGeometry(100, 100, 800, 480)

        #Layout principal
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        #Haut de la fenêtre
        topLayout = QHBoxLayout()

        #Bouton info
        btnInfo = QPushButton(self)
        btnInfo.setIcon(QIcon("info.png"))
        btnInfo.clicked.connect(self.plot_clustered_stacked)
        topLayout.addWidget(btnInfo)

        #Bouton reset
        btnReset = QPushButton(self)
        btnReset.setIcon(QIcon("reset.png"))
        btnReset.clicked.connect(self.reset)
        topLayout.addWidget(btnReset)

        #Bouton paramètres
        btnParam = QPushButton(self)
        btnParam.setIcon(QIcon("parameters.png"))
        btnParam.clicked.connect(self.openParamWidget)
        topLayout.addWidget(btnParam)

        mainLayout.addLayout(topLayout)

        #Figure et Canvas acceuilant les graphs
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvas(self.figure)
        mainLayout.addWidget(self.canvas)

        #Layout du bas
        bottomLayout = QHBoxLayout()

        # Bouton reload
        btnReload = QPushButton(self)
        btnReload.setIcon(QIcon("reload.png"))
        btnReload.clicked.connect(self.reload)
        bottomLayout.addWidget(btnReload)

        #Bouton étape précédente
        btnPreviousStep = QPushButton(self)
        btnPreviousStep.setIcon(QIcon("previous.png"))
        btnPreviousStep.clicked.connect(self.previousStep)
        bottomLayout.addWidget(btnPreviousStep)

        # Bouton étape par étape
        btnNextSmallStep = QPushButton(self)
        btnNextSmallStep.setIcon(QIcon("next.png"))
        #btnNextSmallStep.clicked.connect(self.btnNextSmallStep)
        bottomLayout.addWidget(btnNextSmallStep)

        # Bouton prochaine année
        btnNextStep = QPushButton(self)
        btnNextStep.setIcon(QIcon("fast-forward.png"))
        btnNextStep.clicked.connect(self.nextStep)
        bottomLayout.addWidget(btnNextStep)

        mainLayout.addLayout(bottomLayout)

        #Dessine les graphiques
        self.plotGraphs()
        self.show()

    def openParamWidget(self):
        """
        Instancie, puis affiche une fenêtre de modification des paramètres
        :return:
        """

        self.paramWidget = ParamWidget()
        self.paramWidget.show()
        # self.hide()

    def reset(self):
        """
        Remet à zéro les paramètres et affiche le graph initial
        :return:
        """
        #Remet à zéro les paramètres
        global DataYear
        DataYear = [0]
        global Compo_org_1
        Compo_org_1 = 2.22
        global Compo_org_2
        Compo_org_2 = 2.22
        global Taux_expl_1
        Taux_expl_1 = 0.35
        global Taux_expl_2
        Taux_expl_2 = 0.35
        global Total_t
        Total_t = 1496
        global RapportSecteurs
        RapportSecteurs = 1.72
        global Annee
        Annee = 1

        #Dessine le graphique
        self.plotGraphs()

    def openInfoWidget(self):
        return

    def plotGraphs(self):
        """
        Dessine les graphiques sur la page principale
        :return:
        """
        global DataYear

        # Remise à zéro
        self.figure.clf()

        if Annee == 1:
            DataYear = CalcYear()

        GraphData = [[DataYear[Annee - 1][0], DataYear[Annee - 1][1], DataYear[Annee - 1][2]], [DataYear[Annee - 1][4],
                     DataYear[Annee - 1][5], DataYear[Annee - 1][6]], [DataYear[Annee - 1][8], DataYear[Annee - 1][9],
                     DataYear[Annee - 1][10]]]
        Tot_1_t = DataYear[Annee - 1][3]
        Tot_2_t = DataYear[Annee - 1][7]

        #Dessine le graphique des secteurs
        #GraphData = [DataYear[Annee - 1][0], DataYear[Annee - 1][1],DataYear[Annee - 1][2],DataYear[Annee - 1][4],DataYear[Annee - 1][5],DataYear[Annee - 1][6], DataYear[Annee - 1][8],DataYear[Annee - 1][9],DataYear[Annee - 1][10]]

        plotSectors(self.figure, np.array(GraphData))

        #Dessine le graphique des totaux
        #Tot_1_t = DataYear[Annee - 1][3]
        #Tot_2_t = DataYear[Annee - 1][7]
        #Tot_3_t = gettotal(DataYearOne[2])

        totalsGraph = self.figure.add_subplot(212)
        squarify.plot(sizes=[Tot_1_t, Tot_2_t], label=['Total S1', 'Total S2'], color=['#3498db', '#e74c3c'], alpha=.8,
                      ax=totalsGraph)
        totalsGraph.axis('off')

        self.canvas.draw()

    def nextStep(self):
        global Annee
        global DataYear
        Annee = Annee + 1
        # Si année une

        if not DataYear[Annee-2]:
            None

        else:
            DataYear = caclanneesuivante(DataYear)
        self.plotGraphs()

    def previousStep(self):
        global Annee
        if Annee > 1:
            Annee = Annee - 1
        else:
            None
        self.plotGraphs()

    def reload(self):
        global Annee
        global DataYear
        Annee = 1
        del DataYear
        self.plotGraphs()




    def plot_clustered_stacked(self, dfall = [], **kwargs):

        # create fake dataframes
        # Les c
        df1 = pd.DataFrame(np.array([[111, 0], [121, 122], [131, 0]]))

        # Les v
        df2 = pd.DataFrame(np.array([[211, 212], [221, 222], [231, 232]]))

        # Les s
        df3 = pd.DataFrame(np.array([[311, 312], [321, 322], [331, 332]]))

        dfall = [df1, df2, df3]

        self.figure.clf()

        axe = self.figure.add_subplot(111)

        for df in dfall:  # for each data frame
            axe = df.plot(kind="bar",
                          linewidth=0,
                          stacked=True,
                          ax=axe,
                          legend=False,
                          grid=False,
                          **kwargs)  # make bar plots

        count = 0

        h, l = axe.get_legend_handles_labels()  # get the handles we want to modify
        for i in range(0, 6, 2):  # len(h) = n_col * n_df
            for j, pa in enumerate(h[i:i + 2]):
                for rect in pa.patches:  # for each index
                    rect.set_x(rect.get_x() + 1 / 4 * i / 2)
                    rect.set_width(1 / 4)

                    if count <= 2:
                        rect.set_color("blue")
                    elif count == 6 or count == 7 or count == 8:
                        rect.set_color("red")
                    elif count == 12 or count == 13 or count == 14:
                        rect.set_color("yellow")

                    count = count + 1

        axe.set_xticks((np.arange(0, 6, 2) + 1 / 4) / 2)
        axe.set_xticklabels(["Secteur 1", "Secteur 2", "Total"], rotation=0)

        l1 = axe.legend(h[:2], ["base", "ajout"], loc=[1.01, 0.5])

        axe.add_artist(l1)

        self.canvas.draw()

        return axe


app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
mainWidget = MainWidget()
sys.exit(app.exec_())
