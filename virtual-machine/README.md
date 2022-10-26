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
