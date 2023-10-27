# -*- coding: utf-8 -*-
{
    'name' : 'Material Management',
    'version' : '1.0',
    'summary' : 'Material Management',
    'sequence' : 10,
    'description' : """Material Management""",
    'category' : 'Productivity',
    'website' : '',
    'depends' : ['base'],
    'data' : [
        'security/ir.model.access.csv',
        'views/material_views.xml',
        'views/menu.xml',
    ],
    'demo' : [],
    'qweb' : [],
    'installable' : True,
    'application' : True,
    'auto_install' : False
}