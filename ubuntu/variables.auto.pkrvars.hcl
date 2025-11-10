
# vsphere datacenter name
vsphere_datacenter      = "vcf-lab-mgmt01-dc01"

# name or IP of the ESXi host
vsphere_host            = "esx1.int.sentania.net"

# vsphere network
vsphere_network         = "vcf-lab-mgmt01-cl01-vds01-pg-vm-mgmt"

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

ovf = true