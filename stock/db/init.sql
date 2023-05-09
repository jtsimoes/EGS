CREATE USER 'stock'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE IF NOT EXISTS stockdb;
USE stockdb;

-- Lazer
INSERT INTO categories (name, image) VALUES ('Lazer', 'lazer.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Brinquedos e Jogos', 1, 'brinquedos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Instrumentos Musicais', 1, 'instrumentos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Livros e Revistas', 1, 'livros.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Coleções e Antiguidades', 1, 'colecoes.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Bilhetes e Espetáculos', 1, 'bilhetes.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('DVDs e Filmes', 1, 'dvds.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('CDs, Discos de Vinil e Música', 1, 'cds.jpg');

-- Desporto
INSERT INTO categories (name, image) VALUES ('Desporto', 'desporto.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Ciclismo', 2, 'ciclismo.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Surf e Bodyboard', 2, 'surf.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Caminhada, Corrida e Atletismo', 2, 'caminhada.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Campismo', 2, 'campismo.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Futsal e Futebol', 2, 'futsal.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Patins, Skates e Trotinetes', 2, 'patins.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Pesca e Mergulho', 2, 'pesca.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Ski e Snowboard', 2, 'ski.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Outros Desportos', 2, 'outros_desportos.jpg');

-- Moda
INSERT INTO categories (name, image) VALUES ('Moda', 'moda.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Bebé e Criança', 3, 'bebe.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Roupa', 3, 'roupa.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Calçado', 3, 'calcado.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Jóias, Relógios e Bijuteria', 3, 'joias.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Malas e Acessórios', 3, 'malas.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Saúde e Beleza', 3, 'saude.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Retrosaria', 3, 'retrosaria.jpg');

-- Casa
INSERT INTO categories (name, image) VALUES ('Casa', 'casa.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Artigos de Cozinha', 4, 'cozinha.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Móveis', 4, 'moveis.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Eletrodomésticos', 4, 'eletrodomesticos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Decorativos', 4, 'decorativos.jpg');

-- Jardinagem
INSERT INTO categories (name, image) VALUES ('Jardinagem', 'jardinagem.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Utilidades e Decoração', 5, 'utilidades.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Sementes, Árvores e Produtos Agrícolas', 5, 'sementes.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Máquinas e Ferramentas', 5, 'maquinas.jpg');

-- Tecnologia
INSERT INTO categories (name, image) VALUES ('Tecnologia', 'tecnologia.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Telemóveis', 6, 'telemoveis.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Tablets', 6, 'tablets.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Videojogos e Consolas', 6, 'videojogos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Computadores e Informática', 6, 'computadores.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Eletrónica', 6, 'eletronica.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('TV, Som e Fotografia', 6, 'tv.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Acessórios', 6, 'acessorios.jpg');

-- Veículos
INSERT INTO categories (name, image) VALUES ('Veículos', 'veiculos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Carros', 7, 'carros.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Motociclos e Scooters', 7, 'motociclos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Barcos e Lanchas', 7, 'barcos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Autocaravanas e Reboques', 7, 'autocaravanas.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Comerciais e Camiões', 7, 'comerciais.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Tratores e Alfaias Agrícolas', 7, 'tratores.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Outros Veículos', 7, 'outros_veiculos.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Peças e Acessórios', 7, 'pecas.jpg');

-- Equipamento Profissional
INSERT INTO categories (name, image) VALUES ('Equipamento Profissional', 'equipamento.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Industrial', 8, 'industrial.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Hotelaria e Restauração', 8, 'hotelaria.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Materiais de Construção Civil', 8, 'construcao.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Lojas e Comércio', 8, 'lojas.jpg');
INSERT INTO subcategories (name, category_id, image) VALUES ('Segurança e Vigilância', 8, 'seguranca.jpg');

-- Outros
INSERT INTO categories (name, image) VALUES ('Outros', 'outros.jpg');