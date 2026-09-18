# systemd 功能测试覆盖详情

共 **36** 个测试套，**114** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_systemd_systemctl_service_and_system_management | 15 cases | systemctl version |
| | | systemctl: list running services |
| | | systemctl: list targets |
| | | systemctl --all: all services |
| | | systemctl: list unit files |
| | | systemctl is-active: check service status |
| | | systemctl is-enabled: check enabled |
| | | systemctl is-failed: list failed units |
| | | systemctl status: service status |
| | | systemctl show: service properties |
| | | systemctl cat: show unit file |
| | | systemctl list-dependencies |
| | | systemctl list-sockets |
| | | systemctl list-timers |
| | | systemctl list-machines |
| test_systemd_journalctl_journal_query | 13 cases | journalctl version |
| | | journalctl -n: last entries |
| | | journalctl -b: current boot |
| | | journalctl --list-boots |
| | | journalctl -k: kernel messages |
| | | journalctl -o short: short format |
| | | journalctl -o json: json format |
| | | journalctl -o verbose |
| | | journalctl --disk-usage |
| | | journalctl --output=cat |
| | | journalctl -p err: error messages |
| | | journalctl --since |
| | | journalctl -q: quiet |
| test_systemd_systemdanalyze_system_profiling | 3 cases | systemd-analyze version |
| | | systemd-analyze time: boot time |
| | | systemd-analyze security |
| test_systemd_hostnamectl_hostname_management | 7 cases | hostnamectl version |
| | | hostnamectl status: system info |
| | | hostnamectl hostname: current name |
| | | hostnamectl --static |
| | | hostnamectl --transient |
| | | hostnamectl --pretty |
| | | hostnamectl chassis |
| test_systemd_localectl_locale_management | 3 cases | localectl version |
| | | localectl status: locale info |
| | | localectl list-locales |
| test_systemd_timedatectl_timedate_management | 5 cases | timedatectl version |
| | | timedatectl status: time info |
| | | timedatectl show: all properties |
| | | timedatectl list-timezones |
| | | timedatectl show-timesync |
| test_systemd_loginctl_login_management | 6 cases | loginctl version |
| | | loginctl list-sessions |
| | | loginctl list-users |
| | | loginctl show-session |
| | | loginctl show-user |
| | | loginctl user-status |
| test_systemd_systemddetectvirt | 5 cases | systemd-detect-virt: detect VM |
| | | systemd-detect-virt -q: quiet mode |
| | | systemd-detect-virt -c: container only |
| | | systemd-detect-virt -v: VM only |
| | | systemd-detect-virt -r: chroot only |
| test_systemd_systemdcgls_cgroup_listing | 3 cases | systemd-cgls: cgroup tree |
| | | systemd-cgls -k: kernel threads |
| | | systemd-cgls --no-pager |
| test_systemd_systemdcgtop_cgroup_top | 1 cases | systemd-cgtop -b: batch mode |
| test_systemd_systemdtmpfiles | 2 cases | systemd-tmpfiles version |
| | | systemd-tmpfiles --cat-config |
| test_systemd_busctl_dbus_introspection | 5 cases | busctl version |
| | | busctl list: list services |
| | | busctl status: bus status |
| | | busctl tree: object tree |
| | | busctl introspect |
| test_systemd_systemdrun | 2 cases | systemd-run version |
| | | systemd-run --user --scope |
| test_systemd_systemdcat | 2 cases | systemd-cat: pipe to journal |
| | | systemd-cat version |
| test_systemd_systemdnotify | 2 cases | systemd-notify version |
| | | systemd-notify help |
| test_systemd_systemdpath | 4 cases | systemd-path: all paths |
| | | systemd-path: specific path |
| | | systemd-path --suffix |
| | | systemd-path help |
| test_systemd_systemdescape | 5 cases | systemd-escape: basic escape |
| | | systemd-escape --path: path escape |
| | | systemd-escape -u: unescape |
| | | systemd-escape --suffix |
| | | systemd-escape --template |
| test_systemd_systemdmachineidsetup | 2 cases | systemd-machine-id-setup help |
| | | systemd-machine-id-setup: check machine-id |
| test_systemd_coredumpctl | 3 cases | coredumpctl version |
| | | coredumpctl list: list dumps |
| | | coredumpctl info |
| test_systemd_systemddelta | 2 cases | systemd-delta help |
| | | systemd-delta: show overrides |
| test_systemd_systemdid128 | 2 cases | systemd-id128 show: show IDs |
| | | systemd-id128 new: generate ID |
| test_systemd_systemdinhibit | 2 cases | systemd-inhibit help |
| | | systemd-inhibit --list |
| test_systemd_systemdacpower | 1 cases | systemd-ac-power: check power |
| test_systemd_systemdaskpassword | 1 cases | systemd-ask-password help |
| test_systemd_systemdcreds | 1 cases | systemd-creds help |
| test_systemd_systemdsocketactivate | 1 cases | systemd-socket-activate help |
| test_systemd_power_management_commands | 1 cases | $cmd help |
| test_systemd_systemdfirstboot | 1 cases | systemd-firstboot help |
| test_systemd_systemdstdiobridge | 1 cases | systemd-stdio-bridge help |
| test_systemd_oomctl | 2 cases | oomctl help |
| | | oomctl dump |
| test_systemd_systemctl_service_operations | 4 cases | systemctl try-restart |
| | | systemctl reload-or-restart |
| | | systemctl reset-failed |
| | | systemctl daemon-reload |
| test_systemd_run0_privilege_escalation | 1 cases | run0 help |
| test_systemd_systemdmount | 1 cases | systemd-mount help |
| test_systemd_systemdsysext | 1 cases | systemd-sysext help |
| test_systemd_systemdconfext | 1 cases | systemd-confext help |
| test_systemd_error_handling | 3 cases | systemctl: invalid command |
| | | journalctl: invalid option |
| | | hostnamectl: invalid option |
