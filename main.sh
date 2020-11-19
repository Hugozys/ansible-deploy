#!/usr/bin/bash

# copy all content from github workspace to home directory (including hidden files)
shopt -s dotglob nullglob
cp -r ${ANSIBLE_DIRECTORY}/* ~

cd ~

if [ -f "./requirements.yaml" ]
then
    ansible-galaxy collection install -r ./requirements.yaml
fi

cmd="ansible-playbook ${ANSIBLE_PLAYBOOK}"

# export additional environment variables
eval "$(exp envs)"

# pass extra variables if any
option="\"$(exp vars)\""
if [ -n "${option}" ]; then cmd="${cmd} -e ${option}"; fi

echo -e "${cmd}"
eval "${cmd}"

