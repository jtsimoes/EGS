-- Create the ResellrMessages database
DROP DATABASE IF EXISTS ResellrMessages;

CREATE DATABASE ResellrMessages;

-- Create new user and grant permissions
CREATE OR REPLACE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON ResellrMessages.* TO 'user'@'localhost';

-- Switch to the ResellrMessages database
USE ResellrMessages;

-- Create the ConvTable table
CREATE TABLE ConvTable (
  id INT NOT NULL AUTO_INCREMENT,
  userId1 INT NOT NULL,
  userName1 VARCHAR(255) NOT NULL,
  userHidden1 BOOLEAN NOT NULL,
  userId2 INT NOT NULL,
  userName2 VARCHAR(255) NOT NULL,
  userHidden2 BOOLEAN NOT NULL,
  lastMessage VARCHAR(255),
  PRIMARY KEY (id)
);

-- Insert data into the ConvTable table
INSERT INTO ConvTable (userId1, userName1, userHidden1, userId2, userName2, userHidden2, lastMessage)
VALUES
  (1, 'João Ferreira', false, 2, 'José Silva', false, 'Claro que sim!'),
  (3, 'Amélia Rodrigues', false, 1, 'João Ferreira', true, 'Até breve!'),
  (2, 'José Silva', false, 3, 'Amélia Rodrigues', false, 'Como está?');

-- Create the MsgTable table
CREATE TABLE MsgTable (
  id INT NOT NULL AUTO_INCREMENT,
  conversationId INT NOT NULL,
  senderId INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  content TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (conversationId) REFERENCES ConvTable(id)
);

-- Insert data into the MsgTable table
INSERT INTO MsgTable (conversationId, senderId, timestamp, content)
VALUES
  (1, 1, '2023-02-27 10:30:00', 'Bom dia, tudo bem?'),
  (1, 1, '2023-02-27 11:05:00', 'Estaria disposto a negociar o preço do artigo?'),
  (1, 2, '2023-02-27 11:15:00', 'Claro que sim!'),
  (2, 3, '2023-03-04 14:50:00', 'Boa tarde, estou interessado neste artigo!'),
  (2, 1, '2023-03-04 14:57:00', 'Ainda bem! Será possível discutir noutro local?'),
  (2, 3, '2023-03-04 15:20:00', 'Até breve!'),
  (3, 2, '2023-03-05 17:30:00', 'Boa tarde, o meu nome é José Silva.'),
  (3, 2, '2023-03-05 18:20:00', 'Como está?');

