

# RESOLUTION DU RUBIK PAR PATRICE WEISZ (c) 2020
# INITIATION A PYTHON DANS CINEMA 4D
# EXEMPLE DE PLUGIN R23    PYTHON 3.7.7



# SECTION DES VARIABLES GLOBALES
TEST = 'LdFFfFFblFfubrlDuuBf'
ALEA = 40  # nombre de rotations aleatoires du melange
VITESSE = 10 # vitesse de rotations des effecteurs
TEXT1 = 2001
TXT_MELANGE = 2002
TEXT2 = 2003
TEXT3 = 2004
BTN_PLAY = 1001
BTN_CANCEL = 1002
BTN_ALEA = 1003
BTN_INVERSE = 1004
BTN_METHODE = 1005
BTN_TEST = 1006
SLIDE_VIT = 1007
SLIDE_LONG = 1008
GROUP_OPTIONS = 50000
TIRAGE = 2000


import c4d, random, copy
from c4d import gui


#PROGRAMME DE TEST UTILISE PPOUR LE DEBUGAGE
def Test():
    """ teste la methode de resolution sur N tirages aleatoires """

    print ("Debut des tests")
    for n in range(1,TIRAGE):
        #print n,
        #if n%10 ==0:
            #print
        cha = MelangeCubes.MelangeAleatoire()
        print (cha)
        Cubes.PosiDebut()  # init le modele dans Cube.posi
        Cube_test = Cubes.posi.copy()
        Methode.RotCubes(cha)
        MelangeCubes.etape.ecrit('modele', Cubes.posi)  # stocke le modele melange
        rota = Methode.Step2()  # on applique la methode
        Methode.RotCubes(rota)  # on fait tourner le modele




