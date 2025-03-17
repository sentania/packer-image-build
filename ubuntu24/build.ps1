packer build -force -var-file="ubuntu24.pkrvars.hcl" `
  -var='vsphere_guest_os_type=ubuntu64Guest' `
  -var='vsphere_vm_name=ubuntu-24-temp' `
  -var='template_library_Name=ubuntu24' `
  -var='content_library_destination=vcenter.int.sentania.net' .