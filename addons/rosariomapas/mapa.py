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

class MapLatLng(models.Model):
    # Variables
    _name = "map.latlng"

    # Metodos de campos

    # Campos
    latitude = fields.Float('Latitud', size=15, digits=(4,12), required=True)
    longitude = fields.Float('Longitud', size=15, digits=(4,12), required=True)
    
    polyline_id = fields.Many2one('map.polyline', 'Polyline', ondelete="cascade")
    

    _sql_constraints = [
        
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

MapLatLng()

class MapPolyline(models.Model):
    # Variables
    _name = "map.polyline"

    # Metodos de campos

    # Campos
    latlng_ids = fields.One2many('map.latlng', 'polyline_id', 'Puntos')
    
    

    _sql_constraints = [
        
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

MapPolyline()