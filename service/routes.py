"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application

from flask import jsonify, request, make_response, abort, url_for
from http import HTTPStatus  # Use standard HTTP status codes


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), HTTPStatus.OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        HTTPStatus.OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based on the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), HTTPStatus.CREATED, {"Location": location_url}
    )


######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint will read an Account based on the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)
    account = Account.find(account_id)
    if not account:
        abort(HTTPStatus.NOT_FOUND, f"Account with id [{account_id}] could not be found.")
    return account.serialize(), HTTPStatus.OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
