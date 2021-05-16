CREATE TABLE `t_location` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(10) NOT NULL COMMENT '地点名',
  `user_id` BIGINT NOT NULL COMMENT '创建者的ID',
  PRIMARY KEY (`id`)
);

ALTER TABLE `t_plan` ADD COLUMN `location_id` BIGINT COMMENT '计划生效的地点的ID' AFTER `duration`;