#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from controllers.dml import *
from database.schema import Cliente, Produto, validate_document
from datetime import datetime, date
from schematics.exceptions import DataError

import sqlite3


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


##############################################
#                  Clientes                  #
##############################################
@app.route("/cliente/add", methods=["POST"])
def add_client():
    data = request.get_json(silent=True)
    dml = DML()

    cliente = validate_document(data, Cliente)

    try:
        dml.insert_client(cliente)
    except sqlite3.IntegrityError as e:
        logging.critical(f"Cliente com cpf {cliente.cpf} já adicionado.")
        return jsonify(
            error=404,
            message="Cliente já adicionado.",
        ), 404

    except Exception as err:
        logging.critical(err, type(err))
        abort(500, description=str(err))
    finally:
        dml.destroy_me()

    return jsonify(ok=True), 201


@app.route("/cliente/del", methods=["POST"])
def del_client():
    data = request.get_json(silent=True)
    dml = DML()
    try:
        dml.delete_client(data["id"])
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True)


@app.route("/cliente/edit", methods=["POST"])
def edit_client():
    data = request.get_json(silent=True)
    dml = DML()

    try:
        dml.edit_client(data["query"], data["where"])
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True)


@app.route("/cliente/find", methods=["POST"])
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


@app.route("/cliente/all")
def find_all_client():
    dml = DML()

    try:
        json_ = dml.find_all_clientes()
    except Exception as err:
        logging.critical(err, type(err))
        json_ = []
    finally:
        dml.destroy_me()

    return jsonify(json_)


##############################################
#                  Comandas                  #
##############################################
@app.route("/comanda/start", methods=["POST"])
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
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True), 201


@app.route("/comandas/total", methods=["POST"])
def total_comanda():
    comanda_id = request.get_json(silent=True)["comanda_id"]
    dml = DML()

    try:
        total = dml.total_comanda(comanda_id)
        dml.destroy_me()
        return jsonify(total=total)

    except Exception as err:
        logging.critical(err, type(err))
        dml.destroy_me()
        return jsonify(error=400), 400


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
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True)


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


@app.route("/comanda/order", methods=["POST"])
def find_produtos_by_comanda_id():
    comanda_id = request.get_json(silent=True)["comanda_id"]
    dml = DML()

    order = dml.order(comanda_id)
    dml.destroy_me()

    return jsonify(order)


@app.route("/comandas/active")
def active_comandas():
    dml = DML()

    try:
        comandas = dml.find_active_comandas()
    except Exception as err:
        logging.critical(err, type(err))
        comandas = []
    finally:
        dml.destroy_me()

    return jsonify(comandas)


@app.route("/comanda/edit", methods=["POST"])
def edit_comanda():
    data = request.get_json(silent=True)
    dml = DML()

    try:
        dml.edit_comanda(data["query"], data["where"])
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/comanda/finish", methods=["POST"])
def finish_comanda():
    cliente_id = request.get_json(silent=True)["cliente_id"]
    dml = DML()

    try:
        dml.finish_comanda(
            cliente_id=cliente_id,
            fim=str(datetime.now())
        )
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True)

##############################################
#                 PRODUTOS                   #
##############################################
@app.route("/produto/add", methods=["POST"])
def add_produto():
    values = request.get_json(silent=True)
    dml = DML()

    try:
        produto_values = validate_document(values, Produto)
        dml.insert_produto(produto_values)
    except DataError as e:
        logging.critical("Argumentos recebidos invalidos.")
        abort(406, description="Argumentos Passados inválidos.")
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True), 201


@app.route("/produto/del", methods=["POST"])
def delete_produto():
    produto_id = request.get_json(silent=True)["produto_id"]
    dml = DML()

    try:
        dml.delete_produto(produto_id=produto_id)
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=True)


@app.route("/produtos/all")
def all_produtos():
    dml = DML()

    try:
        comandas = dml.find_all_products()
    except Exception as err:
        logging.critical(err, type(err))
        comandas = []
    finally:
        dml.destroy_me()

    return jsonify(comandas)


@app.route("/produto/like", methods=["POST"])
def like_produto():
    produto = request.get_json(silent=True)["produto"]
    dml = DML()

    try:
        json_ = dml.find_like_produtos(product_name=produto)
    except Exception as err:
        logging.critical(err, type(err))
        json_ = {}
    finally:
        dml.destroy_me()

    return jsonify(json_)


@app.route("/produto/edit", methods=["POST"])
def edit_produto():
    data = request.get_json(silent=True)
    dml = DML()

    try:
        dml.edit_produto(data["query"], data["where"])
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


##############################################
#              PEDIDOSCOMANDAS               #
##############################################
@app.route("/pedido/add_produto", methods=["POST"])
def insert_produto_comanda():
    data = request.get_json(silent=True)
    dml = DML()
    try:
        dml.insert_pedido(data["comanda_id"], data["produto_id"], data["quantidade"])
    except Exception as err:
        dml.destroy_me()
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/pedido/remove_produto", methods=["POST"])
def remove_produto_comanda():
    data = request.get_json(silent=True)
    dml = DML()
    try:
        dml.remove_pedido(data["comanda_id"], data["produto_id"])
    except Exception as err:
        dml.destroy_me()
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


@app.route("/pedido/edit_pedido", methods=["POST"])
def edit_pedido():
    data = request.get_json(silent=True)
    dml = DML()

    try:
        dml.edit_pedido(data["query"], data["where"])
    except Exception as err:
        logging.critical(err, type(err))
        return jsonify(error=400), 400
    finally:
        dml.destroy_me()

    return jsonify(ok=200)


##############################################
#                   HEALTH                   #
##############################################
@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, threaded=True)
