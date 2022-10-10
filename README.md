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
git apply boptest-proxy.patch
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
docker exec -it project1-boptest-bacnet-cli-1 python ReadAllProperties.py 10.0.0.8 analogValue 63
```