# METHODE DE RESOLUTION
class Methode:
    """ methode de resolution classique du rubiks'cube pour les 2 premiers layers
     et methodes Fridrich (CFOP) pour la derniere face """


    def RotCubes(cls, cha):
        """ rotation des faces du modele des cubes """
        for r in cha:
            Cubes.Rotate(r)
    RotCubes = classmethod(RotCubes)


    def Step2(cls):
        """ resoud la croix blanche
        on commence par les 4 arretes (LU,BU,RU,FU) """

        def Retourne(cube, formules):
            """ choisit la formule en fonction de l'orientation du cube """
            spins = {'L': [0, 0, 1],
                     'l': [0, 0, -1],
                     'F': [1, 0, 0],
                     'f': [-1, 0, 0],
                     'R': [0, 0, 1],
                     'r': [0, 0, -1],
                     'B': [1, 0, 0],
                     'b': [-1, 0, 0],
                     'U': [0, 1, 0],
                     'u': [0, -1, 0],
                     'D': [0, 1, 0],
                     'd': [0, -1, 0],
                     }
            delta = [0, 0, 0]
            for r in formules:  # on calcule le delta spin des formules
                delta = [a + b for a, b in zip(spins[r], delta)]
            delta = [a + b for a, b in zip(delta, cube[1])]
            delta = [delta[0] % 4, delta[1] % 4, delta[2] % 4]
            if (delta == [0, 0, 0]) or (delta == [2, 2, 2]) or (delta == [2, 0, 2]):
                return 0  # la 1ere formule fonctionne
            else:
                return 1  # on retourne la 2e formule

        c4d.CallCommand(13957) # efface la console'
        Cubes.posi = MelangeCubes.etape.lit('modele')
        posform = {}
        rota = {}
        posform['LU'] = {'LU': '',  # rotation calculant le spin si direct
                         'LB': 'L',
                         'LD': 'LL',
                         'LF': 'l',
                         'FU': 'U',
                         'FD': 'Fl',
                         'RF': 'Fdll',
                         'RU': 'UU',
                         'RB': 'RDDLL',
                         'RD': 'DDLL',
                         'BU': 'u',
                         'BD': 'DLL'
                         }
        rota['LU'] = {'LU': ['', 'ufUl'],  # rotations ramenant LU a sa place
                      'LB': ['L', 'BDLL'],  # direct ou inverse
                      'LD': ['LL', 'fDFl'],
                      'LF': ['l', 'fdFLL'],
                      'FU': ['FFdll', 'fl'],
                      'RF': ['Fdllf', 'FFlff'],
                      'FD': ['Fl', 'dLL'],
                      'RU': ['RRDDLL', 'RRdFlf'],
                      'RB': ['RDDLLr', 'RdFlfR'],
                      'RD': ['DDLL', 'dFlf'],
                      'BU': ['BUbu', 'BL'],
                      'BD': ['DLL', 'bLB']
                      }
        posform['BU'] = {'LU': 'LLdBB',  # rotations calculant le spin si direct
                         'LB': 'b',
                         'LD': 'dBB',
                         'LF': 'LdBB',
                         'FU': 'FFDDBB',
                         'RF': 'rDBB',
                         'FD': 'DDBB',
                         'RU': 'RRDBB',
                         'RB': 'B',
                         'RD': 'DBB',
                         'BU': '',
                         'BD': 'BB'
                         }
        rota['BU'] = {'LU': ['LLdBB', 'lb'],  # rotations ramenant BU a sa place
                      'LB': ['b', 'ldLBB'],  # direct ou inverse
                      'LD': ['dBB', 'Lbl'],
                      'LF': ['LdBBl', 'fDDBBF'],
                      'FU': ['FFDDBB', 'fLdBBl'],
                      'RF': ['rDBBR', 'FDDBBf'],
                      'FD': ['DDBB', 'dLbl'],
                      'RU': ['RRDBB', 'RB'],
                      'RB': ['B', 'RDBBr'],
                      'RD': ['DBB', 'rBR'],
                      'BU': ['', 'bRDrBB'],
                      'BD': ['BB', 'DLbl']
                      }
        posform['RU'] = {'LU': 'LLDDRR',  # rotations calculant le spin si direct
                         'LB': 'lDDRR',
                         'LD': 'DDRR',
                         'LF': 'fDRR',
                         'FU': 'FFDRR',
                         'RF': 'R',
                         'FD': 'fR',
                         'RU': '',
                         'RB': 'r',
                         'RD': 'RR',
                         'BU': 'br',
                         'BD': 'dRR'
                         }
        rota['RU'] = {'LU': ['LLDDRR', 'LLDfRF'],  # rotations ramenant RU a sa place
                      'LB': ['lDDRRL', 'BBrBB'],  #Bdrrb direct ou inverse
                      'LD': ['DDRR', 'DfRF'],
                      'LF': ['fDRRF', 'FFRFF'],
                      'FU': ['FFDRR', 'FRf'],
                      'RF': ['R', 'FDRRf'],
                      'FD': ['fRF', 'DRR'],
                      'RU': ['', 'rFDRRf'],
                      'RB': ['r', 'bdBRR'],
                      'RD': ['RR', 'RFDRRf'],
                      'BU': ['br', 'buBU'],
                      'BD': ['dRR', 'Brb']
                      }
        posform['FU'] = {'LU': 'LF',  # rotations calculant le spin si direct
                         'LB': 'lDFF',
                         'LD': 'DFF',
                         'LF': 'F',
                         'FU': '',
                         'RF': 'f',
                         'FD': 'FF',
                         'RU': 'rf',
                         'RB': 'RdFF',
                         'RD': 'dFF',
                         'BU': 'BBDDFF',
                         'BD': 'DDFF'
                         }
        rota['FU'] = {'LU': ['LF', 'LLDFF'],  # rotations ramenant FU a sa place
                      'LB': ['lDFFL', 'LLFLL'],  # direct ou inverse
                      'LD': ['DFF', 'lFL'],
                      'LF': ['F', 'LDlFF'],
                      'FU': ['', 'fLDlFF'],
                      'RF': ['f', 'rdRFF'],
                      'FD': ['FF', 'FLDlFF'],
                      'RU': ['rf', 'ruRU'],
                      'RB': ['RdFFr', 'RRfRR'],
                      'RD': ['dFF', 'Rfr'],
                      'BU': ['BBDDFF', 'bRdrFF'],
                      'BD': ['DDFF', 'dRfr']
                      }
        rots = ''
        nom_cube = lambda n: n[0]
        for cub in ['LU', 'BU','RU','RU','FU']:
            pos = [p[0] for p in Cubes.posi.values()].index(cub)#python 2 et 3
            positcub = list(Cubes.posi.keys())[pos]# python 2 et 3
            rotmod = rota[cub][positcub][Retourne(Cubes.posi[positcub], posform[cub][positcub])]
            Methode.RotCubes(rotmod)  # rotation du modele
            rots += rotmod
        return rots  + Methode.Step3()
    Step2 = classmethod(Step2)


    def Step3(cls):
        """ ordonne les 4 coins blancs
        on amene le cube a sa position puis on l'oriente"""

        posform = {}
        rota = {}
        posform['LBU'] = {'LBU': '',  # position des 8 coins
                          'RUB': 'RlDLr',  # chaine qui le remet à sa place
                          'RFU': 'rBDDbR',
                          'LUF': 'BfdbF',
                          'LBD': 'ldL',
                          'RBD': 'lDL',
                          'RDF': 'lDDL',
                          'LFD': 'Bdb'
                          }
        posform['RUB'] = {'LBU': 'lRdrL',  # position des 8 coins
                          'RUB': '',  # chaine qui le remet à sa place
                          'RFU': 'FbDBf',
                          'LUF': 'LRDDrl',
                          'LBD': 'Rdr',
                          'RBD': 'RDr',
                          'RDF': 'bDB',
                          'LFD': 'bDDB'
                          }
        posform['RFU'] = {'LBU': 'BrDDRb',  # position des 8 coins
                          'RUB': 'bGdfB',  # chaine qui le remet à sa place
                          'RFU': '',
                          'LUF': 'LrDRl',
                          'LBD': 'rDDR',
                          'RBD': 'Fdf',
                          'RDF': 'rdR',
                          'LFD': 'rDR'
                          }
        posform['LUF'] = {'LBU': 'fBDFb',  # position des 8 coins
                          'RUB': 'LRDDlr',  # chaine qui le remet à sa place
                          'RFU': 'LrdlR',
                          'LUF': '',
                          'LBD': 'fDF',
                          'RBD': 'LDDl',
                          'RDF': 'Ldl',
                          'LFD': 'LDl'
                          }
        rota['LBU'] = 'BdbldL'  # chaine d'orientation x1 ou x2 pour le tourner
        rota['RUB'] = 'RdrbdB'
        rota['RFU'] = 'FdfrdR'
        rota['LUF'] = 'LdlfdF'
        rots = ''
        nom_cube = lambda n: n[0]
        for cub in ['LBU', 'RUB', 'RFU', 'LUF']:
            pos = [p[0] for p in Cubes.posi.values()].index(cub)#python 2 et 3
            positcub = list(Cubes.posi.keys())[pos]# python 2 et 3
            rotmod = posform[cub][positcub]  # chaine qui ramene le cube a sa place
            ori = Cubes.posi[positcub][2]  # orientation du cube/
            Methode.RotCubes(rotmod)  # on fait tourner le modele
            positcub = Cubes.posi[cub][0]
            assert cub == positcub, "pas a la bonne place"  # erreur si mauvaise chaine
            ori = Cubes.posi[positcub][2]  # orientation du cube/
            if ori != 'U':
                Methode.RotCubes(rota[cub])  # on fait tourner 1x le modele
                rotmod += rota[cub]
                ori = Cubes.posi[positcub][2]  # orientation du cube
                if ori != 'U':
                    Methode.RotCubes(rota[cub])  # on fait tourner 1x le modele
                    rotmod += rota[cub]
                    ori = Cubes.posi[positcub][2]  # orientation du cube
            assert ori == 'U', "ori =" + ori  # devrait etre bien orienté
            rots += rotmod
        Methode.RotCubes('$')  # rotation du modele rubik de 180°
        rots += '$'
        return rots + Methode.Step4()

    Step3 = classmethod(Step3)

    def Step4(cls):
        """ ordonne le 2e layer, soit les 4 arretes du milieu
            on les positionne au-dessus du centre (cube inverse)
            et selon leur orientation on applique la bonne chaine de rotation"""

        def TranspCotes(cha, D, A):
            """ transpose la formule en faisant une permutation circulaire des cotes """
            rots = {}
            rots['F'] = 'LlFfRrBbUuDd'  # sens normal
            rots['L'] = 'BbLlFfRrUuDd'  # transposition  F-->L
            rots['B'] = 'RrBbLlFfUuDd'  # transposition  F-->B
            rots['R'] = 'FfRrBbLlUuDd'  # transposition  F-->R
            if cha == '':
                return ''
            else:
                return ''.join([rots[A][rots[D].index(r)] for r in cha])

        posform = {}
        FL = 'ulULUFuf'  # formule de la methode pour le mettre a gauche
        FR = 'URurufUF'  # formule de la methode pour le mettre a droite

        posform['LF'] = {'LU': ['L', TranspCotes(FR, 'F', 'L'), 'u' + FL],
                         'FU': ['F', 'U' + TranspCotes(FR, 'F', 'L'), FL],
                         'RU': ['R', 'UU' + TranspCotes(FR, 'F', 'L'), 'U' + FL],
                         'BU': ['B', 'u' + TranspCotes(FR, 'F', 'L'), 'UU' + FL],
                         'LF': ['L', '', FL],
                         'RF': ['O', '', FR],  # orientation indifferente
                         'LB': ['O', '', TranspCotes(FL, 'F', 'L')],
                         'RB': ['O', '', TranspCotes(FR, 'F', 'R')]
                         }
        posform['LB'] = {'LU': ['L', TranspCotes(FL, 'F', 'L'), 'U' + TranspCotes(FR, 'F', 'B')],
                         'FU': ['F', 'U' + TranspCotes(FL, 'F', 'L'), 'UU' + TranspCotes(FR, 'F', 'B')],
                         'RU': ['R', 'UU' + TranspCotes(FL, 'F', 'L'), 'u' + TranspCotes(FR, 'F', 'B')],
                         'BU': ['B', 'u' + TranspCotes(FL, 'F', 'L'),TranspCotes(FR, 'F', 'B')],
                         'LF': ['O', '', FL],
                         'RF': ['O', '', FR],  # orientation indifferente
                         'LB': ['L', '', TranspCotes(FL, 'F', 'L')],
                         'RB': ['O', '', TranspCotes(FR, 'F', 'R')]
                         }
        posform['RF'] = {'LU': ['L', 'UU' + TranspCotes(FL, 'F', 'R'), 'u' + FR],
                         'FU': ['F', 'u' + TranspCotes(FL, 'F', 'R'), FR],
                         'RU': ['R', TranspCotes(FL, 'F', 'R'), 'U' + FR],
                         'BU': ['B', 'U' + TranspCotes(FL, 'F', 'R'), 'UU' + FR],
                         'LF': ['O', '', FL],  # orientation indifferente
                         'RF': ['R', '', FR],
                         'LB': ['O', '', TranspCotes(FL, 'F', 'L')],
                         'RB': ['O', '', TranspCotes(FR, 'F', 'R')]
                         }
        posform['RB'] = {'LU': ['L', 'UU' + TranspCotes(FR, 'F', 'R'), 'U' + TranspCotes(FL, 'F', 'B')],
                         'FU': ['F', 'u' + TranspCotes(FR, 'F', 'R'), 'UU' + TranspCotes(FL, 'F', 'B')],
                         'RU': ['R', TranspCotes(FR, 'F', 'R'), 'u' + TranspCotes(FL, 'F', 'B')],
                         'BU': ['B', 'U' + TranspCotes(FR, 'F', 'R'), TranspCotes(FL, 'F', 'B')],
                         'LF': ['O', '', FL],
                         'RF': ['O', '', FR],  # orientation indifferente
                         'LB': ['O', '', TranspCotes(FL, 'F', 'L')],
                         'RB': ['R', '', TranspCotes(FR, 'F', 'R')]
                         }
        restants = ['LF','LB', 'RF', 'RB']  # cubes d'arrete a placer
        i = 0
        rots = rot = ''
        posUp = ('LU', 'FU', 'BU', 'RU')  # les 4 positions utilisables
        nom_cube = lambda n: n[0]
        j = 0
        while len(restants) != 0 and j < 20:  # algo pour les 4 arretes
            cub = restants[i]
            pos = [p[0] for p in Cubes.posi.values()].index(cub)#python 2 et 3
            positcub = list(Cubes.posi.keys())[pos]# python 2 et 3
            depl = posform[cub][positcub]
            if positcub in posUp:
                if ori == depl[0]:  # cube bien oriente
                    rot = depl[1]  # on le met a sa place
                else:
                    rot = depl[2]  # cube mal oriente on prend la 2e formule
                restants.pop(i)  # on retire le cube des cubes restants a placer
                i = 0
                Methode.RotCubes(rot)
                rots += rot
            else:
                if i < len(restants) - 1:  # on change de cube
                    i = (i + 1) % len(restants)
                else:  # on remonte le cube si besoin
                    if ori == depl[0]:
                        restants.pop()  # on retire le cube bien placé
                        i = 0
                    else:
                        rot = depl[2]  # on remonte le cube
                        Methode.RotCubes(rot)
                        rots += rot
            j += 1
        return rots + Methode.Step5(rots)  # retour de la chaine pour Step4
    Step4 = classmethod(Step4)

    def Step5(cls, rots):
        """ ordonne toutes les faces jaunes du 3e layer selon la méthode Fridrich
         appelé aussi CFOP, CROSS, F2L (FIRST TWO LAYER), OLL et PLL.
            il y 57 motifs jaunes obtenus après avoir fini les 2 layers avec step4
            On les appelle les OLL (ORIENTATIONS LAST LAYER) """

        # Les patterns jaunes sont codés avec leur orientation
        # U si face en haut et L si oriente vers la gauche, etc.
        # ex, dans BUBLUUFFF il y a 3 faces jaunes UP

        # NOTATIONS UTILISEES :
        # Pour les formules de rotations, on garde les formules
        # avec les notations originales afin de les controler facilement
        # puis on les convertit dans notre notation sur 1 seul caractere
        #
        # rappel de notre notation simple :
        # LFRUBD : faces Left, Front, Right, Up, Back, Down sens horloge
        # lfrubd : faces tournées en sens inverse au lieu de : (L',F',R',U',B',D')
        #
        # Notations 2 rotations successives :
        # U2,R2 : UU, RR etc.
        # rotations du milieu :
        # M,m : middle layer entre L et R meme sens que L
        # E,e : Equatorial layer entre U et D meme sens que D
        # S,s : Standing layer entre F et B meme sens que F
        #
        # Notations pour 2 layers à la fois :
        # Attention : dans notre notation on utilise deja les lettres f,u,r,b,l,d pour les sens inverses,
        # donc on en introduit d'autres (G,H,I,K,N,O) pas encore utilisees pour
        # les rotations de 2 layers simultanes :
        # G,g''  (f,f') : FS, fs
        #      (u,u') : Ue, uE
        # A,r' (r,r') : Rm, rM
        #      (b,b') : Bs, bS
        # C,l' (l,l') : LM, lm
        #      (d,d') : DE, de
        #
        # on traduit donc avec notre notation sur une seule lettre dans patt_OLL :

        patt_OLL = {' 0': ('', 'f’'),
                    ' 1': ('LBRLURLFR', 'R U2 R2 F R F’ U2 R’ F R F’'),
                    ' 2': ('LBBLURLFF', 'F R U R’ U’ F’ f R U R’ U’ f’'),
                    ' 3': ('LBBLURFFU', 'l L2 U’ L U’ l’ U2 l U’ L l’'),
                    ' 4': ('BBRLURUFF', 'r’ R2 U R’ U r U2 r’ U R’ r'),
                    ' 5': ('UBULURLFR', 'r’ U2 R U R’ U r2 U2 R’ U’ R U’ r’'),
                    ' 6': ('UBULURFFF', 'r U R’ U R U2 r2 U’ R U’ R’ U2 r'),
                    ' 7': ('UBBLURLFU', 'R U R’ U R’ F R F’ U2 R’ F R F’'),
                    ' 8': ('UBULURUFU', 'r’ R U R U R’ U’ r2 R2 U R U’ r’'),
                    ' 9': ('LURLURLUR', 'R U2 R2 U’ R U’ R’ U2 F R F’'),
                    '10': ('LBRUUULFR', 'F R U R’ U’ R F’ r U R’ U’ r’'),
                    '11': ('LBBUUULFF', 'f R U R’ U’ R U R’ U’ f'),
                    '12': ('BURLURFUR', 'R’ U’ R U’ R’ U F’ U F R'),
                    '13': ('BUBUURFFF', 'r U2 R’ U’ R U R’ U’ R U’ r’'),
                    '14': ('BUBLUUFFF', 'l’ U2 L U L’ U’ L U L’ U l'),
                    '15': ('LURUURFFF', 'F R’ F2 L F2 R F2 L’ F'),
                    '16': ('LURLUUFFF', 'F’ L F2 R’ F2 L’ F2 R F’'),
                    '17': ('LUBUURLFF', 'F R U R’ U’ R U R’ U’ F’'),
                    '18': ('BURLUUFFR', 'F’ L’ U’ L U L’ U’ L U F'),
                    '19': ('BURUURUFF', 'r U R’ U R U2 r’'),
                    '20': ('LUBLUUFFU', 'l’ U’ L U’ L’ U2 l'),
                    '21': ('UUBLUUFFR', 'r R2 U’ R U’ R’ U2 R U’ R r’'),
                    '22': ('BUUUURLFF', 'l’ L2 U L’ U L U2 L’ U L’ l'),
                    '23': ('LUBUURFFU', 'R’ U’ R F R’ F’ U F R F’'),
                    '24': ('BURLUUUFF', 'L U L’ F’ L F U’ F’ L’ F'),
                    '25': ('UURUURLFF', 'l’ U2 L U L’ U l'),
                    '26': ('LUULUUFFR', 'r U2 R’ U’ R U’ r’'),
                    '27': ('BBRUUUUFF', 'F U R U2 R’ U’ R U R’ F’'),
                    '28': ('LBBUUUFFU', 'F’ U’ L’ U2 L U L’ U’ L F'),
                    '29': ('BBRUUULFU', 'r’ U’ r R’ U’ R U r’ U r'),
                    '30': ('LBBUUUUFR', 'l U l’ L U L’ U’ l U’ l’'),  # **********
                    '31': ('BUBUURUFU', 'R U R’ U R U2 R’ F R U R’ U’ F’'),
                    '32': ('BUBLUUUFU', 'L’ U’ L U’ L’ U2 L F’ L’ U’ L U F'),
                    '33': ('BUUUURFFU', 'R U R’ U’ R U’ R’ F’ U’ F R U R’'),
                    '34': ('UUBLUUUFF', 'L’ U’ L U L’ U L F U F’ L’ U’ L'),
                    '35': ('BUULUUFFU', 'R’ U’ F U R U’ R’ F’ R'),
                    '36': ('UUBUURUFF', 'L U F’ U’ L’ U L F L’'),
                    '37': ('UURUURFFU', 'F R’ F’ R U R U’ R’'),
                    '38': ('LBULUULUU', 'f R U R’ U’ f’'),
                    '39': ('UBRUURUUR', 'f’ L’ U’ L U f'),
                    '40': ('UBRLUUFUU', 'R U2 R2 F R F’ R U2 R’'),
                    '41': ('LBUUUULFU', 'F R U R’ U’ F’'),
                    '42': ('BBUUUUFFU', 'R U R’ U’ R’ F R F’'),
                    '43': ('BBUUUUUFR', 'L F’ L’ U’ L U F U’ L’'),
                    '44': ('UBBUUULFU', 'R’ F R U R’ U’ F’ U R'),
                    '45': ('UUBLURUUF', 'F U F’ U’ R’ F’ L F r’ R r L’'),# ajout de r L' a la fin'
                    '46': ('UURLURUUR', 'R’ U’ R’ F R F’ U R'),
                    '47': ('BUUUURUFR', 'R U R’ U R U’ R’ U’ R’ F R F’'),
                    '48': ('UUBLUULFU', 'L’ U’ L U’ L’ U L U L F’ L’ F'),
                    '49': ('BUBUUUFUF', 'R U2 R’ U’ R U R’ U’ R U’ R’'),
                    '50': ('LUBUUULUF', 'R U2 R2 U’ R2 U’ R2 U2 R'),
                    '51': ('BUBUUUUUU', 'R’ U2 R F U’ R’ U’ R U F’'),
                    '52': ('BUUUUUFUU', 'r U R’ U’ r’ F R F’'),
                    '53': ('UURUUUFUU', 'F R’ F’ r U R U’ r’'),
                    '54': ('LUBUUUFUU', 'L’ U’ L U’ L’ U2 L'),
                    '55': ('BURUUUUUF', 'R U R’ U R U2 R’'),
                    '56': ('UUUUURUFU', 'r U R’ U’ r’ R U R U’ R’'),
                    '57': ('UBUUUUUFU', 'R U R’ U’ R’ r U R U’ r’'),
                    '58': ('UUUUUUUUU', '')  # face jaune deja faite
                    }
        patt_pw = Methode.RemplaceForms(patt_OLL) # modifie les formules

        emp_jau = {}
        emp_jau['F'] = ['LBU', 'BU', 'RUB', 'LU', 'U', 'RU', 'LUF', 'FU', 'RFU']
        emp_jau['L'] = ['RUB', 'RU', 'RFU', 'BU', 'U', 'FU', 'LBU', 'LU', 'LUF']
        emp_jau['B'] = ['RFU', 'FU', 'LUF', 'RU', 'U', 'LU', 'RUB', 'BU', 'LBU']
        emp_jau['R'] = ['LUF', 'LU', 'LBU', 'FU', 'U', 'BU', 'RFU', 'RU', 'RUB']

        # on permute circulairement les orientations
        perm_ori = {'F': {'U': 'U', 'L': 'L', 'B': 'B', 'R': 'R', 'F': 'F'},
                    'L': {'U': 'U', 'L': 'F', 'B': 'L', 'R': 'B', 'F': 'R'},
                    'B': {'U': 'U', 'L': 'R', 'B': 'F', 'R': 'L', 'F': 'B'},
                    'R': {'U': 'U', 'L': 'B', 'B': 'R', 'R': 'F', 'F': 'L'}
                    }

        # fabrique les 4 pattern jaunes possibles a partir du modele
        patt_j = {'F': '', 'L': '', 'B': '', 'R': ''}
        pivot_j = {'F': '', 'L': 'u', 'B': 'UU', 'R': 'U'}
        for face in ['F', 'L', 'B', 'R']:  # on genere les 4 patterns possibles
            for emp in emp_jau[face]:
                patt_j[face] += perm_ori[face][Cubes.posi[emp][2]]  # concatene l'orientation

        # recherche dans la liste des patterns corrigees :
        sol = False
        for p in sorted(patt_pw.keys()):
            for face in ['F', 'L', 'B', 'R']:  # on teste les 4 patterns jaunes
                if patt_pw[p][0] == patt_j[face]:
                    sol = True # solution trouvee pour les faces jaunes
                    break
            if sol:
                break
        if not sol: # pas de solution
            cha = ''
        else:
            cha = pivot_j[face] + patt_pw[p][1] + pivot_j[face]
        MelangeCubes.etape.ecrit('etat', 'inversion')  # stocke etat inversion
        Methode.RotCubes(cha) # on fait tourner le modele avant l'étape suivante
        return cha + Methode.Step6(rots)  # retourne la chaine finale


    Step5 = classmethod(Step5)

    def Step6(cls, rots):
        """ finalisation de la face jaune selon la methode CFOP ou Fridrich
          on applique les formules de permutation des 21 PLL PERMUTATIONS LAST LAYER
            ces formules permutent à la fois les coins et les arretes """

        patt_PLL = {}
        patt_PLL = {'A': ('','l’ R’ D2 R U R’ D2 R U’ R'), #OK
                    'a': ('','l’ U R’ D2 R U’ R’ D2 R2'), #OK
                    'U': ('','R2 U’ R’ U’ R U R U R U’ R'), #OK
                    'u': ('','R’ U R’ U’ R’ U’ R’ U R U R2'), #OK
                    'Z': ('','U R’ U’ R U’ R U R U’ R’ U R U R2 U’ R’ U'),#OK
                    'H': ('','r2 R2 U r2 R2 U2 r2 R2 U R2 r2'), #OK
                    'J': ('','R U R’ F’ R U R’ U’ R’ F R2 U’ R’ U’'),#OK
                    'Js':('','L’ U’ L F L’ U’ L U L F’ L2 U L U'),#OK
                    'R': ('','R’ U2 R U2 R’ F R U R’ U’ R’ F’ R2 U’'),#OK
                    'Rs':('','L U2 L’ U2 L F’ L’ U’ L U L F L2 U'), #Ok
                    'T': ('','R U R’ U’ R’ F R2 U’ R’ U’ R U R’ F’'),#OK
                    'F': ('','R’ U R U’ R2 F’ U’ F U R F R’ F’ R2 U’'),
                    'V': ('','L’ U R U’ L U L’ U R’ U’ L U2 R U2 R’'),#OK
                    'E': ('','x U R’ U’ L U R U’ r2 U’ R U L U’ R’ U'), #OK
                    'N': ('','R’ U R’ F R F’ R U’ R’ F’ U F R U R’ U’ R'),#OK
                    'Ns':('','L U’ L F’ L’ F L’ U L F U’ F’ L’ U’ L U L’'),#OK
                    'Y': ('','F R U’ R’ U’ R U R’ F’ R U R’ U’ R’ F R F’'),#OK
                    'G': ('','L2 u’ L U’ L U L’ u L2 F U’ F’'),#OK
                    'g': ('','y’ R U R’ y L2 u’ L U’ L’ U L’ u L2'),#OK
                    'Gs':('','R2 u R’ U R’ U’ R u’ R2 F’ U F'),#OK
                    'gs':('','y L’ U’ L y’ R2 u R’ U R U’ R u’ R2'),#OK
                    'I': ('','')# OK
                    }

        def Compare(cubeFini,dic2):
            """ compare les positions des cubes Posi et Fini sans les spins """

            # on cree un dict sans les spins
            c_posi = {}
            for r in dic2:
                c_posi[r] = [dic2[r][0]] # on ne prend que la position
            if c_posi == cubeFini:  # compare avec le cube fini
                return True
            else:
                return False

        patt_pw = Methode.RemplaceForms(patt_PLL) # formule reecrite dans notre notation

        # algorithme de force brute sur les 22 algos pour les jaunes :
        cubeComp = copy.deepcopy(Cubes.posi) # sinon les sous-listes sont communes aux 2
        cubePasFini = copy.deepcopy(Cubes.posi)
        Cubes.PosiDebut() # position ordonne de depart de Cubes.posi
        cubeFini = copy.deepcopy(Cubes.posi) # contient e cube fini (position de depart)
        Cubes.posi = copy.deepcopy(cubePasFini) # reprend sa valeur
        for r in cubeFini:
            cubeFini[r].pop(1)   # on retire les spins pour faire la comparaison
            cubeFini[r].pop(1)   # on retire l'orientation car seule la position compte

        # applique toutes les formules PLL en tournant la face U et le cube selon y :
        for r in patt_pw:
            for face in ['','u','uu','U']: # F,L,B,R
                cha = face + patt_pw[r][1] # on fait pivoter la face jaune
                pivot =''
                for cote in range(4):     # on fait pivoter tout le cube selon y
                    pivot = 'Ued'*cote # rotations de tout le cube selon y= Ued
                    Methode.RotCubes(pivot + cha)  # on tourne Cubes.posi avec la formule cha
                    Methode.RotCubes(MelangeCubes.Inversion(pivot)) #on remet le cube en face
                    cubeComp = copy.deepcopy(Cubes.posi)
                    if Compare(cubeFini,cubeComp):
                        print ("SOLUTION TROUVEE ;-)")
                        cha = pivot + cha
                        rots += cha
                        Methode.RotCubes(MelangeCubes.Inversion(rots))#
                        return  cha
                    else:
                        Cubes.posi = copy.deepcopy(cubePasFini)      # on restaure le cube melange
        print ("PERDU : pas trouvé !!")
        return ''
    Step6 = classmethod(Step6)


    def RemplaceForms(cls,OllPll):
        """ fonction qui remplace les formules originales par notre codage sur 1 caractere """

        rotTwoP = {
            'r’': 'AM',  # 2 layers Right on met A pour r
            'l’': 'Cm',  # 2 layers Left on met C pour l
            'f’': 'Gs',  # on fait les primes d'abord on met G pour f
            'u’': 'HE'   # H pour u afin d'eviter un remplacement errone par rotTwo'
                }
        rotTwo = {
            'r': 'Rm',   # 2 layers Right
            'l': 'LM',   # 2 layers Left
            'f': 'FS',   # 2 layers Front
            'u': 'Ue'    # 2 layers Up
                }
        # x,x' : rotation complète du cube par R : Rml, rML
        # y,y' : rotation complète du cube par U : Ued, uED
        # z,z' : rotation complète du cube par F : FSb, fsB
        rotThreeP = {
            'x’': 'rML', # 3 layers (tout le cube selon x’ soit r )
            'y’': 'uED',
            'z’': 'fsB'
            }
        rotThree = {
            'x': 'Rml',  # 3 layers (tout le cube selon x soit R )
            'y': 'Ued',
            'z': 'FSb'
            }

        correct = {
            'A':'r', # on corrige et remet r,l,f a leur place pour eviter un rempl. premature
            'C':'l',
            'G':'f',
            'H':'u'
                }
        nota_pw = {'L’': 'l', 'F’': 'f', 'R’': 'r', 'B’': 'b', 'U’': 'u', 'D’': 'd'}
        rotDoub = {'L2': 'LL', 'F2': 'FF', 'R2': 'RR',
                   'B2': 'BB', 'U2': 'UU', 'D2': 'DD',
                   'l2': 'll', 'r2': 'rr'
                   }
        patt_mod = {} # dict pour les formules modifiees
        for i in OllPll:
            nouv_chain = OllPll[i][1]

            # remplace les doubles rotations U2-->UU , R2-->RR, etc.
            for r in rotDoub:
                if r in nouv_chain:
                    nouv_chain = nouv_chain.replace(r, rotDoub[r])

            # remplace les rotations de 2 layers par des simples dans patt_PW
            for r in rotTwoP:  # cherche les rot primes de 2 layers
                if r in nouv_chain:
                    nouv_chain = nouv_chain.replace(r, rotTwoP[r])  # remplace par 2 simples
            for r in rotTwo:  # cherche les rot de 2 layers
                if r in nouv_chain:
                    nouv_chain = nouv_chain.replace(r, rotTwo[r])

            # remplace les rotations de 3 layers par des simples
            for r in rotThreeP:  # cherche les rot primes de 3 layers
                if r in nouv_chain:
                    nouv_chain = nouv_chain.replace(r, rotThreeP[r])  # remplace par 3 simples
            for r in rotThree:  # cherche les rot de 3 layers
                if r in nouv_chain:
                    nouv_chain = nouv_chain.replace(r, rotThree[r])  # remplace par 3

            for r in correct:  # on remet les minuscules
                if r in nouv_chain:
                    nouv_chain = nouv_chain.replace(r, correct[r])  # remplac
            for r in nota_pw:  # cherche et remplace les L',U' etc par des l,u
                if r in nota_pw:
                    nouv_chain = nouv_chain.replace(r, nota_pw[r])
                    nouv_chain = nouv_chain.replace(' ', '')  # retire les blancs
            patt_mod[i] = (OllPll[i][0], nouv_chain)  # nouveau dict avec rots simples
        return patt_mod # renvoie le dict avec les formules modifies
    RemplaceForms = classmethod(RemplaceForms)




