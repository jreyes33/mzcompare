from mzc.parser import ManagerParser, PlayersParser
from mzc.currency import Currency
from string import upper #@UnusedImport


class Equipo(object):
    """Equipo de MZ"""

    def __init__(self, usuario, usingTeamID=False):
        lm = ManagerParser(usuario, usingTeamID)
        self.userDataDict, self.teamDict = lm.read_manager_data()
        lj = PlayersParser(self.teamDict['teamId'])
        self.listaMayores = lj.read_players_data()
        self.moneda = lj.read_currency()
        if not self.moneda:
            self.moneda = "USD"
        # corrige error de ligas con bots
        if not self.userDataDict.has_key('countryShortname'):
            self.userDataDict[u'countryShortname']= lj.read_country().upper()
            self.teamDict[u'teamName'] = lj.read_team_name()
        self.listaJuves = []

    def hacer_enteros(self, datos):
        for jugador in self.listaMayores:
            for i in datos:
                jugador[i] = int(jugador[i])
        for jugador in self.listaJuves:
            for i in datos:
                jugador[i] = int(jugador[i])

    def separar_juves(self):
        i = 0
        while i < len(self.listaMayores):
            if self.listaMayores[i]['junior'] == '0':
                i += 1
            else:
                self.listaJuves.append(self.listaMayores.pop(i))

    def sacar_suma_prom(self, dato, incluirJuves=True):
        # Mayores
        self.teamDict['sumM_' + dato] = 0
        for i in self.listaMayores:
            self.teamDict['sumM_' + dato] += int(i[dato])
        if len(self.listaMayores) != 0:
            self.teamDict['avgM_' + dato] = self.teamDict['sumM_' + dato] /\
                                       float(len(self.listaMayores))
        else:
            self.teamDict['avgM_' + dato] = 0.0

        #Juveniles
        if incluirJuves:
            self.teamDict['sumJ_' + dato] = 0
            for i in self.listaJuves:
                self.teamDict['sumJ_' + dato] += int(i[dato])
            if len(self.listaJuves) != 0:
                self.teamDict['avgJ_' + dato] = self.teamDict['sumJ_' + dato] /\
                                               float(len(self.listaJuves))
            else:
                self.teamDict['avgJ_' + dato] = 0.0

            #Totales
            self.teamDict['sumT_' + dato] = self.teamDict['sumM_' + dato] +\
                                           self.teamDict['sumJ_' + dato]
            if len(self.listaMayores) + len(self.listaJuves) != 0:
                self.teamDict['avgT_' + dato] = self.teamDict['sumT_' + dato] /\
                       float(len(self.listaJuves) + len(self.listaMayores))
            else:
                self.teamDict['avgT_' + dato] = 0.0

    def contar_jugs(self):
        self.teamDict['nMay'] = len(self.listaMayores)
        self.teamDict['nJuv'] = len(self.listaJuves)
        self.teamDict['nJug'] = self.teamDict['nMay'] + self.teamDict['nJuv']
        self.teamDict['nExt'] = len([1 for d in self.listaMayores if
                                 d['countryShortname'] !=
                                 self.userDataDict['countryShortname'].lower()])

    def ordenar(self, dato, voltear=True):
        self.listaMayores.sort(key = lambda k: k[dato], reverse = voltear)
        self.listaJuves.sort(key = lambda k: k[dato], reverse = voltear)

    def obtener_max(self, dato, incluirJuves=True):
        self.ordenar(dato, voltear=True)
        if self.listaJuves and incluirJuves and \
           self.listaJuves[0][dato] > self.listaMayores[0][dato]:
            self.teamDict['max_' + dato] = [self.listaJuves[0]['name'],
                                           self.listaJuves[0][dato]]
        elif self.listaMayores:
            self.teamDict['max_' + dato] = [self.listaMayores[0]['name'],
                                           self.listaMayores[0][dato]]
        else:
            self.teamDict['max_' + dato] = ["-", 0]

    def obtener_min(self, dato, incluirJuves=True):
        self.ordenar(dato, voltear=False)
        if self.listaJuves and incluirJuves and \
           self.listaJuves[0][dato] < self.listaMayores[0][dato]:
            self.teamDict['min_' + dato] = [self.listaJuves[0]['name'],
                                           self.listaJuves[0][dato]]
        elif self.listaMayores:
            self.teamDict['min_' + dato] = [self.listaMayores[0]['name'],
                                           self.listaMayores[0][dato]]
        else:
            self.teamDict['min_' + dato] = ["-", 0]

    def obtener_datos_11(self):
        # Ejecutar antes de separar los juveniles
        self.teamDict['sum11_value'] = 0
        self.teamDict['sum11_salary'] = 0
        self.teamDict['sum11_age'] = 0
        self.ordenar('value', voltear=True)
        for i in self.listaMayores[:11]:
            self.teamDict['sum11_value'] += int(i['value'])
            self.teamDict['sum11_salary'] += int(i['salary'])
            self.teamDict['sum11_age'] += int(i['age'])
        long = float(len(self.listaMayores[:11]))
        if long != 0:
            self.teamDict['avg11_value'] = self.teamDict['sum11_value'] / long
            self.teamDict['avg11_salary'] = self.teamDict['sum11_salary'] / long
            self.teamDict['avg11_age'] = self.teamDict['sum11_age'] / long
        else:
            self.teamDict['avg11_value'] = 0
            self.teamDict['avg11_salary'] = 0
            self.teamDict['avg11_age'] = 0

    def convertir_moneda(self, hacia):
        # Ejecutar antes de separar los juveniles
        if hacia != self.moneda:
            m = Currency(self.moneda)
            for j in self.listaMayores:
                j['salary'] = m.convert_to(hacia, j['salary'])
                j['value'] = m.convert_to(hacia, j['value'])
        self.moneda = hacia

