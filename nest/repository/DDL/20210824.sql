ALTER TABLE `t_user` ADD COLUMN `activate_code` CHAR(16) NOT NULL AFTER `id`;
ALTER TABLE `t_user` ADD COLUMN `status` INT NOT NULL AFTER `salt`;
