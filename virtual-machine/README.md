# Virtual Machine Configuration

Because BACnet runs over UDP on a fixed port, it is necessary to use different (optionally virtual) machines to perform certain operations.

1. Install [Multipass](https://multipass.run/)
2. Download the vm configuration file:
    ```bash
    curl -O https://raw.githubusercontent.com/gtfierro/simulated-digital-twin/main/virtual-machine/vm-config.yaml
    ```
3. Run the following to start the vm
    ```bash
    multipass launch -n bacnet --cloud-init vm-config.yaml  --timeout 600 -d 20G -m 4G -c 2
    ```
4. Set up the simulated digital twin (this can take awhile because of the size of the repositories
    ```bash
    multipass exec bacnet ./setup-simulated-digital-twin.sh
    ```
5. Finally, you can start a shell on the VM and start the digital twin
   ```bash
   multipass shell bacnet
   # (inside the VM now)
   cd simulated-digital-twin
   make up
   ```
6. You can then inspect your network interfaces to get the subnet/gateway for your VM. Typically, if you run `multipass list`, the VM's IP should show up and will be on a `/24`:

   ```bash
   $ multipass list
   bacnet                  Running        10.47.35.39      Ubuntu 22.04 LTS
                                          172.17.0.1
                                          10.0.0.1
   # Here, you would use a setting of 10.47.35.1/24 for BACpypes.ini
   ```
