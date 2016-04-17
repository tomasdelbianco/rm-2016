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
            'colectivos': Colectivos.search([], order="name")
        })