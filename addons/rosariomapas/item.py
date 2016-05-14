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

class item_tag(models.Model):
    # Variables
    _name = "item.tag"

    # Metodos de campos

    # Campos
    name = fields.Char('Nombre', size=128, required=True)
        

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Tag ya existente'),
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

item_tag()

class item_categoria(models.Model):
    # Variables
    _name = "item.categoria"

    # Metodos de campos

    # Campos
    name = fields.Char('Nombre', size=128, required=True)
    parent_id = fields.Many2one('item.categoria', 'Categoría Padre')
    descripcion = fields.Text('Descripcion')
    keyword_ids = fields.Many2many('item.tag', string='Keywords', help="Palabras Clave")
    keywords = fields.Text('Keywords')
    url = fields.Char('URL', size=64)
    id_externo = fields.Integer('ID Anterior', size=8)
    parent_id_externo = fields.Integer('ID Parent Anterior', size=8)
    item_ids = fields.One2many('item.item', 'categoria_id', 'Items')
    subcategoria_ids = fields.One2many('item.categoria', 'parent_id', 'Subcategorías')
        
    active = fields.Boolean('Activo', default=True)


    _sql_constraints = [
        ('url_uniq', 'unique(url)', 'La URL ya existe!'),
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales
    @api.multi
    def acomodar_parents(self):
        for subcat in self.search([('parent_id_externo', '!=', False)]):
            subcat.parent_id = self.search([('parent_id_externo','=',False), ('id_externo','=',subcat.parent_id_externo)])[0]

    # @api.multi
    # def acomodar_keywords(self):
    #     for cat in self.search([('keywords','!=',[])])

item_categoria()

class item_foto(models.Model):
    # Variables
    _name = "item.foto"

    # Metodos de campos

    # Campos
    
    foto = fields.Binary('Foto', required=True)
    name = fields.Char('Nombre', size=45)
    descripcion = fields.Text('Descripción')
    item_id = fields.Many2one('item.item', 'Item')
    latlng_id = fields.Many2one('map.latlng', 'Posición')

    _sql_constraints = [
        
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales

item_foto()

class item_item(models.Model):
    # Variables
    _name = "item.item"

    # Metodos de campos

    # Campos
    
    name = fields.Char('Nombre', size=256, required=True)
    direccion = fields.Char('Dirección', size=256, required=True)
    telefono = fields.Char('Telefono', size=128)
    latlng_id = fields.Many2one('map.latlng', 'Posicion', help="Latitud y Longitud")
    foto_ids = fields.One2many('item.foto', 'item_id', 'Fotos')
    web_url = fields.Char('Dirección web', size=256)
    keyword_ids = fields.Many2many('item.tag', string="Palabras Clave")
    keywords = fields.Text('Palabras Clave')
    id_externo = fields.Integer('ID Anterior', size=8)
    categoria_id_anterior = fields.Integer('Categoria ID Anterior', size=8)
    categoria_id = fields.Many2one('item.categoria', 'Categoría')
    descripcion = fields.Text('Descripción')
    url = fields.Char('URL', size=64)
    plan = fields.Selection([('gratis','Gratis'), ('pago_1', 'Pago 1')], 'Plan', default="gratis")
    visitas = fields.Integer('Visitas', size=8)
    active = fields.Boolean('Activo', default=True)
    publicado = fields.Boolean('Publicado')
    latitud = fields.Char('Latitud', size=45)
    longitud = fields.Char('Longitud', size=45)
        
        

    _sql_constraints = [
        ('url_uniq', 'unique(url)', 'La URL ya existe!'),
    ]

    # Constraints

    # Metodos on_change

    # Metodos heredados del orm

    # Metodos generales
    @api.multi
    def btn_acomodar_categorias(self):
        for item in self.search([('categoria_id','=',False)]):
            item.categoria_id = self.env['item.categoria'].search([('parent_id','!=',False),('id_externo', '=', item.categoria_id_anterior)]) and self.env['item.categoria'].search([('parent_id','!=',False),('id_externo', '=', item.categoria_id_anterior)])[0] or False
            item.latlng_id = self.env['map.latlng'].create({'latitude':item.latitud,'longitude':item.longitud})

item_item()