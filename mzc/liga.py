from mzc.parser import SeriresParser, ManagerParser
from mzc.equipo import Equipo


class Liga(object):
    """Liga oficial de MZ"""

    def __init__(self, usuario):
        lm = ManagerParser(usuario, usingTeamID=usuario.isdigit())
        self.userDataDict, self.teamDict = lm.read_manager_data()
        ll = SeriresParser(self.teamDict['seriesId'])
        self.tablaPos = ll.read_series_data()
        
    def hacer_enteros(self, datos):
        for equipo in self.tablaPos:
            for i in datos:
                equipo[i] = int(equipo[i])
    
    def ordenar(self, dato, voltear=True):
        self.tablaPos.sort(key = lambda k: k[dato], reverse = voltear)
        
    def obtener_detalles(self):
        self.listaEquipos = []
        for i in self.tablaPos:
            e = Equipo(i['teamId'], usandoTeamId=True)
            e.teamDict['teamCurrency'] = e.moneda
            self.listaEquipos.append(e)