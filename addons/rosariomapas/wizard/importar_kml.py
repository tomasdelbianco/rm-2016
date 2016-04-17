# -*- coding: 850 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from openerp.addons import funciones
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning, ValidationError
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round as round
from openerp.tools.safe_eval import safe_eval as eval
from pykml import parser

import logging
_logger = logging.getLogger(__name__)

import base64
import zipfile
import shutil
import io

class WizardImportarKml(models.TransientModel):
    # Variables
    _name = "wizard.importar.kml"
    _description = 'Importar Recorridos KML'
    # Metodos de campos

    # Campos
    archivo_kml_zip = fields.Binary('Recorridos KML comprimidos en ZIP')
    
    @api.multi
    def procesar_kml(self):
        tup_colectivo = self.env['tup.colectivo']
        tup_recorrido = self.env['tup.recorrido']
        for obj in self:
            archivo = base64.b64decode(obj.archivo_kml_zip)
            if archivo:
                file_like_object = io.BytesIO(archivo)
                zf = zipfile.ZipFile(file_like_object, 'a')                
                for filename in zf.namelist():
                    data = zf.read(filename)
                    try:
                        k = parser.fromstring(data)
                        recorrido = str(k.Document.Placemark.name)
                        if recorrido:
                            linea = recorrido.replace(" Ida", "").replace(" Vuelta", "")
                            if linea:
                                kml_data = base64.b64encode(data)

                                tup_col_id = tup_colectivo.search([('name','=', linea)])
                                if not tup_col_id:
                                    tup_col_id = tup_colectivo.create({'name':linea})

                                tup_rec_id = tup_recorrido.search([('name','=', linea)])
                                if not tup_rec_id:
                                    tup_rec_id = tup_recorrido.create({'name':linea, 'colectivo_id':tup_col_id.id})

                                tup_col_id.write({'recorrido_id':tup_rec_id.id})

                                if "Ida" in recorrido:
                                    tup_rec_id.write({'kml_ida':kml_data})
                                elif "Vuelta" in recorrido:
                                    tup_rec_id.write({'kml_vuelta':kml_data})
                    except Exception, e:
                        print e
                        print "No se pudo importar: ",filename
                        pass
                tup_colectivo.search([]).procesar_kml()



    _sql_constraints = [
        
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

WizardImportarKml()