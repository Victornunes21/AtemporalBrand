CREATE DATABASE AtemporalBrand;
USE AtemporalBrand;


CREATE TABLE Cliente(
	clienteID INT auto_increment primary key,
    nome VARCHAR(45),
    senha VARCHAR(45) NOT NULL,
    email VARCHAR(100) UNIQUE,
    cpf VARCHAR(14) NOT NULL UNIQUE
    
);

CREATE TABLE Contato(
	contatoID INT auto_increment primary key,
    ddd INT,
    telefone VARCHAR(45),
    clienteID INT,
    fornecedorID INT,
    foreign key(clienteID) REFERENCES Cliente(clienteID),
    foreign key(fornecedorID) REFERENCES Fornecedor(fornecedorID)
);
	

CREATE TABLE Fornecedor(
	fornecedorID INT auto_increment primary key,
    nome VARCHAR(45),
    senha VARCHAR(45) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Produto(
	produtoID INT auto_increment primary key,
    nome VARCHAR(45),
    descricao VARCHAR(200),
    quantProduto VARCHAR(45),
    valorProduto FLOAT,
    tamanhoProduto VARCHAR(45) 
);

CREATE TABLE Endereco(
	enderecoID INT auto_increment primary key,
	rua VARCHAR(150),
    bairro VARCHAR(45),
    numero INT,
    complemento varchar(45),
    cidade VARCHAR(45),
    estado VARCHAR(45),
    cep VARCHAR(45),
	pais VARCHAR(45),
    clienteID INT,
    foreign key(clienteID) REFERENCES Cliente(clienteID)
	
);

CREATE TABLE Categoria(
	categoriaID INT auto_increment primary key,
    nome VARCHAR(45)
	
);

CREATE TABLE ProdutoCategoria(
	produtoID INT,
    categoriaID INT,
    foreign key (produtoID) REFERENCES Produto(produtoID),
	foreign key (categoriaID) REFERENCES Categoria (categoriaID)
);

CREATE TABLE Compra(
	compraID INT auto_increment primary key,
    valor VARCHAR(45),
    dataCompra DATE,
    clienteID INT,
    foreign key(clienteID) REFERENCES Cliente(clienteID)
    
);

CREATE TABLE Carrinho(
	carrinhoID INT auto_increment primary key,
    clienteID INT,
    foreign key(clienteID)  REFERENCES Cliente(clienteID)
    
);

CREATE TABLE CarrinhoProduto(
	 quantidade INT,
     total FLOAT,
     carrinhoID INT,
     produtoID INT,
	 foreign key(carrinhoID) REFERENCES Carrinho(carrinhoID),
     foreign key(produtoID) REFERENCES Produto(produtoID)
);


CREATE TABLE Estoque(
	estoqueID INT auto_increment primary key,
    quantProduto INT,
    fornecedorID INT,
    produtoID INT,
    foreign key(fornecedorID) REFERENCES Fornecedor(fornecedorID),
	foreign key(produtoID) REFERENCES Produto(produtoID)
);


CREATE TABLE Imagem(
	imagemID INT auto_increment primary key,
    url VARCHAR(250),
    produtoID INT,
	foreign key(produtoID) REFERENCES Produto(produtoID)
);