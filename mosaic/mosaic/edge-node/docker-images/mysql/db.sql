DROP DATABASE IF EXISTS `sdn_db`;
CREATE DATABASE `sdn_db`;
use `sdn_db`;

GRANT ALL PRIVILEGES ON sdn_db.* TO 'sdn'@'%' IDENTIFIED BY 'mn962lf8sm49sh4k1';
FLUSH PRIVILEGES;

CREATE TABLE `devices` (
    `deviceId` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(256) NOT NULL UNIQUE,
    `secret` varchar(256) NOT NULL,
    `ip` varchar(16),
    PRIMARY KEY (`deviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `users` (
    `userId` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(256) NOT NULL UNIQUE,
    `password` varchar(128) NOT NULL,
    `role` int(11) NOT NULL DEFAULT '0',
    PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `users` (`name`, `password`, `role`) VALUES ("admin", "", 100);

CREATE TABLE `groups` (
    `groupId` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(32) NOT NULL UNIQUE,
    PRIMARY KEY (`groupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    
INSERT INTO `groups` (`name`) VALUES ("combat");
    
CREATE TABLE `groupPermissions` (
    `groupId` int(11) NOT NULL,
    `userId` int(11) NOT NULL,
    `role` INT(11) NOT NULL,
    CONSTRAINT `permission_groupId` FOREIGN KEY (`groupId`) REFERENCES `groups` (`groupId`),
    CONSTRAINT `permission_userId` FOREIGN KEY (`userId`) REFERENCES `users` (`userId`),
    CONSTRAINT `dupl` UNIQUE (`groupId`, `userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `groupDevices` (
    `groupId` int(11) NOT NULL,
    `deviceId` int(11) NOT NULL,
    CONSTRAINT `group_groupId` FOREIGN KEY (`groupId`) REFERENCES `groups` (`groupId`),
    CONSTRAINT `group_deviceId` FOREIGN KEY (`deviceId`) REFERENCES `devices` (`deviceId`),
    CONSTRAINT `dupl` UNIQUE (`groupId`, `deviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `units` (
    `unitId` int(11) NOT NULL AUTO_INCREMENT,
    `groupId` int(11) NOT NULL,
    `name` varchar(32) NOT NULL UNIQUE,
    `bandwidthLimit` varchar(32),
    CONSTRAINT `unit_groupId` FOREIGN KEY (`groupId`) REFERENCES `groups` (`groupId`),
    PRIMARY KEY (`unitId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `membership` (
    `unitId` int(11) NOT NULL,
    `deviceId` int(11) NOT NULL,
    CONSTRAINT `unit_Id` FOREIGN KEY (`unitId`) REFERENCES `units` (`unitId`),
    CONSTRAINT `unit_deviceId` FOREIGN KEY (`deviceId`) REFERENCES `devices` (`deviceId`),
    CONSTRAINT `dupl-mem` UNIQUE (`unitId`, `deviceId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `policies` (
    `policyId` int(11) NOT NULL AUTO_INCREMENT,
    `source` int(11) NOT NULL,
    `destination` int(11) NOT NULL,
    `limits` int(11) NOT NULL,
    PRIMARY KEY (`policyId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
