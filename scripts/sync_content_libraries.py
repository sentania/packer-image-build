#!/usr/bin/env python3
import os
import sys
import requests
from vmware.vapi.vsphere.client import create_vsphere_client
from com.vmware.content_client import SubscribedLibrary

def main():
    if len(sys.argv) != 3:
        print("Usage: sync_content_libraries_sdk.py <vSphereUSERNAME> <vSpherePASSWORD>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    # Assume the vCenter list is in inputs/vcenterlist.txt
    vcenter_file = os.path.join("inputs", "vcenterlist.txt")
    try:
        with open(vcenter_file, 'r') as f:
            vcenters = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading vCenter list file: {e}")
        sys.exit(1)

    for vcenter in vcenters:
        print(f"\nProcessing vCenter: {vcenter}")
        session = requests.session()
        session.verify = False  # Disable certificate verification if needed

        try:
            client = create_vsphere_client(server=vcenter, username=username, password=password, session=session)
        except Exception as e:
            print(f"Error connecting to vCenter {vcenter}: {e}")
            continue

        stub_config = client._stub_config  # Get the SDK stub configuration

        try:
            # Instantiate the SubscribedLibrary service for listing and syncing
            subscribed_library_service = SubscribedLibrary(stub_config)
        except Exception as e:
            print(f"Error initializing SubscribedLibrary service: {e}")
            continue

        try:
            # Use the SubscribedLibrary service's list() method
            library_ids = subscribed_library_service.list()
        except Exception as e:
            print(f"Error listing subscribed libraries on {vcenter}: {e}")
            library_ids = []

        if not library_ids:
            print(f"No subscribed libraries found on {vcenter}.")
            continue

        for library_id in library_ids:
            print(f"Syncing library: {library_id}")
            try:
                subscribed_library_service.sync(library_id)
                print(f"Library {library_id} synchronized successfully.")
            except Exception as e:
                print(f"Error syncing library {library_id} on {vcenter}: {e}")

if __name__ == "__main__":
    main()
