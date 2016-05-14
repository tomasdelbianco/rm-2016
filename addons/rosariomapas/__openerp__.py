{
    'name': "Rosario Mapas",
    'version': '1.0',
    'depends': ['base'],
    'author': "Tomas Del Bianco",
    'category': 'Category',
    'description': """
    Modulo de Rosario Mapas
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'transporte_view.xml',
        'item_view.xml',
        'wizard/importar_kml_view.xml',
    ],
}