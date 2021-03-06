# ansible-deploy docker action

![main pipeline](https://github.com/Hugozys/ansible-deploy/workflows/main%20pipeline/badge.svg?branch=master)
![push image](https://github.com/Hugozys/ansible-deploy/workflows/push%20image/badge.svg?branch=master)
![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/hugozzys/ansible-deploy/latest?label=Docker%20Image)

This action setups a docker container with ansible runtime installed. It is sufficient for my personal use to embed this action as part of the CD process of my application development pipeline.

## Inputs

### `directory`

**Optional** Path to the root directory of your ansible hierarchy. This acion assumes that everything used by ansible runtime will be put in this directory, including package, playbook, roles, group_vars, host_vars, etc.

**Default**  `.`

### `playbook`

**Optional** Path to the plabook you want the action to run.

**Default**  `playbook.yaml`.

When you explicitly specify your playbook path, you MUST put the playbook under the root directory, and the path you specify MUST be a relative path to the root directory.

For instance, say all your ansible code lives in `./Ansible` directory in your repository, and your playbook lives in `./Ansible/playbook/playbook.yaml`. You only need to pass `playbook/playbook.yaml` into this input paramater.

### `envvars`

**Optional** extra key value pairs you want to pass to the ansible environment. They will be set as environment variables of the container which can also be accessed by ansible playbook in runtime.

### `extvars`

**Optional** extra key value pairs you want to pass to the `ansible-playbook` command. These kv pairs will be passed as the value of option `--extra-vars` when executing `ansible-playbook` command.

### `ssh_key`

**Optional** private ssh key you use to connect to remote machine. You MUST pass this key unless you are deploying your application to the same machine where ansible is running, which seems useless since the VM where this action runs will be destroyed by github. (The key must be passed in via Github encrypted secret feature. DO NOT PASS IN PLAIN TEXT!)

### `ssh_key_file_name`

**Optional** you can specify you private ssh key file name by this parameter

**Default** `id_rsa`

### `verbose`

**Optional** define the verbosity level of output when running your playook. The options are `0`, `1`, `3`, `4`, corresponding to the number of `v` you can specify when you manually run playbook from shell.

**Default** `0`

## Example usage

```yaml
uses: Hugozys/ansible-deploy@master
# run ./playbook.yaml
```

```yaml
uses: Hugozys/ansible-deploy@master
with:
    directory:"./ansible"
    playbook:"deploy.yaml" # actual file lives in ./ansible/deploy.yaml
```

```yaml
uses: Hugozys/ansible-deploy@master
with:
    directory:"./ansible"
    playbook:"deploy.yaml" # actual file lives in ./ansible/artifact/app.zip
    extvars:|
        package=artifact/app.zip
        username=hugozzys
    envvars:|
        API_TOKEN:fake-token
```

```yaml
uses: Hugozys/ansible-deploy@master
with:
    directory:"./ansible"
    playbook:"deploy.yaml"
    ssh_key: ${{secrets.SSH_KEY}}
    ssh_key_file_name: secret_id_rsa
    verbose: "4"
```

### NOTE

- This action also supports installing third party dependencies. Namely you want to use community collection, you specify them in the `requirements.txt` file which MUST be placed underneath your ansible root directory.

- Currently the action doesn't support expclitly passing host file into `ansible-playbook`. You need to create an `inventory` directory underneath your ansible root directory and put your host file there. The playbook will read all the files defined in that directory. For instance, if your root directory is `./ansible`, create `./ansible/inventory` and your `host` file will be `./ansible/inventory/host`

### TODO

- [X] Move away from bash
- [X] Support connect to remote
- [ ] Add support for explicit inventory
- [ ] Add more tests into workflow
