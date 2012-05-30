from mzc.parser import ManagerParser
from mzc.equipo import Equipo


class Conjunto(object):
    """Clase para manejar comparaciones entre varios equipos"""

    def __init__(self, usernames):
        self.usernames = usernames
        self.usersDict = {}
        for u in reversed(self.usernames):
            lm = ManagerParser(u, usingTeamID=u.isdigit())
            self.userDataDict, self.teamDict = lm.read_manager_data()
            self.usersDict[u] = self.userDataDict
    
    def obtener_detalles(self):
        self.listaEquipos = []
        for u in self.usernames:
            e = Equipo(u, usandoTeamId=u.isdigit())
            # Adds missing fields
            e.teamDict['username'] = self.usersDict[u]['username']
            e.teamDict['teamCurrency'] = e.moneda
            e.teamDict['countryShortname'] = self.usersDict[u]\
                                                 ['countryShortname'].lower()
            self.listaEquipos.append(e)
    
    def convertir_moneda(self):
        for e in self.listaEquipos[1:]:
            if e.moneda != self.listaEquipos[0].moneda:
                e.convertir_moneda(self.listaEquipos[0].moneda)