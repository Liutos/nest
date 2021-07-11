ALTER TABLE `t_plan` ADD COLUMN `status` INT NOT NULL COMMENT '计划的状态' AFTER `repeat_type`;
ALTER TABLE `t_task` ADD COLUMN `status` INT NOT NULL COMMENT '任务的状态' AFTER `brief`;
