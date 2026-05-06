CREATE DATABASE IF NOT EXISTS ecommerce;
USE ecommerce;

-- Tabela cliente
CREATE TABLE cliente (
    pk_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cpf BIGINT
);

-- Tabela vendedor
CREATE TABLE vendedor (
    pk_vendedor INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL
);

-- Tabela venda
CREATE TABLE venda (
    pk_venda INT PRIMARY KEY AUTO_INCREMENT,
    percentual_desconto FLOAT,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    fk_vendedor INT,
    fk_cliente INT,
    valor_total FLOAT,
    CONSTRAINT fk_venda_vendedor FOREIGN KEY (fk_vendedor) REFERENCES vendedor(pk_vendedor),
    CONSTRAINT fk_venda_cliente FOREIGN KEY (fk_cliente) REFERENCES cliente(pk_cliente)
);

-- Tabela notafiscal
CREATE TABLE notafiscal (
    pk_notafiscal INT PRIMARY KEY AUTO_INCREMENT,
    fk_venda INT UNIQUE,
    CONSTRAINT fk_nota_venda FOREIGN KEY (fk_venda) REFERENCES venda(pk_venda)
);