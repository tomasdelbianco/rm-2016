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
        Categorias = http.request.env['item.categoria']

        return http.request.render('website.homepage', {
            'colectivos': Colectivos.search([('recorrido_id','!=',False), ('recorrido_id.polyline_ida_id', '!=', False), ('recorrido_id.polyline_vuelta_id', '!=', False)], order="name"),
            'categorias': Categorias.search([('parent_id','=',False)])
        })

    @http.route(['/<int:item_id>/<string:web_url>.htm'], type='http', auth="public", website=True)
    def item_old(self, item_id=False, web_url=False, **post):
        Categorias = http.request.env['item.categoria']
        Items = http.request.env['item.item']
        item = Items.search([('id_externo','=',item_id)])
        if item:
            return werkzeug.utils.redirect("/%s-%s"%(item.id, item.url.split("/")[1]), 301)
    
    @http.route(['/<int:item_id>-<string:web_url>'], type="http", auth="public", website=True)
    def item(self, item_id=False, web_url=False, **post):
        Categorias = http.request.env['item.categoria']
        Items = http.request.env['item.item']
        item = Items.browse(item_id)
        return http.request.render("website.item", {
            'item_id': item,
            'categorias': Categorias.search([('parent_id','=',False)]),
        })
    @http.route(['/recorrido/<string:web_url>'], type='http', auth="public", website=True)
    def recorrido(self, web_url=False, **post):
        Colectivos = http.request.env['tup.colectivo']
        Categorias = http.request.env['item.categoria']
        colectivo_id = Colectivos.search([('url', '=', web_url)])
        return http.request.render("website.recorrido_colectivo", {
            'colectivos': Colectivos.search([('recorrido_id','!=',False), ('recorrido_id.polyline_ida_id', '!=', False), ('recorrido_id.polyline_vuelta_id', '!=', False)], order="name"),
            'categorias': Categorias.search([('parent_id','=',False)]),
            'colectivo_id': colectivo_id,
        })

    @http.route(['/rm/search_items'], type='json', auth="public", methods=['POST'], website=True)
    def search_items(self, categorias, texto=False, **kw):
        Items = http.request.env['item.item']
        resultado = []
        if categorias and type(categorias) is list:
            for item in Items.search([('categoria_id','in',categorias)]):
                resultado.append({
                    'id':item.id,
                    'category': 'bar_restaurant',
                    'title':item.name,
                    'location':item.direccion,
                    'latitude':item.latitud,
                    'longitude':item.longitud,
                    'url':item.url,
                    'type': item.categoria_id.name,
                    "type_icon": item.categoria_id.icon_id.path or "/theme_rosariomapas/static/icons/store/apparel/umbrella-2.png",
                    "rating": 4,
                    "gallery": [],
                    "features":[],
                    "date_created": "2014-11-03",
                    # "price": "$2500",
                    "featured": 0,
                    "color": "",
                    "person_id": 1,
                    "year": 1980,
                    "special_offer": 0,
                    "item_specific":{},
                    "description": item.descripcion,
                    # "last_review": "Curabitur odio nibh, luctus non pulvinar a, ultricies ac diam. Donec neque massa, viverra interdum eros ut, imperdiet",
                    # "last_review_rating": 5
                })
        return {'data':resultado}

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
        return {'recorrido_ida':recorrido_ida, 'recorrido_vuelta':recorrido_vuelta, 'url': colectivo.url}

    @http.route(['/rm/search_colectivo'], type='json', auth="public", methods=['POST'], website=True)
    def search_colectivo(self, orig_lat, orig_lng, dest_lat, dest_lng, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        query = """
            SELECT distinct map_latlng.polyline_id
            FROM map_latlng
            WHERE
            SQRT(POW((69.1 * (latitude - %f)) , 2 ) + 
            POW((53 * (longitude - %f)), 2)) < 0.3 
            and map_latlng.polyline_id in (SELECT distinct map_latlng.polyline_id
            FROM map_latlng
            WHERE
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