# GESTION DE LA LECTURE DES ROTATIONS
def XpresStop():
    """ Cree un noeud Xpresso pour stopper l'animation """

    obj = doc.GetFirstObject()
    tag = c4d.BaseTag(c4d.Texpresso)  # tag de type Xpresso
    obj.InsertTag(tag)
    Gv_nodeM = tag.GetNodeMaster()  # renvoie le node Master
    T_node = Gv_nodeM.CreateNode(Gv_nodeM.GetRoot(), c4d.ID_OPERATOR_TIME, x=10, y=10)  # operateur Temps
    P_node = Gv_nodeM.CreateNode(Gv_nodeM.GetRoot(), 1022471, x=100, y=20)  # operateur Python
    li_P_Oports = P_node.GetOutPorts(type=-1)  # renvoie les ports de sortie
    P_node.RemovePort(li_P_Oports[0])
    li_P_Iports = P_node.GetInPorts(type=-1)  # renvoie les ports de sortie
    P_node.RemovePort(li_P_Iports[1])  # supprime Input2
    li_T_Oports = T_node.GetOutPorts(type=-1)  # recupere le port de sortie
    li_T_Oports[0].Connect(li_P_Iports[0])  # connecte les 2 ports
    P_node[c4d.GV_PYTHON_CODE] = 'import c4d\n\n' \
                                 + 'def main():\n' \
                                 + '    if Input1 >= doc.GetMaxTime().Get()/2: \n' \
                                 + '        c4d.documents.RunAnimation(doc,True)'  # code python




