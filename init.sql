DROP DATABASE IF EXISTS blog_site;

CREATE DATABASE blog_site CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE blog_site;

CREATE USER IF NOT EXISTS 'blog_dba'@'%' IDENTIFIED BY 'blog_dba';

GRANT SELECT, INSERT, UPDATE, DELETE ON blog_site.* TO 'blog_dba'@'%';

CREATE TABLE IF NOT EXISTS `User`
(
    `uid`             BIGINT       NOT NULL AUTO_INCREMENT,
    `name`            VARCHAR(255) NOT NULL UNIQUE,
    `nickname`        VARCHAR(255) UNIQUE,
    `email`           VARCHAR(255) NOT NULL UNIQUE,
    `hashed_password` VARCHAR(255) NOT NULL,
    `salt`            VARCHAR(255) NOT NULL,
    `admin`           TINYINT(1) DEFAULT 0,
    `avatar`          VARCHAR(255),
    `created_at`      BIGINT,
    PRIMARY KEY (`uid`)
) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `Blog`
(
    `bid`              BIGINT       NOT NULL AUTO_INCREMENT,
    `user_id`          BIGINT       NOT NULL,
    `title`            VARCHAR(255) NOT NULL,
    `summary`          VARCHAR(255) NOT NULL,
    `content_path`     TEXT         NOT NULL,
    `created_at`       BIGINT,
    `last_modified_at` BIGINT,
    PRIMARY KEY (`bid`),
    FOREIGN KEY (`user_id`) REFERENCES `User` (`uid`)
) ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `Comment`
(
    `cid`        BIGINT       NOT NULL AUTO_INCREMENT,
    `blog_id`    BIGINT       NOT NULL,
    `user_id`    BIGINT       NOT NULL,
    `content`    VARCHAR(255) NOT NULL,
    `created_at` BIGINT,
    PRIMARY KEY (`cid`),
    FOREIGN KEY (`blog_id`) REFERENCES `Blog` (`bid`),
    FOREIGN KEY (`user_id`) REFERENCES `User` (`uid`)
) ENGINE = InnoDB;

INSERT INTO `User`
(`uid`, `name`, `nickname`, `email`, `hashed_password`, `salt`, `admin`, `created_at`)
VALUES (28800, 'admin', 'admin', 'admin@example.com',
        '5bcf0d9ec60eefacf23029e6c34e01cdd49b42eded878b20bf9d5519e4386d03', 'm|Z5LG8fox9cVKGm', 1, 1704070800);
