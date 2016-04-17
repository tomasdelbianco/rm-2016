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

import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    # Variables
    _inherit = "res.partner"

    # Metodos de campos

    # Campos
    es_empresa_tup = fields.Boolean('Es Empresa de Transporte?')

    _sql_constraints = [
        
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

res_partner()

class tup_recorrido(models.Model):
    # Variables
    _name = "tup.recorrido"

    # Metodos de campos

    # Campos
    name = fields.Char('Nombre', size=128, required=True)
    colectivo_id = fields.Many2one('tup.colectivo', 'Colectivo', required=True, ondelete='cascade')
    fecha = fields.Date('Fecha', required=True, default=fields.datetime.now())
    polyline_ida_id = fields.Many2one('map.polyline', 'Puntos del recorrido de ida')
    polyline_vuelta_id = fields.Many2one('map.polyline', 'Puntos del recorrido de vuelta')
    kml_ida = fields.Binary('KML Ida')
    kml_vuelta = fields.Binary('KML Vuelta')
    recorrido = fields.Text('Recorrido')

    _sql_constraints = [
        
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

tup_recorrido()

class tup_colectivo(models.Model):
    # Variables
    _name = "tup.colectivo"

    # Metodos de campos

    # Campos
    name = fields.Char('Nombre', size=128, required=True)
    foto = fields.Binary('Foto')
    descripcion = fields.Text('Descripción')
    empresa_tup_id = fields.Many2one('res.partner', 'Empresa', domain=[('es_empresa_tup','=',True)])
    recorrido_id = fields.Many2one('tup.recorrido', 'Recorrido activo')
    recorrido_ids = fields.One2many('tup.recorrido', 'colectivo_id', 'Recorridos')
    active = fields.Boolean('Activo', default=True)
        

    _sql_constraints = [
        ('name_uniq','unique(name)', 'El colectivo ya existe'),
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

tup_colectivo()