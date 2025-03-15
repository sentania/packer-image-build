# Name or IP of you vCenter Server
vsphere_server          = "vcenter.int.sentania.net"

# vsphere username
vsphere_username        = "administrator@vsphere.local"

# vsphere password
vsphere_password        = "guj34mp0w3R2win!"

# vsphere datacenter name
vsphere_datacenter      = "sboweLab"

# name or IP of the ESXi host
vsphere_cluster         = "nucCluster"

# vsphere network
vsphere_network         = "VLAN2500 172.25.0.0_24"

# vsphere datastore
vsphere_datastore       = "storage-iscsi-1"

# cloud_init files for unattended configuration for Ubuntu
cloudinit_userdata      = "./http/user-data"
cloudinit_metadata      = "./http/meta-data"

# final clean up script
shell_scripts           = ["./setup/setup.sh"]

# SSH username (created in user-data. If you change it here the please also adjust in ./html/user-data)
ssh_username            = "labuser"

# SSH password (created in autounattend.xml. If you change it here the please also adjust in ./html/user-data)
ssh_password            = "VMware1!"