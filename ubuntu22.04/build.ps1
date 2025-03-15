packer build -var-file="ubuntu-2204.pkrvars.hcl" `
  -var='vsphere_guest_os_type=ubuntu64Guest' `
  -var='vsphere_vm_name=ubuntu-2205-temp' .