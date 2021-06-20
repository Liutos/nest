CREATE TABLE `t_keyword` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(1000) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `ix__content` (`content`(100))
);

CREATE TABLE `t_task_keyword` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `keyword_id` BIGINT NOT NULL,
  `task_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `ix__keyword_id` (`keyword_id`)
);