# Isilon-Network-Checks
For DELL/EMC Isilon OneFS NAS , isilon extended network interface  output. 

This tool provides an extended view of 'isi network interface list' output.
Its well known that, 'isi network interface list ' is mostly buggy in its display - the IP Coloumn and Corresponding 'poolname' . 
This tool along with other healthchecks, will also find the right Poolname against each IP's . 

Tasks Performed by Script:
 1) Add new Columns for health Check: [ ping Response time, SMB Share Accessibility , isiBufFix_poolName ]

Input : provide the fqdn name of the cluster to be checked. 
mysmbcfg.cfg contains the username,password and Domain name for the SMB Share Access validations.

