import cgi


class Formulario(object):
    """Obtiene los campos del formulario"""
    
    def __init__(self, depurar=False):
        self.form = cgi.FieldStorage()
        if depurar:
            import cgitb
            cgitb.enable()
     
        
class FormLiga(Formulario):
    
    def obtener(self):
        if self.form.has_key('u'):
            return self.form['u'].value
        else:
            return None


class FormVarios(Formulario):
    
    def obtener(self): 
        if self.form.has_key('u'):
            return self.form.getlist('u')
        else:
            return None


class FormSolo(FormLiga):
    
    pass