from odoo import exceptions
from odoo.tests import common


class MaterialTest(common.TransactionCase):

    def setUp(self):
        super(MaterialTest, self).setUp()
        self.material = self.env['material']
        self.supplier = self.env['res.partner']

        self.supplier_data = {
            'name': 'Toko ABC',
        }
        self.supplier_id = self.supplier.create(self.supplier_data)

        self.material_data = {
            'name': 'Kain Kuning',
            'code': 'KK',
            'type': 'jeans',
            'price': 150,
            'partner_id': self.supplier_id.id,
        }

        self.material = self.material.create(self.material_data)

    def test_create(self):
        self.assertEqual(self.material.name, 'Kain Kuning')
        self.assertEqual(self.material.code, 'KK')
        self.assertEqual(self.material.type, 'jeans')
        self.assertEqual(self.material.price, 150)
        self.assertEqual(self.material.partner_id.id, self.supplier_id.id)

        print('Your test create was succesfull!')

    def test_invalid_price(self):
        with self.assertRaises(exceptions.ValidationError):
            self.material.write({
                'price': 50,
            })

        print('Your test invalid price was succesfull!')

    def test_update(self):
        self.material.write({'name': 'Kain Biru'})
        self.material.write({'code': 'KB'})
        self.material.write({'type': 'fabric'})
        self.material.write({'price': 300})

        self.assertEqual(self.material.name, 'Kain Biru')
        self.assertEqual(self.material.code, 'KB')
        self.assertEqual(self.material.type, 'fabric')
        self.assertEqual(self.material.price, 300)

    def test_filter(self):
        material_data_2 = {
            'name': 'Kain Hijau 2',
            'code': 'KH22',
            'type': 'jeans',
            'price': 250,
            'partner_id': self.supplier_id.id,
        }
        material_data_3 = {
            'name': 'Kain Hijau 3',
            'code': 'KH3',
            'type': 'fabric',
            'price': 300,
            'partner_id': self.supplier_id.id,
        }

        material_2 = self.material.create(material_data_2)
        material_3 = self.material.create(material_data_3)

        jeans_materials_item = self.material.search([('type', '=', 'jeans')])
        self.assertNotEqual(len(jeans_materials_item), 2)

        material_ids = jeans_materials_item.ids
        self.assertIn(material_2.id, material_ids)
        self.assertNotIn(material_3.id, material_ids)

        print('Your test filter was succesfull!')

    def test_delete(self):
        self.material.unlink()
        print('Your test delete was succesfull!')