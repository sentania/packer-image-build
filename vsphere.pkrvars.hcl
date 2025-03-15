##################################################################################
# VARIABLES
##################################################################################

# Credentials

vcenter_username                = "administrator@vsphere.local"
vcenter_password                = "superSecretPassword"

# vSphere Objects

vcenter_insecure_connection     = true
vcenter_server                  = "vcenter.int.sentania.net"
vcenter_datacenter              = "sboweLab"
vcenter_cluster                    = "192.168.110.111"
vcenter_datastore               = "storage-iscsi-0"
vcenter_network                 = "VLAN2601 172.26.1.0_24"
vcenter_folder                  = "Templates"

# ISO Objects
iso_path                        = "[Datastore2_NonSSD] /packer_cache/ubuntu-22.04.3-live-server-amd64.iso"
