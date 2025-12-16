{
    'name':'Real Estate',
    'version':'1.0',
    'category':'Training',
    'summary':'This is Training purpose only',
    'description':'Custom Real Estate Module',
    'author':'Neeraj Sharma',
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_menus.xml',
    ],
    'depends':['base'],
    'installable':True,
    'application':True,
}