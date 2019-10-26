#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from controllers.dml import *
from database.schema import Cliente, validate_document
from datetime import datetime, date


app = Flask(__name__)


##############################################
#                  Clientes                  #
##############################################
@app.route("/client/add", methods=["POST"])
def add_client():
    data = request.get_json(silent=True)
    dml = DML()

    cliente = validate_document(data, Cliente)

    try:
        dml.insert_client(cliente)
    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/client/del", methods=["POST"])
def del_client():
    data = request.get_json(silent=True)
    dml = DML()
    try:
        dml.delete_client(data["id"])

    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/client/edit", methods=["POST"])
def edit_client():
    data = request.get_json(silent=True)
    dml = DML()

    try:
        dml.edit_client(data["query"], data["where"])
    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/client/find", methods=["POST"])
def find_client():
    data = request.get_json(silent=True)
    dml = DML()

    try:
        json_ = dml.find_client(data["where"])
    except Exception as err:
        logging.critical(err, type(err))
        json_ = {}
    finally:
        dml.destroy_me()

    return jsonify(json_)


##############################################
#                  Comandas                  #
##############################################
@app.route("/comanda/add", methods=["POST"])
def add_comanda():
    cliente_id = request.get_json(silent=True)["cliente_id"]
    dml = DML()

    try:
        dml.insert_comanda(
            cliente_id=cliente_id,
            inicio=str(datetime.now()),
            data_comanda=str(date.today()),
        )
    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/comanda/delete", methods=["POST"])
def delete_comanda():
    cliente_id = request.get_json(silent=True)["cliente_id"]
    dml = DML()

    try:
        dml.delete_comanda(
            cliente_id=cliente_id,
            data_comanda=str(date.today()),
        )
    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/comanda/find_by_user_id", methods=["POST"])
def find_user_id_comanda():
    cliente_id = request.get_json(silent=True)["cliente_id"]
    dml = DML()

    try:
        _id = dml.find_active_comanda_by_client_id(
            cliente_id=cliente_id,
            data_comanda=str(date.today()),
        )
    except Exception as err:
        logging.critical(err, type(err))
        _id = None
    finally:
        dml.destroy_me()

    return jsonify(ID=_id[0] if _id else _id)


##############################################
#                   HEALTH                   #
##############################################
@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, threaded=True)
