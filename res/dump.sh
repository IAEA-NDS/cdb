#!/bin/bash
current_date_time="`date +%Y%m%d%H%M`";
echo "Dumping cdb at $current_date_time";
mysqldump -p cdb > ~/backups/cdb-$current_date_time.mysql;
