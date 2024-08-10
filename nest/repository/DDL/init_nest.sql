DROP TABLE IF EXISTS `t_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_keyword` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `content` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix__content` (`content`(100))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `t_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_location` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(10) NOT NULL COMMENT '地点名',
  `user_id` bigint(20) NOT NULL COMMENT '创建者的ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `t_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_plan` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `crontab` CHAR(16) DEFAULT '' COMMENT 'crontab 风格的执行周期',
  `duration` int(11) DEFAULT '0' COMMENT '持续时长',
  `location_id` bigint(20) DEFAULT NULL COMMENT '计划生效的地点的ID',
  `task_id` int(11) NOT NULL COMMENT '该计划所属的任务',
  `location` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '能够执行该任务的地点',
  `repeat_interval` int(11) DEFAULT NULL COMMENT '配合“重复类型”，计算出下一次的触发时间',
  `repeat_type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '表示这一次执行完任务后，下一次的触发时间如何计算',
  `status` int(11) NOT NULL COMMENT '计划的状态',
  `trigger_time` datetime NOT NULL COMMENT '需要执行任务的时间',
  `visible_hours` json DEFAULT NULL,
  `visible_wdays` json DEFAULT NULL,
  `ctime` datetime NOT NULL,
  `mtime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_task_id` (`task_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `t_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_task` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '创建该任务的用户的ID',
  `brief` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '对所要做的事情的简短描述',
  `detail` text COLLATE utf8mb4_bin COMMENT '任务的详情',
  `status` int(11) NOT NULL COMMENT '任务的状态',
  `ctime` datetime NOT NULL,
  `mtime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `t_task_keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_task_keyword` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `keyword_id` bigint(20) NOT NULL,
  `task_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix__keyword_id` (`keyword_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `t_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `activate_code` char(16) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用于登录的邮箱',
  `nickname` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '昵称',
  `password_hash` char(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '原始密码和“盐”一起用哈希算法计算出的哈希值',
  `salt` char(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '参与密码哈希计算的随机值',
  `status` int(11) NOT NULL,
  `ctime` datetime NOT NULL,
  `mtime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ux_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;
