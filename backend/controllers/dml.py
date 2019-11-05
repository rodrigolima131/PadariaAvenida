from database.db import Database
from database.schema import Cliente, Produto
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class DML:
    def __init__(self):
        self.conn = Database().create_connection()
        self.query_comanda_exists = """
        SELECT * FROM Comandas 
        WHERE cliente_id = {} 
            AND fim IS NULL 
            AND data_comanda = '{}';
        """

    def destroy_me(self):
        try:
            self.conn.close()
        except Exception as err:
            logging.critical(err, type(err))

    ##############################################
    #                  Clientes                  #
    ##############################################
    def insert_client(self, cliente: Cliente):
        self.conn.execute(
            "INSERT INTO Clientes (nome, cpf, telefone) VALUES (?, ?, ?)",
            (cliente.nome, cliente.cpf, cliente.telefone)
        )
        self.conn.commit()

    def delete_client(self, _id: int):
        self.conn.execute("DELETE FROM Clientes WHERE ID = ?", str(_id))
        self.conn.commit()

    def edit_client(self, set_query, where):
        self.conn.execute(f"UPDATE Clientes SET {set_query} WHERE {where}")
        self.conn.commit()

    def find_client(self, where):
        execute = self.conn.execute(f"SELECT * FROM Clientes WHERE {where}")
        fetch = execute.fetchone()
        return {k[0]: v for k, v in list(zip(execute.description, fetch))}

    def find_all_clientes(self):
        try:
            execute = self.conn.execute("SELECT ID, nome, telefone FROM Clientes;")
            fetch = execute.fetchall()

            columns = [v[0] for v in execute.description]

            list_return = []
            for f in fetch:
                list_return.append(
                    dict(zip(columns, f))
                )
            return list_return
        except Exception as e:
            logging.critical(e, type(e))
            return []

    ##############################################
    #                  Comandas                  #
    ##############################################
    def insert_comanda(self, cliente_id: str, inicio: str, data_comanda: str):
        verify = self.conn.execute(
            self.query_comanda_exists.format(cliente_id, data_comanda)
        )
        if not verify.fetchone():
            self.conn.execute(
                "INSERT INTO Comandas (cliente_id, inicio, data_comanda) VALUES (?, ?, ?)",
                (cliente_id, inicio, data_comanda)
            )
            self.conn.commit()

    def delete_comanda(self, cliente_id: int, data_comanda: str):
        self.conn.execute(
            f"DELETE FROM Comandas WHERE cliente_id = {str(cliente_id)} AND data_comanda = '{data_comanda}' AND fim IS NULL"
        )
        self.conn.commit()

    def find_active_comanda_by_client_id(self, cliente_id: int, data_comanda: str):
        try:
            execute = self.conn.execute(
                "SELECT ID FROM Comandas WHERE cliente_id = {} AND fim IS NULL and data_comanda = '{}'".format(
                    cliente_id, data_comanda
                )
            )
            fetch = execute.fetchone()
            return fetch
        except Exception as err:
            logging.critical(err, type(err))
            return None

    def order(self, comanda_id: int):
        try:
            execute = self.conn.execute(
                """SELECT produto, quantidade, ROUND(quantidade*valor, 2) as total FROM PedidosComanda
                JOIN Produtos ON PedidosComanda.produto_id = Produtos.ID
                WHERE comanda_id = {}""".format(
                    comanda_id
                )
            )
            fetch = execute.fetchall()

            columns = [v[0] for v in execute.description]

            list_return = []
            for f in fetch:
                list_return.append(
                    dict(zip(columns, f))
                )
            return list_return
        except Exception as err:
            logging.critical(err, type(err))
            return None

    def total_comanda(self, comanda_id):
        query = f"""
            SELECT SUM(valor * quantidade) AS total_value FROM PedidosComanda
            JOIN Produtos on PedidosComanda.produto_id = Produtos.ID
            WHERE comanda_id = {comanda_id};
        """
        try:
            execute = self.conn.execute(query)
            fetch = execute.fetchone()

            return fetch[0]
        except Exception as err:
            logging.critical(err, type(err))
            return {}

    def find_active_comandas(self):
        try:
            execute = self.conn.execute("""
                SELECT c.ID, c.cliente_id, cl.nome, c.inicio, c.fim, c.data_comanda 
                FROM Comandas c 
                JOIN Clientes cl ON c.cliente_id = cl.ID
                WHERE fim IS NULL 
                ORDER BY inicio ASC;
            """)
            fetch = execute.fetchall()

            columns = [v[0] for v in execute.description]

            list_return = []
            for f in fetch:
                list_return.append(
                    dict(zip(columns, f))
                )

            for comanda in list_return:
                total = self.total_comanda(comanda["ID"])
                comanda["total"] = round(total, 2) if total else 0

            return list_return
        except Exception as e:
            logging.critical(e, type(e))
            return []

    def edit_comanda(self, set_query, where):
        query = f"UPDATE Comandas SET {set_query} WHERE {where}"
        self.conn.execute(query)
        self.conn.commit()

    def finish_comanda(self, cliente_id: int, fim: str):
        self.conn.execute(f"UPDATE Comandas SET fim = '{fim}' WHERE cliente_id = {cliente_id} and fim IS NULL")
        self.conn.commit()

    ##############################################
    #                 PRODUTOS                   #
    ##############################################
    def insert_produto(self, produto_values: Produto):
        verify = self.conn.execute(f"SELECT * FROM Produtos WHERE produto = '{produto_values.produto}'; ")
        if not verify.fetchone():
            self.conn.execute(
                "INSERT INTO Produtos (produto, valor, unidade) VALUES (?, ?, ?);",
                (produto_values.produto, produto_values.valor, produto_values.unidade)
            )
            self.conn.commit()

    def delete_produto(self, produto_id: int):
        self.conn.execute(f"DELETE FROM Produtos WHERE ID = {produto_id};")
        self.conn.commit()

    def find_all_products(self):
        try:
            execute = self.conn.execute("SELECT * FROM Produtos;")
            fetch = execute.fetchall()

            columns = [v[0] for v in execute.description]

            list_return = []
            for f in fetch:
                list_return.append(
                    dict(zip(columns, f))
                )
            return list_return
        except Exception as e:
            logging.critical(e, type(e))
            return {}

    def find_like_produtos(self, product_name: str):
        try:
            execute = self.conn.execute(f"SELECT * FROM Produtos WHERE produto LIKE '%{product_name}%';")
            fetch = execute.fetchall()

            columns = [v[0] for v in execute.description]

            list_return = []
            for f in fetch:
                list_return.append(
                    dict(zip(columns, f))
                )
            return list_return
        except Exception as e:
            logging.critical(e, type(e))
            return []

    def edit_produto(self, set_query, where):
        query = f"UPDATE Produtos SET {set_query} WHERE {where};"
        self.conn.execute(query)
        self.conn.commit()

    ##############################################
    #              PEDIDOSCOMANDA                #
    ##############################################
    def insert_pedido(self, comanda_id: int, produto_id: int, quantidade):
        self.conn.execute(
            "INSERT INTO PedidosComanda (comanda_id, produto_id, quantidade) VALUES (?, ?, ?)",
            (comanda_id, produto_id, quantidade)
        )
        self.conn.commit()

    def remove_pedido(self, comanda_id: int, produto_id: int):
        self.conn.execute(
            "DELETE FROM PedidosComanda WHERE comanda_id = {} AND produto_id = {}".format(comanda_id, produto_id)
        )
        self.conn.commit()

    def edit_pedido(self, set_query, where):
        query = f"UPDATE PedidosComanda SET {set_query} WHERE {where}"
        self.conn.execute(query)
        self.conn.commit()
