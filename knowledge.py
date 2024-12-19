from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from knowledge_service import ExternalDatasetService

app = Flask(__name__)
api = Api(app)

class BedrockRetrievalApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("retrieval_setting", nullable=False, required=True, type=dict, location="json")
        parser.add_argument("query", nullable=False, required=True, type=str)
        parser.add_argument("knowledge_id", nullable=False, required=True, type=str)
        args = parser.parse_args()

        # Authorization check
        auth_header = request.headers.get("Authorization")
        if " " not in auth_header:
            return {"error_code": 1001, "error_msg": "Invalid Authorization header format."}, 403
        
        auth_scheme, auth_token = auth_header.split(None, 1)
        if auth_scheme.lower() != "bearer":
            return {"error_code": 1001, "error_msg": "Invalid Authorization header format."}, 403
        
        if auth_token:
            # process your authorization logic here
            pass
        
        # Call the knowledge retrieval service
        result = ExternalDatasetService.knowledge_retrieval(args["retrieval_setting"], args["query"], args["knowledge_id"])
        return result, 200

api.add_resource(BedrockRetrievalApi, '/retrieval')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
