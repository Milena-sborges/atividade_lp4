import mysql.connector
from mysql.connector import Error

def conectar_banco():
    """Estabelece a conexão com o banco de dados MySQL."""
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
        valores = (nome,) # Vírgula necessária para indicar que é uma tupla
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Vendedor {nome} cadastrado com ID: {cursor.lastrowid}")
    except Error as e:
        print(f"Erro ao inserir vendedor: {e}")

def inserir_nota(conexao, fk_venda):
    """Gera uma nota fiscal vinculada a uma venda específica."""
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
        sql = "SELECT pk_cliente, nome, cpf FROM cliente"

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

        sql = "SELECT pk_vendedor, nome FROM vendedor"

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
            FROM venda v
            JOIN cliente c ON v.fk_cliente = c.pk_cliente
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
        
        # SQL que conecta a venda ao vendedor (para filtrar pelo nome)
        # e ao cliente (para mostrar o nome de quem comprou)
        sql = """
            SELECT v.pk_venda, v.data_venda, v.valor_total, c.nome
            FROM venda v
            JOIN vendedor vend ON v.fk_vendedor = vend.pk_vendedor
            JOIN cliente c ON v.fk_cliente = c.pk_cliente
            WHERE vend.nome = %s
        """
        
        cursor.execute(sql, (nome_vendedor,))
        resultados = cursor.fetchall()

        print(f"\n--- Vendas Realizadas por: {nome_vendedor} ---")
        
        if not resultados:
            print(f"Nenhum registro de venda encontrado para o vendedor '{nome_vendedor}'.")
        else:
            # Cabeçalho do relatório
            print(f"{'ID Venda':<10} | {'Data':<20} | {'Cliente':<20} | {'Valor':<10}")
            print("-" * 65)
            
            for linha in resultados:
                id_venda, data, valor, nome_cliente = linha
                # formatamos o valor para 2 casas decimais com .2f
                print(f"{id_venda:<10} | {str(data):<20} | {nome_cliente:<20} | R$ {valor:<10.2f}")
            
            print(f"\nTotal de vendas do vendedor: {len(resultados)}")

    except Error as e:
        print(f"Erro ao gerar relatório de vendas por vendedor: {e}")

if __name__ == "__main__":
    conexao = conectar_banco()

    if conexao:

     
        cadastrar_cliente(conexao, "Milena Souza", 11122233344)
        cadastrar_cliente(conexao, "Gustavo Silva", 22233344455)
        cadastrar_cliente(conexao, "Ana Beatriz", 33344455566)
        cadastrar_cliente(conexao, "Ricardo Oliveira", 44455566677)
        cadastrar_cliente(conexao, "Carla Mendes", 55566677788)
        cadastrar_cliente(conexao, "Marcos Pontes", 66677788899)
        cadastrar_cliente(conexao, "Fernanda Lima", 77788899900)
        cadastrar_cliente(conexao, "Lucas Rocha", 88899900011)
        cadastrar_cliente(conexao, "Julia Costa", 99900011122)
        cadastrar_cliente(conexao, "Roberto Junior", 10020030044)

      
  
        cadastrar_vendedor(conexao, "Vendedor João")
        cadastrar_vendedor(conexao, "Vendedora Maria")
        cadastrar_vendedor(conexao, "Vendedor Paulo")

        
        
        realizar_vendas(conexao, 5.0, '2026-05-01 10:00:00', 1, 1, 150.00)
        realizar_vendas(conexao, 0.0, '2026-05-01 11:30:00', 2, 2, 200.50)
        realizar_vendas(conexao, 10.0, '2026-05-02 09:15:00', 3, 3, 89.90)
        realizar_vendas(conexao, 2.5, '2026-05-02 14:00:00', 1, 4, 1200.00)
        realizar_vendas(conexao, 0.0, '2026-05-03 16:45:00', 2, 5, 45.00)
        realizar_vendas(conexao, 5.0, '2026-05-03 17:00:00', 3, 6, 310.00)
        realizar_vendas(conexao, 7.0, '2026-05-04 10:20:00', 1, 7, 99.00)
        realizar_vendas(conexao, 0.0, '2026-05-04 11:00:00', 2, 8, 250.00)
        realizar_vendas(conexao, 15.0, '2026-05-05 13:10:00', 3, 9, 500.00)
        realizar_vendas(conexao, 0.0, '2026-05-05 15:30:00', 1, 10, 75.20)
        realizar_vendas(conexao, 5.0, '2026-05-06 09:00:00', 2, 1, 180.00)
        realizar_vendas(conexao, 10.0, '2026-05-06 10:45:00', 3, 2, 60.00)
        realizar_vendas(conexao, 2.0, '2026-05-07 11:20:00', 1, 3, 400.00)
        realizar_vendas(conexao, 0.0, '2026-05-07 14:15:00', 2, 4, 120.00)
        realizar_vendas(conexao, 8.0, '2026-05-07 16:50:00', 3, 5, 215.00)

        print("\n>>> GERANDO RELATÓRIO DE CLIENTES...")
        relatorio_clientes(conexao)

        # --- RELATÓRIO 2: Todos os vendedores ---
        print("\n>>> GERANDO RELATÓRIO DE VENDEDORES...")
        relatorio_vendedores(conexao)

        print("\n" + "="*50)
        print("FILTROS PERSONALIZADOS")
        print("="*50)

        # --- RELATÓRIO 3: Vendas por Cliente ---
        nome_cli = input("\nDigite o nome do CLIENTE para buscar as vendas: ")
        relatorio_vendas_por_cliente(conexao, nome_cli)

        # --- RELATÓRIO 4: Vendas por Vendedor ---
        nome_vend = input("\nDigite o nome do VENDEDOR para buscar as vendas: ")
        relatorio_vendas_por_vendedor(conexao, nome_vend)