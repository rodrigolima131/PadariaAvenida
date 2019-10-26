#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, abort
import logging
from database.dml import *


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/client/add", methods=["POST"])
def client_add():
    data = request.get_json(silent=True)
    dml = DML()
    try:
        dml.insert_client(data["nome"], data["cpf"], data.get("telefone", ""))
    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return "200"


@app.route("/client/del", methods=["POST"])
def client_del():
    data = request.get_json(silent=True)
    dml = DML()
    try:
        dml.delete_client(data["id"])

    except Exception as err:
        logging.critical(err, type(err))
    finally:
        dml.destroy_me()

    return "200"


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, threaded=True)
