CREATE TABLE users(	
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	roll_no CHAR(7) NOT NULL UNIQUE,
	username VARCHAR(50) NOT NULL PRIMARY KEY,
	password VARCHAR(200) NOT NULL,
	email VARCHAR(50) NOT NULL UNIQUE);

CREATE TABLE department(
	d_id VARCHAR(10) NOT NULL PRIMARY KEY,
	d_name VARCHAR(200) NOT NULL);

CREATE TABLE post(
	p_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	url VARCHAR(512) NOT NULL UNIQUE,
	title TEXT NOT NULL,
	description LONGTEXT,
	thumb TEXT NOT NULL,
	counter BIGINT NOT NULL,
	PRIMARY KEY(p_id));

CREATE TABLE bookmark(
	read_status BIT NOT NULL,
	time_added datetime NOT NULL);


ALTER TABLE users ADD d_id VARCHAR(10) NOT NULL;
ALTER TABLE users ADD FOREIGN KEY ('d_id') REFERENCES department('d_id');

ALTER TABLE bookmark ADD username VARCHAR(50) NOT NULL;
ALTER TABLE bookmark ADD p_id BIGINT UNSIGNED NOT NULL;
ALTER TABLE bookmark ADD b_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE users ADD FOREIGN KEY ('username') REFERENCES users('username');
ALTER TABLE users ADD FOREIGN KEY ('p_id') REFERENCES post('p_id');

INSERT INTO department(d_id,d_name) VALUES('CO','Computer Science & Engineering'),('EC','Electronics & Communication Engineering'),('EE','Electrical & Electronics Engineering'),('ME','Mechanical Engineering'),('CH','Chemical Engineering'),('MN','Mining Engineering'),('MT','Metallurgical Engineering'),('IT','Information Technology'),('CV','Civil Engineering');
