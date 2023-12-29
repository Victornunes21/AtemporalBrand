USE AtemporalBrand;

INSERT INTO Produto(nome, quantProduto, valorProduto, tamanhoProduto, descricao) VALUES
	("Calça", "20", "179.90", "P, M, G", "Calça feminina wide leg"),
    ("Macacão", "20", "129.90", "P, M, G", "Macacão feminino em lamê plissado com decote v prata"),
    ("Vestido", "20", "129.90", "P, M, G", "Vestido curto amplo brilhante com amarração prata"),
    ("Vestido", "20", "179.90", "P, M, G", "Vestido midi evasê com bolso nas laterais lilás"),
    ("Vestido", "20", "159.90", "P, M, G", "Vestido longo evasê com bolso bege"),
    ("Vestido", "20", "199.90", "P, M, G", "Vestido jeans curto tubinho denim médio"),
    ("Camiseta", "20", "69.90", "P, M, G", "Camiseta feminina canelada branca"),
    ("Blusa", "20", "59.90", "P, M, G", "Blusa cropped manga curta lisa - Rosa"),
    ("Camisa", "20", "59.90", "P, M, G", "Camisa polo masculina manga curta - Vermelho"),
    ("Camiseta", "20", "39.90", "P, M, G", "Camiseta masculina relaxed texturizada preta"),
    ("Camiseta", "20", "59.90", "P, M, G", "Camiseta masculina regular âncora verde"),
    ("Calça", "20", "119.90", "P, M, G", "Calça jeans masculina jogger com cordão denim médio"),
    ("Calça", "20", "119.90", "P, M, G", "Calça jeans masculina jogger com cordão denim claro"),
    ("Calça", "20", "119.90", "P, M, G", "Calça esportiva masculina CBV azul");


INSERT INTO CLIENTE(nome, email, cpf, senha) VALUES
	("cliente1", "cliente@gmail.com1", "12345678900", "senha1"),
	("cliente2", "cliente@gmail.com2", "98776543211", "senha2");


SELECT * FROM Produto;
SELECT * FROM Cliente;