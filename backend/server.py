#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, abort
import logging
from database.dml import *


logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route("/model/add-candidate", methods=["POST"])
def main():
    return "ok"


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, threaded=True)
