
# vsphere datacenter name
vsphere_datacenter      = "sboweLab"

# name or IP of the ESXi host
vsphere_host         = "esx1.int.sentania.net"

# vsphere network
vsphere_network         = "VLAN2500 172.25.0.0_24"

# vsphere datastore
vsphere_datastore       = "esx1-local"

# cloud_init files for unattended configuration for Ubuntu
cloudinit_userdata      = "./http/user-data"
cloudinit_metadata      = "./http/meta-data"

# final clean up script
shell_scripts           = ["./setup/setup.sh"]

# SSH username (created in user-data. If you change it here the please also adjust in ./html/user-data)
ssh_username            = "labuser"

# SSH password (created in autounattend.xml. If you change it here the please also adjust in ./html/user-data)
ssh_password            = "VMware123!"