# INTERFACE UTLISATEUR
class MyDialog(gui.GeDialog):
    """ Fenetre de dialogue user"""

    def CreateLayout(self):
        """ creation des widgets users """
        self.SetTitle('PyRubik - Demo Plugin by Patrice Weisz')

        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 1, 2) #G1

        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 1, 2) # SG1
        self.GroupSpace(0, 30) # ecrat entre les boutons du groupe
        self.AddStaticText(TEXT1, c4d.BFH_CENTER, inith = 10, name='HOW TO PLAY : Push Generate Blend, Play Blend and Find Solution, Play Solution',borderstyle=c4d.BORDER_IN)
        self.AddMultiLineEditText(TXT_MELANGE, c4d.BFH_FIT, 300, 30,c4d.DR_MULTILINE_BOLD)
        self.SetMultiLineMode(TXT_MELANGE,c4d.SCRIPTMODE_NONE)
        self.SetString(TXT_MELANGE, MelangeCubes.etape.melange)
        self.GroupEnd()
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 2, 2) #SG2
        self.GroupSpace(150, 0) # ecrat entre les boutons du groupe
        self.AddButton(BTN_ALEA, c4d.BFH_LEFT, name='Generate Blend')
        # self.AddButton(BTN_INVERSE, c4d.BFH_LEFT, name='Inversion')
        self.AddButton(BTN_METHODE, c4d.BFH_RIGHT, name='Find Solution')
        self.GroupSpace(125, 0) # ecrat entre les boutons du groupe
        self.AddButton(BTN_PLAY, c4d.BFH_LEFT, name='Play Blend')
        self.AddButton(BTN_PLAY, c4d.BFH_RIGHT, name='Play Solution')
        self.GroupEnd()
        self.GroupEnd()
        self.AddSeparatorH(2, c4d.BFH_SCALEFIT)
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 2, 1)
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_LEFT, 2, 1)

        self.AddStaticText(TEXT2, c4d.BFH_LEFT, name='Number Of Rotations:')

        self.AddSlider(SLIDE_LONG, c4d.BFH_LEFT, initw=100, inith=0)

        self.SetInt32(SLIDE_LONG, MelangeCubes.etape.lit('longueur'), min=10, max=60, step=1, tristate=False, min2=10, max2=60)

        self.GroupEnd()
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_RIGHT, 2, 1)
        self.AddStaticText(TEXT3, c4d.BFH_RIGHT, name='Modify Speed :')
        self.AddSlider(SLIDE_VIT, c4d.BFH_RIGHT, initw=100, inith=0)
        self.SetInt32(SLIDE_VIT, MelangeCubes.etape.lit('vitesse'), min=1, max=15, step=1, tristate=False, min2=1, max2=15)
        self.GroupEnd()
        self.GroupEnd()
        self.AddSeparatorH(10, c4d.BFH_SCALEFIT)
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_CENTER, 2, 1)
        self.GroupSpace(176, 0) # ecrat entre les boutons du groupe
        self.AddButton(BTN_TEST, c4d.BFH_LEFT, name='Reset Cube')
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name='Cancel')
        self.GroupEnd()
        self.Activate(BTN_ALEA)
        return True

    def Command(self, id, msg):
        """ gestion des actions user """
        if id == BTN_CANCEL:  # bouton annuler
            self.Close()
        elif id == BTN_ALEA:  # bouton Aleatoire
            self.SetString(TXT_MELANGE, MelangeCubes.MelangeAleatoire())
        elif id == BTN_INVERSE:  # bouton Inversion
            self.melange = self.GetString(TXT_MELANGE)
            self.SetString(TXT_MELANGE, MelangeCubes.Inversion(self.melange))
        elif id == BTN_METHODE:  # Bouton Methode
            self.melange = self.GetString(TXT_MELANGE)
            self.SetString(TXT_MELANGE, Methode.Step2())
            self.SetString(TEXT1, 'Voici la solution :')
        elif id == BTN_TEST:  # Bouton Test
            self.melange = self.GetString(TXT_MELANGE)
            self.SetString(TXT_MELANGE, Test())
            self.SetString(TEXT1, 'Voici le resultat sur  :' + str(TIRAGE) + ' tirages')
        elif id == BTN_PLAY:  # bouton play
            VITESSE =self.GetInt32(SLIDE_VIT)
            self.melange = self.GetString(TXT_MELANGE)
            MelangeCubes.TourneRubik(self.melange,VITESSE)
            self.Close()
        elif id == SLIDE_VIT: # slider Vitesse de Rotation
            VITESSE =self.GetInt32(id)

        return True




