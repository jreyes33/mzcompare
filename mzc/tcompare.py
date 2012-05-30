#import sys as sysEncode
from mzc.conjunto import Conjunto

class TeamCompare(object):    
    """Clase que hace uso del resto de modulos y compara varios equipos"""

    def __init__(self, usernames):
        # En lugar de poner encode a todos los print, se usa este truco sucio
#        if not hasattr(sysEncode, 'setdefaultencoding'):
#            reload(sysEncode)
#            sysEncode.setdefaultencoding('utf-8')
        self.usernames = usernames
        self.c = Conjunto(self.usernames)
        self.c.obtener_detalles()
        self.c.convertir_moneda()
        for e in self.c.listaEquipos:
            e.hacer_enteros(['age', 'birthDay', 'birthSeason', 'salary',
                             'value'])
            e.obtener_datos_11()
            e.separar_juves()
            e.contar_jugs()
            e.sacar_suma_prom('age', True)
            e.sacar_suma_prom('value', True)
            e.sacar_suma_prom('salary', False)
            if len(self.usernames) == 2:
                e.obtener_max('age', True)
                e.obtener_max('salary', True)
                e.obtener_max('value', True)
        
    def get_teams(self):
        self.teams = []
        for e in self.c.listaEquipos:
            e.teamDict['players'] = []
            e.teamDict['players'].extend(e.listaMayores)
            e.teamDict['players'].extend(e.listaJuves)
            self.teams.append(e.teamDict)
            if e.teamDict['teamId'] == self.c.teamDict['teamId']:
                e.teamDict['highlight'] = True
        
        return self.teams, self.c.listaEquipos[0].teamDict['teamId']