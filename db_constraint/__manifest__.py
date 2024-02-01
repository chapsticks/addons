{
    'name': '物理外键拓展',
    'summary': '支持物理外键的建立和解除',
    'description': '支持物理外键的建立和解除，odoo默认所有外键都会在数据库层面进行外键约束的建立，该模块将orm与数据层的物理外键解耦，同时保有orm的外键关联查询可用',
    'website': '',
    'author': "周士超",
    'version': '1.0',
    'category': 'base',
    'depends': [],
    "images": ['static/img/db_constraint_true.png', 'static/img/db_constraint_false.png'],
    'data': [
    ],
    'assets': {
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
