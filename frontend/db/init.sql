DROP DATABASE IF EXISTS ressellr;
CREATE DATABASE ressellr;

CREATE OR REPLACE USER 'frontend'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON ressellr.* TO 'frontend'@'localhost';

USE ressellr;

CREATE TABLE users (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `token` VARCHAR(500),
    `username` VARCHAR(500) UNIQUE,
    `name` VARCHAR(500),
    `email` VARCHAR(500) UNIQUE,
    `avatar` VARCHAR(500) DEFAULT NULL,
    `rating` FLOAT DEFAULT 0.0,
    `total_sales` INT DEFAULT 0,
    `total_purchases` INT DEFAULT 0,
    `total_reviews` INT DEFAULT 0,
    `phone` INT UNIQUE,
    `registration` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `location` VARCHAR(500),
    `is_active` BOOLEAN DEFAULT TRUE
);


CREATE TABLE items (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(500) ,
    `date` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `description` VARCHAR(500),
    `price` FLOAT,
    `old_price` FLOAT DEFAULT NULL,
    `image` VARCHAR(500),
    `location` VARCHAR(500),
    `condition` VARCHAR(500),
    `is_available` BOOLEAN DEFAULT TRUE,
    `owner_id` INT,
    `category_id` INT,
    `product_id` INT,
    FOREIGN KEY (owner_id) REFERENCES users(id)
    -- FOREIGN KEY (category_id) REFERENCES categories(id) -- uncomment for external database/table
    -- FOREIGN KEY (product_id) REFERENCES products(id) -- uncomment for external database/table
);


-- Insert random users
INSERT INTO users (`token`, `username`, `name`, `email`, `avatar`, `rating`, `total_sales`, `total_purchases`, `total_reviews`, `phone`, `registration`, `location`, `is_active`)
VALUES
    ('token_user_1', 'jtsimoes', 'João Tomás', 'jtsimoes10@ua.pt', 'https://conteudo.imguol.com.br/c/entretenimento/80/2017/04/25/a-atriz-zoe-saldana-como-neytiri-em-avatar-1493136439818_v2_1x1.jpg', 4.5, 10, 8, 12, 123456789, NOW(), 'Gouveia', TRUE),
    ('token_user_2', 'carlos.costa', 'Carlos Costa', 'ccosta@ua.pt', 'https://icones.pro/wp-content/uploads/2021/03/avatar-de-personne-icone-homme.png', 3.8, 5, 15, 6, 987654321, NOW(), 'Gaia', TRUE),
    ('token_user_3', 'miguel_cabral', 'Miguel Cabral', 'cabral@ua.pt', 'https://st3.depositphotos.com/3431221/13621/v/450/depositphotos_136216036-stock-illustration-man-avatar-icon-hipster-character.jpg', 1, 50, 100, 2, 999666999, NOW(), 'Faro', TRUE);

-- Insert random items
INSERT INTO items (`title`, `date`, `description`, `price`, `old_price`, `image`, `location`, `condition`, `is_available`, `owner_id`, `category_id`, `product_id`)
VALUES
    ('Livro', NOW(), 'Exemplo de um livro com capa dura, praticamente como novo. Não aceito trocas. Preço não negociável', 9.00, NULL, 'https://static.portugues.com.br/2020/07/livro-aberto.jpg', 'Aveiro', 'Usado', TRUE, 1, 1, 1),
    ('Calças de ganga', NOW(), 'Calças de ganga a estrear de tamanho M. Nunca foram usadas e ainda têm a etiqueta. Preço negociável. Entrego em mãos na zona de Gouveia.', 15.30, NULL, 'https://traquinaskids.pt/42985-large_default/calca-ganga-indigo-tiffosi.jpg', 'Gouveia', 'Novo', TRUE, 1, 1, 1),
    ('Cadeira de escritório', NOW(), 'Cadeira de escritório/de executivo. Confortável, pouco usada e pronta a receber um novo dono. Aceito propostas.', 60.50, NULL, 'https://1616346425.rsc.cdn77.org/temp/1615370739_6c9e04b9c72b4bcb5c03e722bff91b05.jpg', 'Viseu', 'Usado', TRUE, 1, 1, 1),
    ('Smartphone', NOW(), 'Sem descrição.', 200.98, NULL, 'https://www.hisense.pt/wp-content/uploads/2019/06/H30-ICE-BLUE-1-2.png', 'Braga', 'Novo', TRUE, 1, 2, 2),
    ('Óculos de sol', NOW(), 'Óculos de sol escuros da marca XPTO com proteção UV. Usados mas sem marcas de uso nem riscos.', 15.00, 16.99, 'https://magento.opticalia.com/media/catalog/product/cache/e4be6767ec9b37c1ae8637aee2f57a6a/v/t/vts560910.png', 'Guarda', 'Novo', TRUE, 2, 1, 1),
    ('Mala de viagem', NOW(), 'Mala de viagem tipo trolley com peso de 2kg e dimensões 80x35cm e altura de 20cm. Como nova, nunca fui usada. Ainda com etiqueta e fatura.', 99.99, 90.99, 'https://img.joomcdn.net/57e3cb5b80a268ab3c8c28d13f7bcac81f21cc71_1024_1024.jpeg', 'Santarém', 'Novo', TRUE, 3, 2, 2);
