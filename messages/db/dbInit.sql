-- Create the ResselrMessages database
DROP DATABASE IF EXISTS ResselrMessages;
CREATE DATABASE ResselrMessages;

-- Switch to the ResselrMessages database
USE ResselrMessages;

-- Create the ConvTable table
CREATE TABLE ConvTable (
  id INT NOT NULL AUTO_INCREMENT,
  userId1 INT NOT NULL,
  userName1 VARCHAR(255) NOT NULL,
  userPicture1 VARCHAR(255) NOT NULL,
  userHidden1 BOOLEAN NOT NULL,
  userId2 INT NOT NULL,
  userName2 VARCHAR(255) NOT NULL,
  userPicture2 VARCHAR(255) NOT NULL,
  userHidden2 BOOLEAN NOT NULL,
  lastMessage VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

-- Insert data into the ConvTable table
INSERT INTO ConvTable (userId1, userName1, userPicture1, userHidden1, userId2, userName2, userPicture2, userHidden2, lastMessage)
VALUES
  (1, 'João Ferreira', 'NA', false, 2, 'José Silva', 'NA', false, 'Claro que sim!'),
  (3, 'Amélia Rodrigues', 'NA', false, 1, 'João Ferreira', 'NA', true, 'Até breve!'),
  (2, 'José Silva', 'NA', false, 3, 'Amélia Rodrigues', 'NA', false, 'Como está?');

-- Create the MsgTable table
CREATE TABLE MsgTable (
  id INT NOT NULL AUTO_INCREMENT,
  conversationId INT NOT NULL,
  senderId INT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `read` BOOLEAN NOT NULL,
  content TEXT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (conversationId) REFERENCES ConvTable(id)
);

-- Insert data into the MsgTable table
INSERT INTO MsgTable (conversationId, senderId, timestamp, `read`, content)
VALUES
  (1, 1, '2023-02-27 10:30:00', true, 'Bom dia, tudo bem?'),
  (1, 1, '2023-02-27 11:05:00', true, 'Estaria disposto a negociar o preço do artigo?'),
  (1, 2, '2023-02-27 11:15:00', false, 'Claro que sim!'),
  (2, 3, '2023-03-04 14:50:00', true, 'Boa tarde, estou interessado neste artigo!'),
  (2, 1, '2023-03-04 14:57:00', true, 'Ainda bem! Será possível discutir noutro local?'),
  (2, 3, '2023-03-04 15:20:00', true, 'Até breve!'),
  (3, 2, '2023-03-05 17:30:00', false, 'Boa tarde, o meu nome é José Silva.'),
  (3, 2, '2023-03-05 18:20:00', false, 'Como está?');

-- Create new user and grant permissions
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON ResselrMessages.* TO 'user'@'localhost';