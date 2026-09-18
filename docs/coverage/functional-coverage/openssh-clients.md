# openssh-clients 功能测试覆盖详情

共 **7** 个测试套，**19** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_openssh_clients_ssh_version_and_help | 5 cases | ssh version |
| | | ssh -Q key: supported keys |
| | | ssh -Q cipher: ciphers |
| | | ssh -Q mac: MACs |
| | | ssh -Q kex: key exchange |
| test_openssh_clients_ssh_connection_dryrun | 3 cases | ssh -G: print config |
| | | ssh -T: disable PTY |
| | | ssh -v: verbose |
| test_openssh_clients_sshkeygen_via_openssh | 1 cases | Generate test key |
| test_openssh_clients_sshagent | 5 cases | ssh-add: list keys |
| | | ssh-add: add key |
| | | ssh-add: verify key added |
| | | ssh-add -L: list public keys |
| | | ssh-add -d: remove key |
| test_openssh_clients_sshkeyscan | 3 cases | ssh-keyscan: scan localhost |
| | | ssh-keyscan -t rsa |
| | | ssh-keyscan -t ecdsa |
| test_openssh_clients_sftp | 1 cases | sftp: help command |
| test_openssh_clients_scp | 1 cases | scp version |
