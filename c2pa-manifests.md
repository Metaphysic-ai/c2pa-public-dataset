# Metaphysic C2PA Manifests

Sample script and datasets for demo purposes.

# Table of Contents

- [1. Install](#1-install)
    - [1.1. Install - Poetry](#11-install---poetry)
    - [1.2. Install - Dependencies](#12-install--dependencies)
- [2. Usage](#2-usage)
    - [2.1. Modules](#21-modules)


# 1. Install <a name=install></a>

### The code was tested with:
**If running manually:**
- Ubuntu 22.04.4 LTS
- Python 3.9.13
- Poetry 1.5.1



## 1.1 Install - Poetry
```shell
pip install poetry
```


## 1.2 Install - Dependencies

```shell
poetry install
```


# 2. Usage

## 2.1. Modules

- `c2pa_sign`: sign files, manifests and add metadata
- `c2pa_extract`: extracts the manifest in json format from previously signed and valid c2pa files
