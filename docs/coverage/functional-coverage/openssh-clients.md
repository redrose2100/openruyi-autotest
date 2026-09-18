# openssh-clients 功能测试覆盖详情

共 **7** 个测试用例，**19** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| openssh-clients | test_openssh_clients_ssh_version_and_help | ssh version |
| | | ssh -Q key: supported keys |
| | | ssh -Q cipher: ciphers |
| | | ssh -Q mac: MACs |
| | | ssh -Q kex: key exchange |
| openssh-clients | test_openssh_clients_ssh_connection_dryrun | ssh -G: print config |
| | | ssh -T: disable PTY |
| | | ssh -v: verbose |
| openssh-clients | test_openssh_clients_sshkeygen_via_openssh | Generate test key |
| openssh-clients | test_openssh_clients_sshagent | ssh-add: list keys |
| | | ssh-add: add key |
| | | ssh-add: verify key added |
| | | ssh-add -L: list public keys |
| | | ssh-add -d: remove key |
| openssh-clients | test_openssh_clients_sshkeyscan | ssh-keyscan: scan localhost |
| | | ssh-keyscan -t rsa |
| | | ssh-keyscan -t ecdsa |
| openssh-clients | test_openssh_clients_sftp | sftp: help command |
| openssh-clients | test_openssh_clients_scp | scp version |
