packer build -force -var-file="ubuntu-22.pkrvars.hcl" `
  -var='vsphere_guest_os_type=ubuntu64Guest' `
  -var='vsphere_vm_name=ubuntu-22-temp' `
  -var='template_library_Name=ubuntu22' `
  -var='content_library_destination=vcenter.int.sentania.net' .