# RIG DE ROTATION DU CUBE AVEC DES EFFECTEURS
class MelangeCubes():
    """ contient les methodes pour la rotation des faces """

    etape = None  # initialisee par le main

    def Inversion(cls, cha):
        """ inverse la chaine de melange """
        ROT = 'LlFfRrBbUuDdEeMmSs'  # rotations possibles
        rev = sol = ''
        for a in cha:
            rev = a + rev  # inverse la chaine
        for a in rev:
            pos = ROT.index(a)
            if pos % 2:  # impair si A on prend B, si B on prend A
                sol += ROT[pos - 1]
            else:
                sol += ROT[pos + 1]
        MelangeCubes.etape.ecrit('etat', 'inversion')  # stocke etat inversion
        return sol
    Inversion = classmethod(Inversion)


    def InitRubik(cls):
        """ raz des effecteurs"""
        par_eff_mel = doc.SearchObject("Rotations des Faces")
        if par_eff_mel != None:
            par_eff_mel.Remove()  # supprime les effecteur du melange et le neutre
        clo_obj = doc.GetFirstObject()
        li_eff_clo = c4d.InExcludeData()  # liste vide d'effecteurs
        clo_obj[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = li_eff_clo  # supprime la liste
        Cubes.PosiDebut()  # init du modele
        MelangeCubes.etape.ecrit('modele', Cubes.posi)  # stocke le modele
        c4d.CallCommand(12501, 12501)  # Aller au début
    InitRubik = classmethod(InitRubik)




# GENERATION D'UN MELANGE ALEATOIRE
    def MelangeAleatoire(cls):
        """ genere un melange aleatoire de ALEA rotations """
        rots = 'LlFfRrBbUuDd'
        melange = ''
        for i in range(ALEA):
            melange += rots[random.randint(0, 11)]  # nombre alea entre 0 et 11 compris
        MelangeCubes.etape.ecrit('melange', melange)  # stocke le melange
        return melange
    MelangeAleatoire = classmethod(MelangeAleatoire)




# GESTION DE LA CREATION DES EFFECTEURS DE ROTATION DES FACES
    def ListeEffecteurs(cls):
        """ met en memoire la liste des effecteurs de reference """
        dic_eff_rots = {}  # dict des effecteurs de reference
        par_eff_ref = doc.SearchObject("Effecteurs de Reference")
        li_eff_ref = par_eff_ref.GetChildren()  # recup des enfants
        li_eff_ref.reverse()  # inverse la liste
        rots = 'LlFfRrBbUuDdMmEeSs$'
        for r in rots:
            dic_eff_rots[r] = li_eff_ref[rots.index(r)]  # dict des effect.
        return dic_eff_rots
    ListeEffecteurs = classmethod(ListeEffecteurs)


    def TourneRubik(cls, cha, VITESSE):
        """ cree la liste des effecteurs du melange """


        def RotCubes(cha):
            """ rotation des faces du modele des cubes """
            Cubes.posi = MelangeCubes.etape.lit('modele')
            for r in cha:
                Cubes.Rotate(r)


        clo_obj = doc.GetFirstObject()
        bc = clo_obj.GetDataInstance()  # recupere le container de Mecanique
        print (VITESSE)
        pas = c4d.BaseTime(0.5/VITESSE)  # 6 F
        if MelangeCubes.etape.etat == 'debut':
            MelangeCubes.InitRubik()  # on remet au debut
            par_eff_mel = c4d.BaseObject(5140)  # neutre
            par_eff_mel.SetName("Rotations des Faces")
            doc.InsertObject(par_eff_mel, pred=clo_obj)
            li_eff_clo = c4d.InExcludeData()  # effecteurs du cloneur
            img_D = c4d.BaseTime(0)  # 0 F
            MelangeCubes.etape.ecrit('etat', 'inversion')  # stocke etat melange
            MelangeCubes.etape.ecrit('melange', cha)  # stocke le melange
        elif MelangeCubes.etape.etat == 'inversion':
            li_eff_clo = clo_obj[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]  # recupere les effecteurs
            par_eff_mel = doc.SearchObject("Rotations des Faces")
            img_D = doc.GetTime()  # prend le temps courant
            MelangeCubes.etape.ecrit('etat', 'debut')  # stocke etat solutionne
        img_F = img_D + pas
        for r in cha:  # cree et attribue les effecteurs
            eff_obj = MelangeCubes.ListeEffecteurs()[r].GetClone()
            img_D += pas
            img_F += pas
            eff_obj[c4d.MGINHERITANCEEFFECTOR_ANIMATEFROM] = img_D  # debut
            eff_obj[c4d.MGINHERITANCEEFFECTOR_ANIMATETO] = img_F  # fin
            li_eff_clo.InsertObject(eff_obj, 1)  # ajoute l'effecteur dans la liste
            doc.InsertObject(eff_obj, parent=par_eff_mel)  # insertion
        clo_obj[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = li_eff_clo
        doc.SetSelection(par_eff_mel, mode=c4d.SELECTION_NEW)
        img_end = img_F + pas
        doc.SetMaxTime(img_end * c4d.BaseTime(2))  # fixe la duree du projet a 2x
        doc.SetLoopMaxTime(img_end * c4d.BaseTime(2))
        RotCubes(cha)  # rotation du modele
        MelangeCubes.etape.ecrit('modele', Cubes.posi)
        c4d.CallCommand(12412)  # lecture avant
    TourneRubik = classmethod(TourneRubik)


class EffRot():
    """creation des 12 effecteurs de référence des faces """

    # section attributs de classe :
    dic_taille_boites = {'L': (150, 150, 50), 'l': (150, 150, 50),
                         'F': (50, 150, 150), 'f': (50, 150, 150),
                         'R': (150, 150, 50), 'r': (150, 150, 50),
                         'B': (50, 150, 150), 'b': (50, 150, 150),
                         'U': (150, 50, 150), 'u': (150, 50, 150),
                         'D': (150, 50, 150), 'd': (150, 50, 150),
                         'M': (150, 150, 50), 'm': (150, 150, 50),  # tranche M
                         'E': (150, 50, 150), 'e': (150, 50, 150),  # tranche E
                         'S': (50, 150, 150), 's': (50, 150, 150),  # tranche S
                         '$': (150, 150, 150)  # rotation complete du cube
                         }
    dic_decala_boites = {'L': (0, 0, -100), 'l': (0, 0, -100),
                         'F': (100, 0, 0), 'f': (100, 0, 0),
                         'R': (0, 0, 100), 'r': (0, 0, 100),
                         'B': (-100, 0, 0), 'b': (-100, 0, 0),
                         'U': (0, 100, 0), 'u': (0, 100, 0),
                         'D': (0, -100, 0), 'd': (0, -100, 0),
                         'M': (0, 0, 0), 'm': (0, 0, 0),  # tranche M
                         'E': (0, 0, 0), 'e': (0, 0, 0),  # tranche E
                         'S': (0, 0, 0), 's': (0, 0, 0),  # tranche S
                         '$': (0, 0, 0)
                         }

    def CreationEffecteurs(cls):
        """ Creation des 12 effecteurs de reference """

        par_eff_ref = c4d.BaseObject(5140)  # neutre parent des effecteurs
        par_eff_ref.SetName("Effecteurs de Reference")  # nom
        doc.InsertObject(par_eff_ref, pred=doc.GetFirstObject())  # insertion du groupe effecteur dans le doc
        rots = NeutresRotation.rots  # recupere la string de codage des rotations
        for r in rots:
            eff_obj = c4d.BaseObject(1018775)  # objet effecteur
            eff_obj.SetName("Rot Face " + str(r))  # nom
            champ_obj = c4d.modules.mograph.FieldObject(c4d.Fbox)  # creation du champ boite
            champ_obj[c4d.FIELD_BOX_SIZE] = c4d.Vector(*EffRot.dic_taille_boites[r])  # taille boite
            champ_obj[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(*EffRot.dic_decala_boites[r])  # position
            champ_obj[c4d.FIELD_INNER_OFFSET] = 1.0  # decalage interne
            champ_list = eff_obj[c4d.FIELDS]  # recupere la liste des champs vide de l'effecteur
            calque = c4d.modules.mograph.FieldLayer(c4d.FLfield)  # cree un calque de champ d'objet'
            calque.SetLinkedObject(champ_obj)  # lie le calque de champ au champ boite
            champ_list.InsertLayer(calque)  # insere le calque de champ dans la liste des champs
            eff_obj[c4d.FIELDS] = champ_list  # insere la liste des champs dans l'effecteur'
            eff_obj[c4d.MGINHERITANCEEFFECTOR_MODE] = 1  # mode animation
            eff_obj[c4d.MGINHERITANCEEFFECTOR_EASE] = 1  # mode sortie
            eff_obj[c4d.MGINHERITANCEEFFECTOR_ANIMATEFROM] = c4d.BaseTime(0)  # debut 0F
            eff_obj[c4d.MGINHERITANCEEFFECTOR_ANIMATETO] = c4d.BaseTime(0.5)  # fin 15F
            eff_obj[c4d.MGINHERITANCEEFFECTOR_OBJECT] = NeutresRotation.dic_neu_rots[r]
            doc.InsertObject(eff_obj, parent=par_eff_ref)  # insere l'effecteur'
            doc.InsertObject(champ_obj, parent=eff_obj)  # insere le champ en enfant de l'effecteur'
            doc.GetActiveBaseDraw()[c4d.BASEDRAW_DISPLAYFILTER_FIELD] = False  # retire de l'affichage les champs
    CreationEffecteurs = classmethod(CreationEffecteurs)  # declaration en methode de classe


class NeutresRotation():
    """ Creation des 12+7 neutres de rotation """

    # section des attributs de classe
    rots = 'LlFfRrBbUuDdMmEeSs$'
    dic_neu_cles = {'L': ('B', 90), 'l': ('B', -90), 'F': ('P', -90), 'f': ('P', 90),
                    'R': ('B', -90), 'r': ('B', 90), 'B': ('P', 90), 'b': ('P', -90),
                    'U': ('H', -90), 'u': ('H', 90), 'D': ('H', 90), 'd': ('H', -90),
                    'M': ('B', 90), 'm': ('B', -90), 'E': ('H', 90), 'e': ('H', -90),
                    'S': ('P', -90), 's': ('P', 90),
                    '$': ('B', 180)
                    }
    axe = {'H': c4d.VECTOR_X, 'P': c4d.VECTOR_Y, 'B': c4d.VECTOR_Z}  # axes
    dic_neu_rots = {}


    def CreationDesNeutres(cls):
        """ Creation des neutres avec images cles """

        par_obj = c4d.BaseObject(5140)  # creation d'un neutre
        par_obj.SetName("Axes de Rotation")
        doc.InsertObject(par_obj, pred=doc.GetFirstObject())
        for i in range(len(NeutresRotation.rots)):  # creation de chaque neutre
            neu_obj = c4d.BaseObject(5140)  # creation du neutre
            neu_obj.SetName("Rot_" + NeutresRotation.rots[i])
            pist = c4d.CTrack(neu_obj, c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_REL_ROTATION, \
                                                                c4d.DTYPE_VECTOR, 0), c4d.DescLevel(
                NeutresRotation.axe[NeutresRotation.dic_neu_cles[NeutresRotation.rots[i]][0]], \
                c4d.DTYPE_REAL, 0)))
            neu_obj.InsertTrackSorted(pist)  # associe la piste au neutre
            courbe_obj = pist.GetCurve()  # recupere la courbe associee
            cle_D = courbe_obj.AddKey(c4d.BaseTime(0))  # ajoute une cle a 0 F
            cle_D['key'].SetValue(courbe_obj, 0)  # rot = 0 degre
            cle_F = courbe_obj.AddKey(c4d.BaseTime(0.5))  # ajoute une cle a 15 F
            cle_F['key'].SetValue(courbe_obj, c4d.utils.DegToRad(
                NeutresRotation.dic_neu_cles[NeutresRotation.rots[i]][1]))  # rot = +- 90 degre
            doc.InsertObject(neu_obj, parent=par_obj)
            NeutresRotation.dic_neu_rots[NeutresRotation.rots[i]] = neu_obj
    CreationDesNeutres = classmethod(CreationDesNeutres)



#MODELISATION DU CUBE
class CreationRubik():
    """ creation des cubes composant le rubik """


    def CreationPetitsCubes(cls):
        """ creation cloneurs et clones """

        # creation du cloneur
        clo_obj = c4d.BaseObject(1018544)  # nouveau Cloneur
        clo_obj[c4d.ID_MG_MOTIONGENERATOR_MODE] = 3  # mode grille
        clo_obj[c4d.ID_MG_TRANSFORM_COLOR] = c4d.Vector(0, 0, 0)  # noir
        clo_obj[c4d.MG_GRID_RESOLUTION] = c4d.Vector(3, 3, 3)  # grille 3 x3
        doc.InsertObject(clo_obj)

        # creation des petits cubes
        cub_obj = c4d.BaseObject(c4d.Ocube)  # creation cube
        cub_obj[c4d.PRIM_CUBE_LEN] = c4d.Vector(100, 100, 100)
        cub_obj[c4d.PRIM_CUBE_DOFILLET] = True
        cub_obj[c4d.PRIM_CUBE_FRAD] = 10.0
        cub_obj[c4d.PRIM_CUBE_SUBF] = 5  # subdivision du biseau
        doc.InsertObject(cub_obj, clo_obj)  # enfant du cloneur

        # modifier les petits cubes
        doc.SetSelection(clo_obj, mode=c4d.SELECTION_NEW)
        c4d.CallCommand(12236)  # Rendre modifiable
        neu_obj = doc.GetFirstObject()  # neutre parent
        li_cub = neu_obj.GetChildren()  # recupere les enfants
        for c in li_cub:
            doc.SetSelection(c, mode=c4d.SELECTION_ADD)
        c4d.CallCommand(12236)  # Rendre modifiable

        # creation des materiaux de couleur
        coul_dic = {'orange': (255, 127, 0), 'blanc': (255, 255, 255),
                    'bleu': (0, 0, 255), 'vert': (0, 255, 0),
                    'jaune': (255, 255, 0), 'rouge': (255, 0, 0)}
        dic_mat = {}
        for c, values in coul_dic.items(): #***
            mat_obj = c4d.BaseMaterial(c4d.Mmaterial)  # materiau standard
            mat_obj.SetName(c)
            r, v, b = values
            mat_obj[c4d.MATERIAL_COLOR_COLOR] = \
                c4d.modules.colorchooser.Color8BitToFloat(r, v, b)  # conversion RVB
            doc.InsertMaterial(mat_obj)
            dic_mat[c] = mat_obj  # stocke les instances de materiaux

        # selection des polygones a colorier
        polycoul = {'vert': [5, [0, 1, 2, 3, 4, 5, 6, 7, 8]],
                    'bleu': [137, [18, 19, 20, 21, 22, 23, 24, 25, 26]],
                    'blanc': [264, [6, 7, 8, 15, 16, 17, 24, 25, 26]],
                    'orange': [203, [0, 3, 6, 9, 12, 15, 18, 21, 24]],
                    'jaune': [265, [0, 1, 2, 9, 10, 11, 18, 19, 20]],
                    'rouge': [71, [2, 5, 8, 11, 14, 17, 20, 23, 26]]
                    }
        # creation des tags de selection et de textures
        for co, cub in polycoul.items(): #***
            p, licub = cub
            for c in licub:
                tag = c4d.BaseTag(c4d.Tpolygonselection)
                tag.SetName('cube' + str(c) + '_p' + str(p))
                obj = li_cub[c]
                obj.InsertTag(tag)  # cree le tag de selection de polygones
                sele = tag.GetBaseSelect()
                sele.Select(p)  # enregistre la selection p
                tagtex = c4d.TextureTag()  # cree le tag de texture
                tagtex.SetMaterial(dic_mat[co])  # associe le materiau
                tagtex[c4d.TEXTURETAG_RESTRICTION] = tag.GetName()
                obj.InsertTag(tagtex)

        # creation du nouveau cloneur Mecanique
        clo_obj = c4d.BaseObject(1018544)  # nouveau Cloneur
        clo_obj[c4d.ID_MG_MOTIONGENERATOR_MODE] = 3  # mode grille
        clo_obj[c4d.ID_MG_TRANSFORM_COLOR] = c4d.Vector(0, 0, 0)  # noir
        clo_obj[c4d.MG_GRID_RESOLUTION] = c4d.Vector(3, 3, 3)  # grille 3 x3
        clo_obj.SetName("Mecanique")
        doc.InsertObject(clo_obj)
        li_cub.reverse()  # inverse les cubes
        for c in li_cub:
            doc.InsertObject(c.GetClone(), parent=clo_obj)
        neu_obj.Remove()  # supprimer et ses enfants
    CreationPetitsCubes = classmethod(CreationPetitsCubes)  # methode de classe



# GESTION DU MODELE DU CUBE EN MEMOIRE SUR LEQUEL SE FAIT LES RECHERCHES DE SOLUTION
class Cubes:
    """  definit la position des cubes du Rubik en memoire """

    noms = ['LBU', 'LU', 'LUF', 'LB', 'L', 'LF', 'LBD', 'LD', 'LFD',
            'BU', 'U', 'FU', 'B', '0', 'F', 'BD', 'D', 'FD',
            'RUB', 'RU', 'RFU', 'RB', 'R', 'RF', 'RBD', 'RD', 'RDF']
    orients_depart = ['U', 'U', 'U', 'L', 'L', 'L', 'D', 'D', 'D', 'U', 'U', 'U', 'B', '0', 'F', 'D', 'D', 'D',
                      'U', 'U', 'U', 'R', 'R', 'R', 'D', 'D', 'D']
    chang_ori = {'L': 'UFDBU', 'l': 'UBDFU', 'F': 'URDLU', 'f': 'ULDRU',
                 'R': 'UBDFU', 'r': 'UFDBU', 'B': 'ULDRU', 'b': 'URDLU',
                 'U': 'BRFLB', 'u': 'BLFRB', 'D': 'BLFRB', 'd': 'BRFLB',
                 'M': 'UFDBU', 'm': 'UBDFU', 'E': 'BLFRB', 'e': 'BRFLB',
                 'S': 'URDLU', 's': 'ULDRU'}
    centres = ['U', 'D', 'B', 'F']  # pour corriger l'orientation de ces centres
    posi = {}  # position des cubes


    def PosiDebut(cls):
        """ definit la position des cubes au depart """
        for i in range(27):  # creation des instances
            Cubes.posi[Cubes.noms[i]] = [Cubes.noms[i], [0, 0, 0], Cubes.orients_depart[i]]
        # Cubes.AffiCubes() # print
    PosiDebut = classmethod(PosiDebut)


    def Rotate(cls, r):
        """ applique la rotation r dans Cubes.posi """
        p = Cubes.posi  # pour simplifier la syntaxe
        n = [''] + Cubes.noms  # pour simplifier

        def Rot(face, sens, axe):
            """ fait la rotation des cubes d'une face et ajuste le spin """
            # p et n variables globales

            f = [0] + face  # ajuste l'indice
            if sens == +1:  # sens horaire
                p[n[f[1]]], p[n[f[7]]], p[n[f[9]]], p[n[f[3]]] = p[n[f[7]]], p[n[f[9]]], p[n[f[3]]], p[n[f[1]]]
                p[n[f[2]]], p[n[f[4]]], p[n[f[8]]], p[n[f[6]]] = p[n[f[4]]], p[n[f[8]]], p[n[f[6]]], p[n[f[2]]]

                for i in range(1, 10):  # les 9 cubes de la face
                    p[n[f[i]]][1][axe] += 1  # spine+1
                    # p[n[f[i]]][1][axe] %= 4 # modulo 4
            else:  # sens trigo
                p[n[f[1]]], p[n[f[3]]], p[n[f[9]]], p[n[f[7]]] = p[n[f[3]]], p[n[f[9]]], p[n[f[7]]], p[n[f[1]]]
                p[n[f[2]]], p[n[f[6]]], p[n[f[8]]], p[n[f[4]]] = p[n[f[6]]], p[n[f[8]]], p[n[f[4]]], p[n[f[2]]]

                for i in range(1, 10):  # les 9 cubes de la face
                    p[n[f[i]]][1][axe] -= 1  # spine-1
                    # p[n[f[i]]][1][axe] %= 4 # modulo 4

            chang = Cubes.chang_ori[r]  # chaine de permutation des orientations
            for i in range(1, 10):
                ind = chang.find(p[n[f[i]]][2])
                if ind != -1:  # si l'orientation est à changer
                    p[n[f[i]]][2] = chang[ind + 1]  # on permute circulairement les orientations

        def RotLeft():
            face = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # face L
            Rot(face, +1, 2)  # sens +1, axe Z

        def RotLeftInv():
            face = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # face l
            Rot(face, -1, 2)  # sens -1, axe Z

        def RotFront():
            face = [3, 12, 21, 6, 15, 24, 9, 18, 27]  # face F
            Rot(face, +1, 0)  # sens +1, axe X

        def RotFrontInv():
            face = [3, 12, 21, 6, 15, 24, 9, 18, 27]  # faces f
            Rot(face, -1, 0)  # sens -1, axe X

        def RotRight():
            face = [21, 20, 19, 24, 23, 22, 27, 26, 25]  # face R
            Rot(face, +1, 2)  # sens +1, axe Z

        def RotRightInv():
            face = [21, 20, 19, 24, 23, 22, 27, 26, 25]  # face r
            Rot(face, -1, 2)  # sens -1, axe Z

        def RotBack():
            face = [19, 10, 1, 22, 13, 4, 25, 16, 7]  # face B
            Rot(face, +1, 0)  # sens +1, axe X

        def RotBackInv():
            face = [19, 10, 1, 22, 13, 4, 25, 16, 7]  # face b
            Rot(face, -1, 0)  # sens -1, axe X

        def RotUp():
            face = [19, 20, 21, 10, 11, 12, 1, 2, 3]  # face U
            Rot(face, +1, 1)  # sens +1, axe Y

        def RotUpInv():
            face = [19, 20, 21, 10, 11, 12, 1, 2, 3]  # face u
            Rot(face, -1, 1)  # sens -1, axe Y

        def RotDown():
            face = [27, 26, 25, 18, 17, 16, 9, 8, 7]  # face D
            Rot(face, +1, 1)  # sens +1, axe Y

        def RotDownInv():
            face = [27, 26, 25, 18, 17, 16, 9, 8, 7]  # face d
            Rot(face, -1, 1)  # sens -1, axe Y

        def RotMiddle():
            face = [10, 11, 12, 13, 14, 15, 16, 17, 18]  # Middle M
            Rot(face, +1, 2)  # sens +1, axe Z
            Cubes.AffiCubes

        def RotMidInv():
            face = [10, 11, 12, 13, 14, 15, 16, 17, 18]  # Middle m
            Rot(face, -1, 2)  # sens -1, axe Z

        def RotEquat():
            face = [24, 23, 22, 15, 14, 13, 6, 5, 4]  # Middle E
            Rot(face, +1, 1)  # sens +1, axe Y

        def RotEquatInv():
            face = [24, 23, 22, 15, 14, 13, 6, 5, 4]  # Middle e
            Rot(face, -1, 1)  # sens -1, axe Y

        def RotStand():
            face = [2, 11, 20, 5, 14, 23, 8, 17, 26]  # Middle S
            Rot(face, +1, 0)  # sens +1, axe X

        def RotStandInv():
            face = [2, 11, 20, 5, 14, 23, 8, 17, 26]  # Middle s
            Rot(face, -1, 0)  # sens -1, axe X

        def RotRubik():
            """ rotation globale de 180° du cube Rubik (step4)
            on permute les emplacements, les noms des cubes
            et les orientations
            ex : LBU devient LDF """

            permut = {'LBU': 'LFD', 'LU': 'LD', 'LUF': 'LBD', 'LB': 'LF', 'L': 'L',
                      'BU': 'FD', 'U': 'D', 'FU': 'BD', 'B': 'F', '0': '0', 'F': 'B', 'D': 'U',
                      'RUB': 'RDF', 'RU': 'RD', 'RFU': 'RBD', 'RB': 'RF', 'R': 'R'}

            perm_noms = {'LBU': 'LFD', 'LFD': 'LBU', 'LU': 'LD', 'LD': 'LU',
                         'LUF': 'LBD', 'LBD': 'LUF', 'LB': 'LF', 'LF': 'LB', 'L': 'L',
                         'BU': 'FD', 'FD': 'BU', 'U': 'U', 'FU': 'BD', 'BD': 'FU',
                         'B': 'B', '0': '0', 'F': 'F', 'D': 'D',
                         'RUB': 'RDF', 'RDF': 'RUB', 'RU': 'RD', 'RD': 'RU',
                         'RFU': 'RBD', 'RBD': 'RFU', 'RB': 'RF', 'RF': 'RB', 'R': 'R'}

            perm_ori = {'U': 'D', 'D': 'U', 'L': 'L', 'R': 'R', 'F': 'B', 'B': 'F', '0': '0'}

            for n in permut:  # permute les cubes
                Cubes.posi[n], Cubes.posi[permut[n]] = Cubes.posi[permut[n]], Cubes.posi[n]
            for n in Cubes.posi:  # permutation des noms des cubes et les orientations
                Cubes.posi[n][0] = perm_noms[Cubes.posi[n][0]]
                Cubes.posi[n][2] = perm_ori[Cubes.posi[n][2]]

            for c in Cubes.centres:
                Cubes.posi[c][2] = c  # on corrige les centres

        rotations = {'L': RotLeft,
                     'l': RotLeftInv,
                     'F': RotFront,
                     'f': RotFrontInv,
                     'R': RotRight,
                     'r': RotRightInv,
                     'B': RotBack,
                     'b': RotBackInv,
                     'U': RotUp,
                     'u': RotUpInv,
                     'D': RotDown,
                     'd': RotDownInv,
                     'M': RotMiddle,
                     'm': RotMidInv,
                     'E': RotEquat,
                     'e': RotEquatInv,
                     'S': RotStand,
                     's': RotStandInv,
                     '$': RotRubik
                     }
        rotations[r]()  # execute la fonction de cle r
    Rotate = classmethod(Rotate)


    def AffiCubes(cls):
        """ affichage des positions des cubes """
        for n in Cubes.noms:
            print (n, Cubes.posi[n])
    AffiCubes = classmethod(AffiCubes)



# SAUVEGARDE DES DONNEES VOLATILES DANS UN BASIC CONTAINER
class Contenant():
    """ lit et ecrit dans un container """

    def Ident(cls, mot):
        """ convertit un mot en identifiant unique """
        # print int(''.join(str(ord(c)) for c in mot[:3]))
        return int(''.join(str(ord(c)) for c in mot[:3]))  # renvoie le int ID
    Ident = classmethod(Ident)


    def __init__(self):
        """ cree l'instance Contenant """
        self.clo_obj = doc.GetFirstObject()
        self.bc = self.clo_obj.GetData()  # recupere le container de Mecanique
        self.ID = Contenant.Ident("rubik")  # identifiant du sub container
        self.sub_bc = self.bc[self.ID]
        if self.sub_bc == None:  # le sub-container n'existe pas
            self.sub_bc = c4d.BaseContainer()  # creation d'un container vide
            self.bc[self.ID] = self.sub_bc  # insert le sub container
            self.sub_bc = self.bc[self.ID]  # recupere le sub container
            self.sub_bc[Contenant.Ident('etat')] = "debut"  # init le champ  'etat''
            self.sub_bc[Contenant.Ident('melange')] = TEST  # init le champ  'melange'
            self.sub_bc[Contenant.Ident('vitesse')] = str(VITESSE) # init Vitesse
            self.sub_bc[Contenant.Ident('longueur')] = str(ALEA) # init Nobre de rotations
            self.sub_bc[Contenant.Ident('modele')] = str(Cubes.posi) # str(pickle.dumps(Cubes.posi), encoding="utf-8")  # init position modele
            self.bc[self.ID] = self.sub_bc  # insert le sub container
            self.clo_obj.SetData(self.bc)  # met a jour le base container
        self.etat = self.sub_bc[Contenant.Ident('etat')]
        self.melange = self.sub_bc[Contenant.Ident('melange')]
        self.modele = eval(self.sub_bc[Contenant.Ident('modele')]) # python 3
        self.vitesse = eval(self.sub_bc[Contenant.Ident('vitesse')]) # python 3
        self.longueur = eval(self.sub_bc[Contenant.Ident('longueur')]) # python 3


    def lit(self, nom):
        """ lit la data dans le subcontainer """
        if nom == 'etat':
            self.etat = self.sub_bc[Contenant.Ident('etat')]
            return self.etat
        elif nom == 'melange':
            self.melange = self.sub_bc[Contenant.Ident('melange')]
            return self.melange
        elif nom == 'modele':
            self.modele = eval(self.sub_bc[Contenant.Ident('modele')]) #python 3
            return self.modele
        elif nom == 'vitesse':
            VITESSE = eval(self.sub_bc[Contenant.Ident('vitesse')])
            return self.vitesse
        elif nom == 'longueur':
            ALEA = eval(self.sub_bc[Contenant.Ident('longueur')])
            return self.longueur



    def ecrit(self, nom, data):
        """ stocke la data dans le subcontainer """
        self.clo_obj = doc.GetFirstObject()
        self.bc = self.clo_obj.GetData()  # recupere le container de Mecanique
        self.ID = Contenant.Ident("rubik")  # identifiant du sub container
        self.sub_bc = self.bc[self.ID]
        if nom == 'etat':
            self.sub_bc.SetString(Contenant.Ident('etat'), data)  # sauve la data etat
            self.etat = data
        elif nom == 'melange':
            self.sub_bc.SetString(Contenant.Ident('melange'), data)  # sauve la chaine de melange
            self.melange = data
        elif nom == 'modele':
            self.sub_bc.SetString(Contenant.Ident('modele'), str(data)) #dumps(data))  # python 3
        elif nom == 'vitesse':
            self.sub_bc.SetString(Contenant.Ident('vitesse'), str(data)) #.dumps(data))  # python 3
        elif nom == 'longueur':
            self.sub_bc.SetString(Contenant.Ident('longueur'), str(data)) #.dumps(data))  # python 3

        self.bc[self.ID] = self.sub_bc  # insert le sub container
        self.clo_obj.SetData(self.bc)  # met a jour le base container



# INITIALISATION ET CREATION DU RUBIK ET DE L'INTERFACE UTILISATEUR
def main():

    if doc.GetDocumentName()== "PyRubik":

        if doc.GetFirstObject() == None:  # doc vide
            doc.Flush()  # vide le document y compris les materiaux si necessaire
            CreationRubik.CreationPetitsCubes()  # creation des petits cubes
            NeutresRotation.CreationDesNeutres()  # creation des axes de rotation
            EffRot.CreationEffecteurs()  # creation des effecteurs de reference
            XpresStop()  # creation du noeud Xpresso stop
            Cubes.PosiDebut()  # init du modele
        MelangeCubes.etape = Contenant()  # cree une reference globale de l'instance
        c4d.EventAdd()
        dlg = MyDialog()
        dlg.Open(c4d.DLG_TYPE_MODAL, xpos=-1, ypos=-1, defaultw=400, defaulth=100)

    else:
        projet = c4d.documents.GetFirstDocument()
        if "PyRubik"  is not projet.GetDocumentName(): # creation d'un nouveau document
            projet = c4d.documents.BaseDocument()# nouveau document de projet
            projet.SetDocumentName("PyRubik")
            c4d.documents.InsertBaseDocument(projet)
            c4d.documents.SetActiveDocument(projet)# PyRubik devient le doc actif
        else:
            projet = li_docs[li_noms.index("PyRubik")] #on recupere le doc "PyRubik"
            c4d.documents.SetActiveDocument(projet) # au cas ou il ne serait pas actif

if __name__ == '__main__':
    main()