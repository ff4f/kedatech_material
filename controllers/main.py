import werkzeug.wrappers
import json

from odoo import http
from odoo.http import request

def valid_response(data, status=200):
    data = {"count": len(data), "data": data}
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data),
    )

def invalid_response(typ, message=None, status=401):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {
                "type": typ,
                "message": str(message)
                if str(message)
                else "wrong arguments (missing validation)",
            }
        ),
    )


class MaterialRestAPI(http.Controller):

    def _get_json_key(self):
        return ('name', 'code', 'type', 'price', 'partner_id')

    def check_keys(self, keys, vals):
        result = False
        for rec in keys:
            if rec in vals:
                result = True
            else:
                result = False
                break
        return result

    @http.route(['/api/material/list',
                '/api/material/list/id/<int:id>',
                '/api/material/list/type/<string:type>'
                ], auth='public', type="http", csrf=False, methods=['GET'])
    def get_material_list(self, id=False, type=False, **kwargs):
        result = {}
        domain = []

        if id:
            domain.append(('id', '=', id))

        if type:
            domain.append(('type', '=', type))

        material_ids = request.env['material'].sudo().search(domain)
        material_list = []

        try:
            for material_id in material_ids:
                data = {
                    'name': material_id.name,
                    'code': material_id.code,
                    'type': material_id.type.title(),
                    'price': material_id.price,
                    'partner_id': material_id.partner_id.display_name,
                }
                material_list.append(data)

            result['result'] = material_list
            result['code'] = 200
            result['message'] = "success"
            return valid_response(result)

        except Exception as e:
            return invalid_response("exception", e, 503)

    @http.route(['/api/create/material'], csrf=False, auth="public", type='json', methods=['POST'])
    def create_material(self, **kwargs):
        materials = request.jsonrequest
        keys = self._get_json_key()
        result = {}

        if self.check_keys(keys, materials):
            try:
                material_id = request.env['material'].sudo().create(materials)
                result = {
                    'result': material_id,
                    'code': 200,
                    'message': 'success'
                }
                return valid_response(result)

            except Exception as e:
                return invalid_response("Failed create material", e, 401)

        else:
            return invalid_response("Check request body", [], 500)

    @http.route('/api/delete/material/id/<int:material_id>/', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id):
        try:
            material = request.env['material'].sudo().search([('id', '=', material_id)])
            if material:
                result = {
                    'message': 'success',
                    'id': material_id,
                    'code': 200
                }
                material.unlink()
                return valid_response(result)
            else:
                return invalid_response("Material does not exist", [], 401)
        except Exception as e:
            return invalid_response("Failed delete material", e, 401)

    @http.route('/api/update/material/id/<int:material_id>/', auth='public', type='json', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        materials = request.jsonrequest
        keys = self._get_json_key()
        params_dict = {}

        for material_key in materials.keys():
            if material_key not in keys:
                return invalid_response("Check body request", [], 401)

        if materials.get('price') <= 100:
            return invalid_response("Failed, material price should higher than 100", [], 401)


        partner_id = request.env['res.partner'].sudo().browse([(materials.get('partner_id'))])
        if not partner_id:
            return invalid_response("Failed, Supplier does not exist", [], 404)

        material = request.env['material'].sudo().search([('id', '=', material_id)])
        if not material:
            return invalid_response("Failed, Material does not exist", [], 404)

        material = material.write(materials)
        result = {
            'result': material,
            'code': 200,
            'message': 'data updated'
        }
        return valid_response(result)
