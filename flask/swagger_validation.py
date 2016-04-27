from functools import wraps
from flask import Flask, request, abort
import json

app = Flask(__name__)

from bravado_core.spec import Spec
from bravado_core.validate import validate_schema_object
from bravado_core.param import get_param_type_spec

# Create a bravado core swagger spec object
with open('swagger.json', 'r') as f:
    spec = Spec.from_dict(json.loads(f.read()))


def swagger_validate(f):
    """
    Decorator that validates incoming requests using the provided swagger spec
    """
    @wraps(f)
    def swagger_validated_function(*args, **kwargs):
        converted_uri = request.path
        # convert /pet/mypetsid to /pet/{petId}
        for key, value in request.view_args.items():
            target = '{{{0}}}'.format(key)
            converted_uri = converted_uri.replace(str(value), target)
        # Grab the swagger spec for this specific uri and request type
        request_spec = spec.get_op_for_request(
            request.method.lower(), converted_uri)
        # cycle through the params and check any params that are set or required
        # by the schema
        for param in request_spec.params.values():
            param_spec = get_param_type_spec(param)
            # TODO - grab out other request types that we care about
            param_value = None
            if param.location == 'formData':
                param_value = request.form.get(param.name)
            elif param.location == 'path':
                param_value = request.view_args.get(param.name)
            if param_value or param.required:
                try:
                    validate_schema_object(spec, param_spec, param_value)
                except Exception as e:
                    abort(400, str(e))
        return f(*args, **kwargs)
    return swagger_validated_function


@app.route('/v2/pet/<int:petId>', methods=['GET', 'POST'])
@swagger_validate
def pet_handler(petId):
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
