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

    @http.route(['/rm/search_colectivo'], type='json', auth="public", methods=['POST'], website=True)
    def search_colectivo(self, orig_lat, orig_lng, dest_lat, dest_lng, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        query = """
            SELECT distinct map_latlng.polyline_id
            from map_latlng
            where
            SQRT(POW((69.1 * (latitude - %f)) , 2 ) + 
            POW((53 * (longitude - %f)), 2)) < 0.3 
            and map_latlng.polyline_id in (SELECT distinct map_latlng.polyline_id
            from map_latlng
            where
            SQRT(POW((69.1 * (latitude - %f)) , 2 ) + 
            POW((53 * (longitude - %f)), 2)) < 0.3)
        """ % (orig_lat, orig_lng, dest_lat, dest_lng)

        cr.execute(query)
        rta = cr.fetchall()
        coles = []
        for res in rta:
            cole = http.request.env['tup.colectivo'].search(['|', ('recorrido_id.polyline_vuelta_id', '=', res[0]), ('recorrido_id.polyline_ida_id', '=', res[0])])
            if cole not in coles:
                coles.append(cole)
        return {"resultado":[c.id for c in coles]}