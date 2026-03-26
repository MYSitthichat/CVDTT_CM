-- SQL Script to create report_form table
-- This table stores information about generated report forms for lab orders

CREATE TABLE IF NOT EXISTS `report_form` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lab_order_id` int(11) NOT NULL,
  `location` varchar(500) DEFAULT '',
  `comment` text DEFAULT '',
  `state` int(11) NOT NULL DEFAULT 0,
  `status` int(11) NOT NULL DEFAULT 1,
  `recorder` int(11) DEFAULT 0,
  `approver` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `idx_lab_order_id` (`lab_order_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Add comments to columns
ALTER TABLE `report_form` 
  MODIFY COLUMN `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'เลขที่รายงาน (Report Number)',
  MODIFY COLUMN `dtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่สร้างรายงาน',
  MODIFY COLUMN `lab_order_id` int(11) NOT NULL COMMENT 'รหัส Lab Order',
  MODIFY COLUMN `location` varchar(500) DEFAULT '' COMMENT 'ที่อยู่ไฟล์ที่บันทึก',
  MODIFY COLUMN `comment` text DEFAULT '' COMMENT 'หมายเหตุ',
  MODIFY COLUMN `state` int(11) NOT NULL DEFAULT 0 COMMENT 'สถานะการทำงาน',
  MODIFY COLUMN `status` int(11) NOT NULL DEFAULT 1 COMMENT 'สถานะใช้งาน (1=active, 0=inactive)',
  MODIFY COLUMN `recorder` int(11) DEFAULT 0 COMMENT 'ผู้บันทึก (employee_id)',
  MODIFY COLUMN `approver` int(11) DEFAULT 0 COMMENT 'ผู้อนุมัติ (employee_id)';
