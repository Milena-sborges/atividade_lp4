import mysql.connector
from mysql.connector import Error

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1953dark',
            database='ecommerce', 
            port='3306'
        )
        if conexao.is_connected():
            print("Conexão ao MySQL estabelecida com sucesso!")
            return conexao
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def cadastrar_cliente(conexao, nome, cpf):
    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO Cliente (nome, cpf) VALUES (%s, %s)"
        valores = (nome, cpf)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Cliente {nome} cadastrado com ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Erro ao inserir cliente: {e}")

def cadastrar_vendedor(conexao, nome):
    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO Vendedor (nome) VALUES (%s)"
        valores = (nome,)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Vendedor {nome} cadastrado com ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Erro ao inserir vendedor: {e}")

def inserir_nota(conexao, fk_venda):
    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO NotaFiscal (fk_venda) VALUES (%s)"
        valores = (fk_venda,)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Nota Fiscal gerada com sucesso para a venda {fk_venda}!")
    except Error as e:
        print(f"Erro ao inserir nota fiscal: {e}")

def realizar_vendas(conexao, percentual_desconto, data_venda, fk_vendedor, fk_cliente, valor_total):
    try:
        cursor = conexao.cursor()
        sql = """INSERT INTO Venda (percentual_desconto, data_venda, fk_vendedor, fk_cliente, valor_total) 
                 VALUES (%s, %s, %s, %s, %s)"""
        valores = (percentual_desconto, data_venda, fk_vendedor, fk_cliente, valor_total)
        cursor.execute(sql, valores)
        
        id_venda_gerada = cursor.lastrowid
        conexao.commit()
        
        print(f"\nVenda realizada! ID: {id_venda_gerada}")
        
        inserir_nota(conexao, id_venda_gerada)
        
    except Error as e:
        print(f"Erro ao inserir venda: {e}")

def relatorio_clientes(conexao):
    try:
        cursor = conexao.cursor()
        sql = "SELECT pk_cliente, nome, cpf FROM Cliente"

        cursor.execute(sql)
        resultados = cursor.fetchall()

        for resultado in resultados:
            pk_cliente, nome, cpf = resultado 
            print(f"ID: {pk_cliente} | Nome: {nome} | CPF: {cpf}")

        print(f"\nTotal de clientes: {len(resultados)}")

    except Error as e:
        print(f"Erro ao gerar relatório de clientes: {e}")

def relatorio_vendedores(conexao):
    try:
        cursor = conexao.cursor()

        sql = "SELECT pk_vendedor, nome FROM Vendedor"

        cursor.execute(sql)
        resultados = cursor.fetchall()

        for resultado in resultados:
            pk_vendedor, nome = resultado
            print(f"ID Vendedor: {pk_vendedor} | Nome: {nome}")

        print(f"\nTotal de vendedores: {len(resultados)}")

    except Error as e:
        print(f"Erro ao gerar relatório de vendedor: {e}")

def relatorio_vendas_por_cliente(conexao, nome_cliente):
    try:
        cursor = conexao.cursor()
        
        sql = """
            SELECT v.pk_venda, v.data_venda, v.valor_total, v.percentual_desconto
            FROM Venda v
            JOIN Cliente c ON v.fk_cliente = c.pk_cliente
            WHERE c.nome = %s
        """
        
        cursor.execute(sql, (nome_cliente,))
        resultados = cursor.fetchall()

        print(f"\n Relatório de Vendas: ")
        
        if not resultados:
            print("Nenhuma venda encontrada para este cliente.")
        else:
            for v in resultados:
                id_venda, data, total, desc = v
                print(f"Venda ID: {id_venda} | Data: {data} | Total: R${total:.2f} | Desconto: {desc}%")
            
            print(f"Total de pedidos realizados: {len(resultados)}")

    except Error as e:
        print(f"Erro ao gerar relatório de vendas por cliente: {e}")

def relatorio_vendas_por_vendedor(conexao, nome_vendedor):
    try:
        cursor = conexao.cursor()
        
        sql = """
            SELECT v.pk_venda, v.data_venda, v.valor_total, c.nome
            FROM Venda v
            JOIN Vendedor vend ON v.fk_vendedor = vend.pk_vendedor
            JOIN Cliente c ON v.fk_cliente = c.pk_cliente
            WHERE vend.nome = %s
        """
        
        cursor.execute(sql, (nome_vendedor,))
        resultados = cursor.fetchall()

        print(f"\n--- Vendas Realizadas por: {nome_vendedor} ---")
        
        if not resultados:
            print(f"Nenhum registro de venda encontrado para o vendedor '{nome_vendedor}'.")
        else:
            print(f"{'ID Venda':<10} | {'Data':<20} | {'Cliente':<20} | {'Valor':<10}")
            print("-" * 65)
            
            for linha in resultados: