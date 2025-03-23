#!/usr/bin/env python3
import os
import sys
import requests
from vmware.vapi.vsphere.client import create_vsphere_client

def main():
    if len(sys.argv) != 3:
        print("Usage: sync_vsphere_libraries_sdk.py <vSphereUSERNAME> <vSpherePASSWORD>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    # The vCenter list file is assumed to be at inputs/vcenterlist.txt
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
            # Create a vSphere client using the SDK. This handles session creation, etc.
            client = create_vsphere_client(server=vcenter, username=username, password=password, session=session)
        except Exception as e:
            print(f"Error connecting to vCenter {vcenter}: {e}")
            continue

        try:
            # List the subscribed libraries. This is equivalent to the GET call.
            libraries = client.content.subscribed_library.list()
            if not libraries:
                print(f"No subscribed libraries found on {vcenter}.")
                continue
        except Exception as e:
            print(f"Error listing subscribed libraries on {vcenter}: {e}")
            continue

        for library_id in libraries:
            print(f"Syncing library: {library_id}")
            try:
                # This calls the sync method from the SDK which under the hood does the appropriate API call.
                client.content.subscribed_library.sync(library_id)
                print(f"Library {library_id} synchronized successfully.")
            except Exception as e:
                print(f"Error syncing library {library_id} on {vcenter}: {e}")

if __name__ == "__main__":
    main()
