ALTER TABLE `t_plan` ADD COLUMN `visible_hours` JSON AFTER `trigger_time`;
ALTER TABLE `t_plan` ADD COLUMN `visible_wdays` JSON AFTER `visible_hours`;
ALTER TABLE `t_plan` DROP COLUMN `exclude_hours`;
ALTER TABLE `t_plan` DROP COLUMN `exclude_wdays`;
