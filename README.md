

# Isilon-Network-Checks /  isilon extended network interface 

For DELL/EMC Isilon OneFS NAS , [ isilon extended network interface ]  output. 
```
Provides an extended view of 'isi network interface list' output. - Making Your Checks Easier ! 
Adds + 'Ping Status ResponseTime/loss' , 'SMB Share Access Check' , 'Display the right Pool for the IP' ( which is Buggy in isi )
```
Its well known that, 'isi network interface list ' is  buggy in its representation - the IP Coloumn and Corresponding 'poolname' . 
Aim of this tool is to have a One Window Check for an entire Isilon NAS cluster from a network point of view. 
This tool along with other healthchecks (ping,RTLoss, SMBShareChecks ), will also get rid of the Bug. 
To maintain transperency to the user, all representation at maintained inline with a raw command output. 



## Getting Started


Adds new Columns for health Check: [ ping Response time, SMB Share Accessibility , isiBufFix_poolName ]


 

### Prerequisites

1) Passwordless login for the ssh user[admin/(variable username)] to remote isilon to fetch data. 

For SMB Share Check: [ Pre-Requisite ]

     A unique Share for SMB Test in all SMB Pools: '//TestShareAccess' 
     
    'mysmbcfg.cfg' contains the username,password and Domain name for the SMB Share Access validations.
    
     By default - Only Pools With "SMB" String Matches are only Considered.



## Running the tests

Explain how to run the script:
```
python isilon_extended_interface.py
Cluster Name?: mycluster.mydomain
Collecting Data:  mycluster.mydomain isi network interface list  => Done. 16321 lines received
Collecting Data:  mycluster.mydomain isi network pools list -v  => Done. 14342 lines received
Fetching IPs configured::98 ip's
Triggering Ping for 98 ip's:  Done
Triggering SmbClient ShareCheck for SMB pool ip's matching names ['smb', 'worm']:  done
Generating Extended 'isi network interface' output
prints  RedColour if NOK for Ping/ShareCheck result


LNN  Name         Status     Owners                                              IP Addresses    Ping_RTT/(%Ploss) SmbClient-ShareCheck  isiBugfix:NetPool
-----------------------------------------------------------------------------------------------
1    10gige-1     Up         -                                                   -
1    10gige-2     Up         -                                                   -
1    10gige-agg-1 Up         groupnet0.subnet_10gb_prd_z1.pool_nfsxx_10gb_prd_z1 11.123.xxx.91   0.155ms(0%)       skip                  Pool_10g_Av
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xx.138   0.191ms(0%)       skip                  pool_10g_rep_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.28   0.171ms(0%)       skip                  pool_nfsxx_10gb_prd_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.30   0.180ms(0%)       skip                  pool_nfsxx_10gb_prd_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.38   0.126ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.51   0.129ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
                             groupnet0.subnet_10gb_rep_z1.pool_10g_rep_c2        11.123.xyz.83   0.161ms(0%)       OK[Active]            pool_smbxx_10gb_prd_z1
                             groupnet0.Subnet_10G_AV_z1.Pool_10g_Av_z1           11.123.xyz.91   0.150ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
																    
1    ext-1        Up         -                                                   -
1    ext-2        Up         -                                                   -
2    10gige-1     Up         -                                                   -
2    10gige-2     Up         -                                                   -
2    10gige-agg-1 Up         groupnet0.subnet_10gb_prd_z1.pool_nfsxx_10gb_prd_z1 11.123.xxx.92   0.142ms(0%)       skip                  Pool_10g_Av_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xx.139   0.141ms(0%)       skip                  pool_10g_rep_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.15   0.166ms(0%)       skip                  pool_nfsxx_10gb_prd_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.23   0.177ms(0%)       skip                  pool_nfsxx_10gb_prd_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.44   0.153ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
                             groupnet0.subnet_10gb_prd_z1.pool_smbxx_10gb_prd_z1 11.123.xyz.52   0.163ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
                             groupnet0.subnet_10gb_rep_z1.pool_10g_rep_z1        11.123.xyz.84   0.165ms(0%)       OK[Active]            pool_smbxx_10gb_prd_z1
                             groupnet0.Subnet_10G_AV_z1.Pool_10g_Av_z1           11.123.xyz.92   0.169ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
                                                                                 11.123.xyz.122  0.167ms(0%)       NOK[Failed]!          pool_smbxx_10gb_prd_z1
2    ext-1        Up         -                                                   -
2    ext-2        Up         -                                                   -
3    10gige-1     No Carrier -                                                   -
3    10gige-2     No Carrier -                                                   -


```



## Built With

* Python 3

## Authors

* **Vipin Kumar G** - *Initial work* - (https://github.com/vkg23)
