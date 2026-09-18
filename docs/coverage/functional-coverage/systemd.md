# systemd 功能测试覆盖详情

共 **36** 个测试用例，**114** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| systemd | test_systemd_systemctl_service_and_system_management | systemctl version |
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
| systemd | test_systemd_journalctl_journal_query | journalctl version |
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
| systemd | test_systemd_systemdanalyze_system_profiling | systemd-analyze version |
| | | systemd-analyze time: boot time |
| | | systemd-analyze security |
| systemd | test_systemd_hostnamectl_hostname_management | hostnamectl version |
| | | hostnamectl status: system info |
| | | hostnamectl hostname: current name |
| | | hostnamectl --static |
| | | hostnamectl --transient |
| | | hostnamectl --pretty |
| | | hostnamectl chassis |
| systemd | test_systemd_localectl_locale_management | localectl version |
| | | localectl status: locale info |
| | | localectl list-locales |
| systemd | test_systemd_timedatectl_timedate_management | timedatectl version |
| | | timedatectl status: time info |
| | | timedatectl show: all properties |
| | | timedatectl list-timezones |
| | | timedatectl show-timesync |
| systemd | test_systemd_loginctl_login_management | loginctl version |
| | | loginctl list-sessions |
| | | loginctl list-users |
| | | loginctl show-session |
| | | loginctl show-user |
| | | loginctl user-status |
| systemd | test_systemd_systemddetectvirt | systemd-detect-virt: detect VM |
| | | systemd-detect-virt -q: quiet mode |
| | | systemd-detect-virt -c: container only |
| | | systemd-detect-virt -v: VM only |
| | | systemd-detect-virt -r: chroot only |
| systemd | test_systemd_systemdcgls_cgroup_listing | systemd-cgls: cgroup tree |
| | | systemd-cgls -k: kernel threads |
| | | systemd-cgls --no-pager |
| systemd | test_systemd_systemdcgtop_cgroup_top | systemd-cgtop -b: batch mode |
| systemd | test_systemd_systemdtmpfiles | systemd-tmpfiles version |
| | | systemd-tmpfiles --cat-config |
| systemd | test_systemd_busctl_dbus_introspection | busctl version |
| | | busctl list: list services |
| | | busctl status: bus status |
| | | busctl tree: object tree |
| | | busctl introspect |
| systemd | test_systemd_systemdrun | systemd-run version |
| | | systemd-run --user --scope |
| systemd | test_systemd_systemdcat | systemd-cat: pipe to journal |
| | | systemd-cat version |
| systemd | test_systemd_systemdnotify | systemd-notify version |
| | | systemd-notify help |
| systemd | test_systemd_systemdpath | systemd-path: all paths |
| | | systemd-path: specific path |
| | | systemd-path --suffix |
| | | systemd-path help |
| systemd | test_systemd_systemdescape | systemd-escape: basic escape |
| | | systemd-escape --path: path escape |
| | | systemd-escape -u: unescape |
| | | systemd-escape --suffix |
| | | systemd-escape --template |
| systemd | test_systemd_systemdmachineidsetup | systemd-machine-id-setup help |
| | | systemd-machine-id-setup: check machine-id |
| systemd | test_systemd_coredumpctl | coredumpctl version |
| | | coredumpctl list: list dumps |
| | | coredumpctl info |
| systemd | test_systemd_systemddelta | systemd-delta help |
| | | systemd-delta: show overrides |
| systemd | test_systemd_systemdid128 | systemd-id128 show: show IDs |
| | | systemd-id128 new: generate ID |
| systemd | test_systemd_systemdinhibit | systemd-inhibit help |
| | | systemd-inhibit --list |
| systemd | test_systemd_systemdacpower | systemd-ac-power: check power |
| systemd | test_systemd_systemdaskpassword | systemd-ask-password help |
| systemd | test_systemd_systemdcreds | systemd-creds help |
| systemd | test_systemd_systemdsocketactivate | systemd-socket-activate help |
| systemd | test_systemd_power_management_commands | $cmd help |
| systemd | test_systemd_systemdfirstboot | systemd-firstboot help |
| systemd | test_systemd_systemdstdiobridge | systemd-stdio-bridge help |
| systemd | test_systemd_oomctl | oomctl help |
| | | oomctl dump |
| systemd | test_systemd_systemctl_service_operations | systemctl try-restart |
| | | systemctl reload-or-restart |
| | | systemctl reset-failed |
| | | systemctl daemon-reload |
| systemd | test_systemd_run0_privilege_escalation | run0 help |
| systemd | test_systemd_systemdmount | systemd-mount help |
| systemd | test_systemd_systemdsysext | systemd-sysext help |
| systemd | test_systemd_systemdconfext | systemd-confext help |
| systemd | test_systemd_error_handling | systemctl: invalid command |
| | | journalctl: invalid option |
| | | hostnamectl: invalid option |
