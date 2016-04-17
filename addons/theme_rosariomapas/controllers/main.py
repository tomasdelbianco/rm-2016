# -*- coding: utf-8 -*-
import werkzeug

from openerp import SUPERUSER_ID
from openerp import http
from openerp import tools
from openerp.http import request
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect

class website_rosariomapas(http.Controller):

    @http.route(['/','/page/homepage'], type='http', auth="public", website=True)
    def index(self, **kw):
        Colectivos = http.request.env['tup.colectivo']
        
        return http.request.render('website.homepage', {
            'colectivos': Colectivos.search([('recorrido_id','!=',False), ('recorrido_id.polyline_ida_id', '!=', False), ('recorrido_id.polyline_vuelta_id', '!=', False)], order="name")
        })

    @http.route(['/rm/get_recorrido'], type='json', auth="public", methods=['POST'], website=True)
    def get_recorrido(self, colectivo_id, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        colectivo = pool['tup.colectivo'].browse(cr, 1, colectivo_id, context=context)
        recorrido_ida = []
        recorrido_vuelta = []
        for punto in colectivo.recorrido_id.polyline_ida_id.latlng_ids:
            recorrido_ida.append({'lat':punto.latitude, 'lng': punto.longitude})
        for punto2 in colectivo.recorrido_id.polyline_vuelta_id.latlng_ids:
            recorrido_vuelta.append({'lat':punto2.latitude, 'lng': punto2.longitude})
        return {'recorrido_ida':recorrido_ida, 'recorrido_vuelta':recorrido_vuelta}