## IPs to Remember

- `10.0.0.1`: the device hosting the BACnet objects for the simulation
- `10.0.0.7`: the device hosting the BACnet-boptest proxy
- `10.0.0.8`: the device hosting the BACnet cli

## Setup

Submodule stuff:

```bash
git submodule init
git submodule update --init --recursive
```

This may take a few minutes as the boptest repo is large

---

Apply patches to boptest-bacnet-proxy:

```bash
cd boptest-bacnet-proxy
git apply ../boptest-proxy.patch
cp ../Dockerfile.boptest-proxy Dockerfile
cp ../run.sh .
```

Apply patches to BOPtest:

```bash
cd project1-boptest
git apply ../boptest.patch
```

---

Build the containers

```bash
make build
```

---

Run the containers

```bash
make run
```

---

Execute commands from the `bacnet-cli` container

```bash
docker exec -it project1-boptest-bacnet-cli-1 python DiscoverDevices.py
docker exec -it project1-boptest-bacnet-cli-1 python ReadAllProperties.py 10.0.0.1 analogValue 63
```
