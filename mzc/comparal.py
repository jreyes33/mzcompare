from mzc.liga import Liga


class ComparaLiga(object):
    """Clase que controla y hace uso del resto de objetos en MZ Compare"""
    
    def __init__(self, username):
        self.username = username
        self.l = Liga(self.username)
        self.l.obtener_detalles()
        for e in self.l.listaEquipos:
            e.hacer_enteros(['age', 'birthDay', 'birthSeason', 'salary',
                             'value'])
            e.obtener_datos_11()
            e.separar_juves()
            e.contar_jugs()
            e.sacar_suma_prom('age', incluirJuves=True)
            e.sacar_suma_prom('value', incluirJuves=True)
            e.sacar_suma_prom('salary', incluirJuves=False)
      
    def getStandings(self):
        return self.l.tablaPos
        
    def getTeams(self):
        self.teams = []
        for e in self.l.listaEquipos:
            e.teamDict = dict(e.teamDict.items() + e.userDataDict.items())
            e.teamDict['players'] = []
            e.teamDict['players'].extend(e.listaMayores)
            e.teamDict['players'].extend(e.listaJuves)
            self.teams.append(e.teamDict)
            if e.teamDict['teamId'] == self.l.teamDict['teamId']:
                e.teamDict['highlight'] = True
        
        return self.teams, self.l.teamDict['teamId']