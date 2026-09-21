#!/usr/bin/env python3
"""
Coverage analysis script for pkgs functional tests.
Analyzes each package's test coverage: commands, parameters, and functional areas.
"""
import os
import re
import json
import sys
from pathlib import Path
from collections import defaultdict

PKGS_DIR = Path(r"E:\code\openruyi-autotest\tests\functional\pkgs")

# Known command lists for key packages (verified from actual RPM package contents)
# Format: package_name -> list of (command_or_feature, category)
PACKAGE_COMMANDS = {
    "coreutils": [
        # File operations
        ("cp", "file_copy_move"), ("mv", "file_copy_move"), ("rm", "file_copy_move"),
        ("rmdir", "file_copy_move"), ("install", "file_copy_move"),
        ("mkdir", "directory_creation"), ("touch", "file_creation"),
        ("ln", "links"), ("link", "links"), ("unlink", "links"), ("readlink", "links"),
        # File viewing
        ("cat", "file_viewing"), ("tac", "file_viewing"), ("nl", "file_viewing"),
        ("head", "file_viewing"), ("tail", "file_viewing"), ("od", "file_viewing"),
        # Text processing
        ("sort", "text_processing"), ("uniq", "text_processing"),
        ("cut", "text_processing"), ("tr", "text_processing"),
        ("paste", "text_processing"), ("comm", "text_processing"),
        ("join", "text_processing"), ("fmt", "text_processing"),
        ("fold", "text_processing"), ("expand", "text_processing"),
        ("unexpand", "text_processing"),
        # Checksums
        ("cksum", "checksums"), ("md5sum", "checksums"), ("sha1sum", "checksums"),
        ("sha224sum", "checksums"), ("sha256sum", "checksums"),
        ("sha384sum", "checksums"), ("sha512sum", "checksums"),
        ("b2sum", "checksums"), ("sum", "checksums"),
        # Conditions
        ("true", "boolean"), ("false", "boolean"), ("test", "boolean"), ("[", "boolean"),
        # Environment
        ("env", "environment"), ("printenv", "environment"),
        ("date", "environment"), ("printf", "environment"),
        # System info
        ("uname", "system_info"), ("who", "system_info"), ("whoami", "system_info"),
        ("id", "system_info"), ("groups", "system_info"), ("users", "system_info"),
        ("logname", "system_info"), ("hostname", "system_info"),
        # File operations
        ("dd", "file_operations"), ("truncate", "file_operations"),
        ("shred", "file_operations"), ("sync", "file_operations"),
        # Counting
        ("wc", "counting"), ("du", "counting"), ("df", "counting"), ("stat", "counting"),
        # Path operations
        ("basename", "path"), ("dirname", "path"), ("pwd", "path"),
        ("realpath", "path"), ("mktemp", "path"),
        # Permissions
        ("chmod", "permissions"), ("chown", "permissions"), ("chgrp", "permissions"),
        # Process control
        ("nice", "process"), ("nohup", "process"), ("stdbuf", "process"),
        # Flow control
        ("sleep", "flow"), ("timeout", "flow"), ("yes", "flow"),
        # Redirection
        ("tee", "redirection"),
        # Split
        ("split", "split"), ("csplit", "split"),
        # Special
        ("stty", "special"), ("pathchk", "special"), ("tsort", "special"),
        ("ptx", "special"), ("dircolors", "special"),
        # Encoding
        ("base32", "encoding"), ("base64", "encoding"), ("basenc", "encoding"),
        # Numbers
        ("seq", "numbers"), ("factor", "numbers"), ("shuf", "numbers"),
        ("numfmt", "numbers"),
        # Listing
        ("ls", "listing"), ("dir", "listing"), ("vdir", "listing"),
        ("echo", "output"),
    ],
    "grep": [
        ("grep", "basic"), ("egrep", "extended"), ("fgrep", "fixed"),
        ("-E", "extended_regex"), ("-F", "fixed_strings"), ("-G", "basic_regex"),
        ("-P", "perl_regex"),
        ("-i", "case_insensitive"), ("-v", "invert_match"),
        ("-c", "count"), ("-n", "line_numbers"),
        ("-l", "file_listing"), ("-L", "file_listing_no_match"),
        ("-o", "only_matching"), ("-q", "quiet"),
        ("-r", "recursive"), ("-R", "recursive_deref"),
        ("-w", "word_match"), ("-x", "line_match"),
        ("-A", "context_after"), ("-B", "context_before"), ("-C", "context"),
        ("-e", "multiple_patterns"), ("-f", "pattern_file"),
        ("-H", "with_filename"), ("-h", "no_filename"),
        ("-m", "max_count"), ("--color", "color_output"),
        ("-s", "silent_errors"),
    ],
    "tar": [
        ("tar", "basic"),
        ("-c", "create"), ("-x", "extract"), ("-t", "list"), ("-r", "append"),
        ("-u", "update"), ("--delete", "delete"),
        ("-f", "file"), ("-v", "verbose"), ("-z", "gzip"),
        ("-j", "bzip2"), ("-J", "xz"), ("--zstd", "zstd"),
        ("--lzma", "lzma"), ("--lzip", "lzip"),
        ("-C", "change_dir"), ("--strip-components", "strip"),
        ("--exclude", "exclude"), ("--exclude-from", "exclude_file"),
        ("--wildcards", "wildcard"),
        ("--listed-incremental", "incremental"), ("--diff", "diff"),
        ("--preserve-permissions", "preserve"), ("--same-owner", "owner"),
        ("--transform", "transform"), ("--xform", "transform"),
        ("--to-command", "to_command"), ("--occurrence", "occurrence"),
    ],
    "systemd": [
        ("systemctl", "service_mgmt"),
        ("journalctl", "journal"),
        ("hostnamectl", "hostname"),
        ("timedatectl", "time_date"),
        ("localectl", "locale"),
        ("loginctl", "login"),
        ("busctl", "dbus"),
        ("systemd-run", "runner"), ("run0", "privilege"),
        ("systemd-analyze", "analysis"),
        ("systemd-cgls", "cgroup"), ("systemd-cgtop", "cgroup"),
        ("systemd-delta", "config_diff"),
        ("systemd-detect-virt", "virtualization"),
        ("systemd-escape", "escape"),
        ("systemd-inhibit", "inhibit"),
        ("systemd-notify", "notify"),
        ("systemd-path", "path"),
        ("systemd-tmpfiles", "tmpfiles"),
        ("systemd-machine-id-setup", "machine_id"),
        ("systemd-firstboot", "firstboot"),
        ("systemd-id128", "id128"),
        ("systemd-mount", "mount"),
        ("systemd-ac-power", "ac_power"),
        ("systemd-creds", "creds"),
        ("systemd-cat", "cat"),
        ("systemd-stdio-bridge", "bridge"),
        ("systemd-socket-activate", "socket"),
        ("coredumpctl", "coredump"),
        ("oomctl", "oom"),
        ("systemd-run", "run"),
        ("systemd-sysext", "sysext"),
        ("systemd-confext", "confext"),
        ("systemd-ask-password", "ask_password"),
        ("poweroff", "power"), ("reboot", "power"), ("halt", "power"),
        ("shutdown", "power"),
    ],
    "git": [
        ("git init", "repo"), ("git clone", "repo"),
        ("git add", "staging"), ("git rm", "staging"), ("git mv", "staging"),
        ("git commit", "commit"), ("git log", "log"), ("git show", "log"),
        ("git diff", "diff"),
        ("git branch", "branch"), ("git checkout", "branch"),
        ("git switch", "branch"), ("git merge", "merge"),
        ("git rebase", "rebase"),
        ("git remote", "remote"), ("git fetch", "remote"),
        ("git pull", "remote"), ("git push", "remote"),
        ("git tag", "tag"),
        ("git stash", "stash"),
        ("git reset", "reset"), ("git restore", "restore"),
        ("git clean", "clean"), ("git gc", "gc"),
        ("git grep", "grep"), ("git blame", "blame"),
        ("git config", "config"),
        ("git status", "status"),
        ("git describe", "describe"),
        ("git rev-parse", "rev_parse"),
        ("git bisect", "bisect"), ("git cherry-pick", "cherry_pick"),
        ("git submodule", "submodule"),
        ("git am", "email"), ("git format-patch", "email"),
        ("git archive", "archive"),
        ("git ls-files", "ls_files"), ("git ls-tree", "ls_tree"),
        ("git reflog", "reflog"),
        ("git worktree", "worktree"),
        ("git shortlog", "shortlog"),
    ],
    "tmux": [
        ("tmux new", "session"), ("tmux attach", "session"),
        ("tmux detach", "session"), ("tmux kill-session", "session"),
        ("tmux rename-session", "session"), ("tmux list-sessions", "session"),
        ("tmux split-window", "window"), ("tmux new-window", "window"),
        ("tmux kill-window", "window"), ("tmux select-window", "window"),
        ("tmux rename-window", "window"), ("tmux list-windows", "window"),
        ("tmux select-pane", "pane"), ("tmux swap-pane", "pane"),
        ("tmux resize-pane", "pane"), ("tmux kill-pane", "pane"),
        ("tmux break-pane", "pane"), ("tmux join-pane", "pane"),
        ("tmux display-panes", "pane"),
        ("tmux send-keys", "interaction"), ("tmux send-prefix", "interaction"),
        ("tmux copy-mode", "interaction"),
        ("tmux command-prompt", "interaction"),
        ("tmux set-option", "config"), ("tmux show-options", "config"),
        ("tmux set-window-option", "config"),
        ("tmux source-file", "config"),
        ("tmux list-keys", "config"), ("tmux list-commands", "config"),
        ("tmux bind-key", "config"), ("tmux unbind-key", "config"),
        ("tmux clock-mode", "display"), ("tmux display-message", "display"),
        ("tmux display", "display"),
        ("tmux if-shell", "scripting"), ("tmux run-shell", "scripting"),
        ("tmux choose-tree", "navigation"), ("tmux choose-session", "navigation"),
        ("tmux capture-pane", "capture"), ("tmux show-buffer", "buffer"),
        ("tmux save-buffer", "buffer"), ("tmux delete-buffer", "buffer"),
        ("tmux list-buffers", "buffer"), ("tmux load-buffer", "buffer"),
        ("tmux paste-buffer", "buffer"),
        ("tmux pipe-pane", "pipe"),
        ("tmux find-window", "search"),
        ("tmux server-info", "server"),
    ],
    "curl": [
        ("curl", "basic"),
        ("-o", "output"), ("-O", "remote_name"), ("-L", "follow"),
        ("-s", "silent"), ("-S", "show_error"), ("-v", "verbose"),
        ("-I", "head"), ("-X", "method"), ("-H", "header"),
        ("-d", "data"), ("-F", "form"), ("-u", "user"),
        ("-x", "proxy"), ("--cacert", "ssl"), ("-k", "insecure"),
        ("--cert", "client_cert"), ("--key", "client_key"),
        ("--connect-timeout", "timeout"), ("-m", "max_time"),
        ("--retry", "retry"),
        ("-A", "user_agent"), ("-e", "referer"),
        ("-b", "cookie"), ("-c", "cookie_jar"),
        ("-w", "write_out"), ("-D", "dump_header"),
        ("-T", "upload"), ("-C", "resume"),
        ("--limit-rate", "rate_limit"),
        ("--resolve", "resolve"),
        ("--compressed", "compressed"),
        ("--data-raw", "data_raw"), ("--data-urlencode", "data_urlencode"),
        ("--json", "json"),
        ("-G", "get_data"), ("--url-query", "url_query"),
    ],
    "openssh": [
        ("ssh", "client"), ("sshd", "server"),
        ("ssh-keygen", "keygen"), ("ssh-copy-id", "copy_id"),
        ("ssh-agent", "agent"), ("ssh-add", "agent"),
        ("ssh-keyscan", "keyscan"),
        ("sftp", "sftp"), ("scp", "scp"),
        ("ssh_config", "config"), ("sshd_config", "config"),
        ("authorized_keys", "auth"),
    ],
    "openssl": [
        ("openssl version", "version"), ("openssl list", "list"),
        ("openssl genrsa", "keygen"), ("openssl rsa", "key"),
        ("openssl req", "csr"), ("openssl x509", "cert"),
        ("openssl s_client", "s_client"), ("openssl s_server", "s_server"),
        ("openssl enc", "encryption"), ("openssl dgst", "digest"),
        ("openssl rand", "random"), ("openssl passwd", "passwd"),
        ("openssl pkcs12", "pkcs12"), ("openssl crl", "crl"),
        ("openssl ocsp", "ocsp"), ("openssl verify", "verify"),
        ("openssl ciphers", "ciphers"), ("openssl speed", "benchmark"),
        ("openssl ts", "timestamp"),
        ("openssl pkey", "pkey"), ("openssl pkeyutl", "pkeyutl"),
        ("openssl dhparam", "dh"), ("openssl ecparam", "ec"),
        ("openssl asn1parse", "asn1"),
    ],
    "pciutils": [
        ("lspci", "list"), ("setpci", "set"),
        ("update-pciids", "update_ids"),
        ("-v", "verbose"), ("-vv", "very_verbose"), ("-k", "kernel_drivers"),
        ("-n", "numeric"), ("-nn", "numeric_ids"),
        ("-t", "tree"), ("-s", "slot"), ("-d", "device"),
        ("-x", "hex_dump"), ("-D", "domains"),
    ],
    "iputils": [
        ("ping", "ping"), ("ping6", "ping6"),
        ("arping", "arping"),
        ("tracepath", "tracepath"), ("traceroute", "traceroute"),
        ("clockdiff", "clockdiff"),
        ("rdisc", "rdisc"),
    ],
    "dnf5-plugins": [
        ("dnf5", "dnf"),
        ("dnf5 copr", "copr"), ("dnf5 builddep", "builddep"),
        ("dnf5 config-manager", "config_manager"),
        ("dnf5 download", "download"),
        ("dnf5 needs-restarting", "needs_restarting"),
        ("dnf5 repoclosure", "repoclosure"),
        ("dnf5 repograph", "repograph"),
        ("dnf5 repomanage", "repomanage"),
        ("dnf5 reposync", "reposync"),
    ],
    "podman": [
        ("podman run", "run"), ("podman ps", "ps"),
        ("podman images", "images"), ("podman pull", "pull"),
        ("podman build", "build"), ("podman exec", "exec"),
        ("podman logs", "logs"), ("podman rm", "rm"),
        ("podman rmi", "rmi"), ("podman stop", "stop"),
        ("podman start", "start"), ("podman restart", "restart"),
        ("podman inspect", "inspect"), ("podman commit", "commit"),
        ("podman tag", "tag"), ("podman push", "push"),
        ("podman cp", "cp"), ("podman top", "top"),
        ("podman stats", "stats"), ("podman port", "port"),
        ("podman network", "network"), ("podman volume", "volume"),
        ("podman secret", "secret"), ("podman pod", "pod"),
        ("podman container", "container"),
        ("podman save", "save"), ("podman load", "load"),
        ("podman export", "export"), ("podman import", "import"),
        ("podman system", "system"),
        ("podman generate", "generate"),
        ("podman healthcheck", "healthcheck"),
        ("podman machine", "machine"),
        ("podman login", "login"), ("podman logout", "logout"),
        ("podman search", "search"),
        ("podman info", "info"), ("podman version", "version"),
    ],
    "wget": [
        ("wget", "basic"),
        ("-O", "output"), ("-o", "log_file"),
        ("-q", "quiet"), ("-nv", "non_verbose"), ("-v", "verbose"),
        ("-c", "continue"), ("-t", "tries"), ("--retry-connrefused", "retry"),
        ("-T", "timeout"), ("--dns-timeout", "dns_timeout"),
        ("--user", "auth"), ("--password", "auth"),
        ("--header", "header"),
        ("--post-data", "post"), ("--post-file", "post_file"),
        ("--method", "method"),
        ("--no-check-certificate", "ssl"), ("--ca-certificate", "ssl"),
        ("--certificate", "ssl"),
        ("-r", "recursive"), ("-l", "level"),
        ("-np", "no_parent"), ("-nd", "no_directories"),
        ("-A", "accept"), ("-R", "reject"),
        ("--spider", "spider"),
        ("-i", "input_file"),
        ("--limit-rate", "limit"),
        ("-P", "directory_prefix"),
        ("--http-user", "http_auth"), ("--http-password", "http_auth"),
        ("--secure-protocol", "protocol"),
        ("--content-disposition", "content_disp"),
        ("--no-clobber", "no_clobber"),
        ("-N", "timestamping"),
        ("--convert-links", "convert_links"),
        ("--no-verbose", "output"),
    ],
    "wget2": [
        ("wget2", "basic"),
        ("-O", "output"), ("-o", "log_file"),
        ("-q", "quiet"), ("-v", "verbose"),
        ("-c", "continue"), ("-t", "tries"),
        ("-T", "timeout"),
        ("--user", "auth"), ("--password", "auth"),
        ("--header", "header"),
        ("--post-data", "post"), ("--post-file", "post_file"),
        ("--method", "method"),
        ("--no-check-certificate", "ssl"),
        ("-r", "recursive"), ("-l", "level"),
        ("-np", "no_parent"), ("-nd", "no_directories"),
        ("-A", "accept"), ("-R", "reject"),
        ("--spider", "spider"),
        ("--limit-rate", "limit"),
        ("-P", "directory_prefix"),
        ("--progress", "progress"),
        ("--filter-mime-type", "filter"),
        ("--stats-server", "stats"),
        ("--http2", "http2"),
        ("--max-threads", "threads"),
        ("--chunk-size", "chunk"),
        ("--dns-cache", "dns"),
        ("--verify-sig", "sig"),
        ("--ocsp", "ocsp"),
        ("--robotstxt", "robots"),
    ],
    "vim": [
        ("vim", "editor"), ("vi", "editor"), ("view", "editor"),
        ("ex", "editor"), ("rvim", "editor"), ("rview", "editor"),
        ("vimdiff", "diff"), ("vimtutor", "tutor"),
        ("xxd", "xxd"),
        ("-c", "command"), ("-e", "ex_mode"),
        ("-s", "silent"), ("-R", "readonly"),
        ("-b", "binary"), ("-n", "no_swap"),
        ("-r", "recovery"), ("-u", "vimrc"),
        ("--noplugin", "noplugin"),
        (":q", "ex_cmd"), (":w", "ex_cmd"), (":e", "ex_cmd"),
        (":set", "ex_cmd"), (":syntax", "ex_cmd"),
        ("/search", "search"), (":%s", "substitute"),
        ("dd", "normal_cmd"), ("yy", "normal_cmd"), ("p", "normal_cmd"),
        ("u", "undo"), ("Ctrl-r", "redo"),
        ("i", "insert"), ("a", "append"), ("o", "open_line"),
        ("v", "visual"), ("V", "visual_line"),
    ],
    "make": [
        ("make", "basic"),
        ("-f", "file"), ("-C", "directory"), ("-j", "jobs"),
        ("-k", "keep_going"), ("-n", "dry_run"), ("-s", "silent"),
        ("-B", "always_make"), ("-d", "debug"),
        ("-i", "ignore_errors"), ("-w", "print_directory"),
        ("-p", "print_db"), ("-q", "question"),
        ("-t", "touch"), ("-e", "environment_overrides"),
    ],
    "gcc": [
        ("gcc", "compile"), ("g++", "cpp"), ("gfortran", "fortran"),
        ("-o", "output"), ("-c", "compile_only"), ("-E", "preprocess"),
        ("-S", "assemble"), ("-Wall", "warnings"), ("-Werror", "warnings"),
        ("-g", "debug"), ("-O0", "optimize"), ("-O2", "optimize"),
        ("-O3", "optimize"), ("-Os", "optimize"),
        ("-std", "standard"), ("-I", "include"), ("-L", "lib_path"),
        ("-l", "link"), ("-shared", "shared"),
        ("-fPIC", "pic"), ("-fPIE", "pie"),
        ("-D", "define"), ("-U", "undefine"),
        ("-static", "static"), ("-march", "arch"),
        ("-v", "verbose"),
    ],
    "gdb": [
        ("gdb", "debugger"), ("gdbserver", "server"),
        ("-p", "attach"), ("-c", "core"), ("-q", "quiet"),
        ("run", "run_cmd"), ("continue", "continue_cmd"),
        ("break", "breakpoint"), ("watch", "watchpoint"),
        ("step", "step"), ("next", "next"),
        ("print", "print"), ("backtrace", "backtrace"),
        ("info", "info"), ("list", "list"),
        ("set", "set"), ("show", "show"),
        ("frame", "frame"), ("thread", "thread"),
        ("disassemble", "disasm"),
    ],
    "rpmbuild": [
        ("rpmbuild", "build"),
        ("-ba", "build_all"), ("-bb", "build_binary"),
        ("-bp", "prep"), ("-bc", "compile"), ("-bi", "install"),
        ("-bl", "list_check"), ("-bs", "source"),
        ("--define", "define"), ("--with", "with"), ("--without", "without"),
        ("--target", "target"), ("--nodeps", "nodeps"),
        ("-v", "verbose"), ("--quiet", "quiet"),
        ("rpmdev-setuptree", "setup_tree"),
        ("rpmspec", "rpmspec"),
        ("rpmbuild --rebuild", "rebuild"),
    ],
    "bash": [
        ("bash", "shell"),
        ("-c", "command"), ("-s", "stdin"),
        ("-i", "interactive"), ("-l", "login"),
        ("-x", "xtrace"), ("-v", "verbose"), ("-n", "syntax_check"),
        ("-e", "errexit"), ("-u", "nounset"), ("-o pipefail", "pipefail"),
        ("if", "conditional"), ("for", "loop"), ("while", "loop"),
        ("case", "conditional"), ("select", "loop"),
        ("function", "function"), ("alias", "alias"),
        ("export", "builtin"), ("readonly", "builtin"),
        ("local", "builtin"), ("declare", "builtin"),
        ("source", "builtin"), (".", "builtin"),
        ("echo", "builtin"), ("printf", "builtin"),
        ("read", "builtin"), ("mapfile", "builtin"),
        ("set", "builtin"), ("shopt", "builtin"),
        ("$", "variable"), ("${}", "expansion"),
        ("$()", "command_sub"), ("$(())", "arithmetic"),
        ("trap", "trap"), ("eval", "eval"), ("exec", "exec"),
        ("<(", "process_sub"), (">(", "process_sub"),
        ("<<<", "herestring"), ("<<", "heredoc"),
        ("|", "pipe"), (">", "redirect"), (">>", "redirect"), ("<", "redirect"),
        ("2>", "stderr"), ("2>&1", "stderr"),
        ("&&", "logical"), ("||", "logical"),
        ("*", "glob"), ("?", "glob"), ("[...]", "glob"),
        ("a[b]", "array"), ("declare -A", "assoc_array"),
        ("${var:-}", "default"), ("${var:=}", "default"),
        ("${var%}", "remove"), ("${var#}", "remove"),
        ("${var//}", "replace"), ("${var^^}", "case_mod"),
    ],
    "python": [
        ("python3", "interpreter"),
        ("-c", "command"), ("-m", "module"), ("-i", "interactive"),
        ("-V", "version"), ("-v", "verbose"),
        ("-O", "optimize"), ("-OO", "optimize"),
        ("-B", "no_bytecode"), ("-s", "no_user_site"),
        ("-E", "ignore_env"), ("-I", "isolated"),
        ("-u", "unbuffered"), ("-W", "warning"),
        ("python3 -m pip", "pip"), ("python3 -m venv", "venv"),
        ("python3 -m http.server", "http_server"),
        ("python3 -m json.tool", "json_tool"),
        ("python3 -m ensurepip", "ensurepip"),
        ("pip3", "pip"), ("pydoc3", "pydoc"),
    ],
    "rpm": [
        ("rpm", "basic"), ("rpmkeys", "keys"),
        ("-q", "query"), ("-i", "install"), ("-e", "erase"),
        ("-U", "upgrade"), ("-F", "freshen"),
        ("-V", "verify"), ("-K", "checksig"),
        ("-a", "all"), ("-l", "list_files"), ("-c", "config_files"),
        ("-d", "doc_files"), ("-R", "requires"), ("--provides", "provides"),
        ("--whatrequires", "whatrequires"), ("--whatprovides", "whatprovides"),
        ("--changelog", "changelog"), ("-s", "state"),
        ("--scripts", "scripts"), ("--triggers", "triggers"),
        ("--import", "import_key"),
        ("-v", "verbose"), ("--nodeps", "nodeps"),
        ("--test", "test_mode"),
        ("--qf", "queryformat"),
    ],
    "systemd-timesyncd": [
        ("timedatectl", "time"), ("systemd-timesyncd", "service"),
        ("/etc/systemd/timesyncd.conf", "config"),
    ],
    "procps-ng": [
        ("ps", "process"), ("top", "top"), ("free", "memory"),
        ("pgrep", "pgrep"), ("pkill", "pkill"), ("pmap", "pmap"),
        ("pwdx", "pwdx"), ("uptime", "uptime"),
        ("vmstat", "vmstat"), ("w", "w"),
        ("watch", "watch"), ("pidwait", "pidwait"),
        ("sysctl", "sysctl"), ("sysctl -p", "sysctl"),
        ("skill", "skill"), ("snice", "snice"),
        ("slabtop", "slabtop"), ("tload", "tload"),
    ],
    "psmisc": [
        ("fuser", "fuser"), ("killall", "killall"),
        ("peekfd", "peekfd"), ("prtstat", "prtstat"),
        ("pstree", "pstree"),
    ],
    "findutils": [
        ("find", "find"), ("locate", "locate"), ("updatedb", "updatedb"),
        ("xargs", "xargs"),
        ("-name", "name"), ("-type", "type"), ("-size", "size"),
        ("-mtime", "time"), ("-user", "user"), ("-perm", "perm"),
        ("-exec", "exec"), ("-delete", "delete"), ("-print", "print"),
        ("-maxdepth", "maxdepth"), ("-mindepth", "mindepth"),
        ("-empty", "empty"), ("-newer", "newer"),
        ("-o", "or"), ("-a", "and"), ("-not", "not"),
        ("xargs -n", "xargs_options"), ("xargs -I", "xargs_options"),
        ("xargs -P", "xargs_options"), ("xargs -0", "xargs_options"),
    ],
    "sed": [
        ("sed", "basic"),
        ("s/old/new/", "substitute"), ("/pattern/d", "delete"),
        ("/pattern/p", "print"), ("-n", "quiet"),
        ("-e", "expression"), ("-f", "script_file"),
        ("-i", "in_place"), ("-r", "extended_regex"),
        ("ADDR", "address"), ("y/old/new/", "transliterate"),
    ],
    "openssh-clients": [
        ("ssh", "ssh"), ("scp", "scp"), ("sftp", "sftp"),
        ("ssh-keygen", "keygen"), ("ssh-copy-id", "copy_id"),
        ("ssh-keyscan", "keyscan"), ("ssh-agent", "agent"),
        ("ssh-add", "agent"),
    ],
    "clang": [
        ("clang", "compile"), ("clang++", "cpp"), ("clang-tidy", "tidy"),
        ("clang-format", "format"), ("clang-check", "check"),
        ("clang-query", "query"),
        ("scan-build", "scan_build"), ("scan-view", "scan_view"),
        ("-o", "output"), ("-c", "compile_only"), ("-g", "debug"),
        ("-Wall", "warnings"), ("-std", "standard"),
    ],
    "llvm/clang-tools-extra": [
        ("llvm-ar", "llvm"), ("llvm-nm", "llvm"), ("llvm-objdump", "llvm"),
        ("llvm-objcopy", "llvm"), ("llvm-strip", "llvm"),
        ("llvm-readobj", "llvm"), ("llvm-size", "llvm"),
        ("llvm-strings", "llvm"), ("llvm-symbolizer", "llvm"),
    ],
    "binutils": [
        ("as", "assembler"), ("ld", "linker"),
        ("objdump", "objdump"), ("objcopy", "objcopy"),
        ("nm", "nm"), ("size", "size"),
        ("strings", "strings"), ("strip", "strip"),
        ("readelf", "readelf"), ("addr2line", "addr2line"),
        ("ar", "ar"), ("ranlib", "ranlib"),
        ("c++filt", "c++filt"), ("gprof", "gprof"),
    ],
    "util-linux": [
        ("mount", "mount"), ("umount", "umount"),
        ("fdisk", "fdisk"), ("partx", "partx"),
        ("blockdev", "block"), ("lsblk", "block"), ("findmnt", "findmnt"),
        ("blkid", "block"), ("wipefs", "block"),
        ("losetup", "loop"), ("swapon", "swap"),
        ("dmesg", "dmesg"), ("flock", "flock"),
        ("fallocate", "fallocate"), ("rename", "rename"),
        ("uuidgen", "uuid"), ("script", "script"),
        ("hardlink", "hardlink"), ("lslogins", "login"),
        ("lscpu", "lscpu"), ("lsipc", "lsipc"),
        ("lslocks", "lslocks"), ("lsmem", "lsmem"),
        ("lsns", "lsns"),
        ("fstrim", "fstrim"), ("ipcs", "ipcs"),
        ("setarch", "setarch"), ("unshare", "unshare"),
        ("nsenter", "nsenter"), ("taskset", "taskset"),
        ("column", "column"), ("hexdump", "hexdump"),
        ("cal", "cal"), ("whereis", "whereis"),
        ("kill", "kill"), ("logger", "logger"),
        ("mcookie", "mcookie"), ("namei", "namei"),
        ("more", "more"), ("rev", "rev"),
    ],
    "iproute2": [
        ("ip", "ip"), ("ss", "ss"), ("tc", "tc"),
        ("bridge", "bridge"), ("lnstat", "lnstat"),
        ("nstat", "nstat"), ("rdma", "rdma"),
        ("devlink", "devlink"), ("tipc", "tipc"),
        ("ip addr", "addr"), ("ip link", "link"), ("ip route", "route"),
        ("ip neigh", "neigh"), ("ip rule", "rule"),
        ("ip netns", "netns"), ("ip maddr", "maddr"),
        ("ip tunnel", "tunnel"), ("ip monitor", "monitor"),
        ("tc qdisc", "qdisc"), ("tc filter", "filter"), ("tc class", "class"),
    ],
    "labwc": [
        ("labwc", "compositor"),
        ("--config", "config"), ("-C", "config_dir"),
        ("-s", "startup"), ("-d", "debug"),
        ("-v", "version"),
    ],
    "weston": [
        ("weston", "compositor"),
        ("weston-terminal", "terminal"),
        ("weston-info", "info"), ("weston-debug", "debug"),
        ("--backend", "backend"), ("--shell", "shell"),
        ("--tty", "tty"), ("--modules", "modules"),
    ],
    "sddm": [
        ("sddm", "display_manager"),
        ("sddm-greeter", "greeter"),
        ("sddm.conf", "config"),
    ],
}


def extract_tested_items(test_sh_path):
    """Extract what commands/features are being tested from a test.sh file."""
    if not test_sh_path.exists():
        return set(), set()
    
    try:
        content = test_sh_path.read_text(encoding='utf-8')
    except:
        return set(), set()
    
    commands = set()
    features = set()
    
    # Extract commands from rlRun invocations
    rlrun_pattern = re.findall(r'rlRun\s+"([^"]+)"', content)
    for cmd in rlrun_pattern:
        # Extract the actual command (before first space, or before first pipe/redirect)
        cmd = cmd.strip()
        # Handle "test $(...) ..." patterns
        if cmd.startswith('test '):
            inner = cmd[5:]
            if inner.startswith('$('):
                inner_match = re.match(r'\$\(([^)]+)\)', inner)
                if inner_match:
                    cmd = inner_match.group(1).strip()
            elif inner.startswith('"'):
                # string test
                commands.add('test')
                continue
            else:
                parts = inner.split()
                if parts:
                    cmd = parts[0]
        # Skip compound commands
        if cmd.startswith('test ') or cmd.startswith('['):
            commands.add('test')
            continue
        if cmd.startswith('echo '):
            continue
        if cmd.startswith('printf '):
            continue
        if cmd.startswith('mkdir ') or cmd.startswith('cd ') or cmd.startswith('rm '):
            continue
        if cmd.startswith('grep ') or cmd.startswith('! grep'):
            continue
        
        # Extract main command
        parts = cmd.split()
        if not parts:
            continue
        main_cmd = parts[0]
        
        # Handle special cases
        if main_cmd == 'if' or main_cmd == 'for' or main_cmd == 'while':
            continue
        
        # Include subcommands
        if main_cmd in ('podman', 'dnf5', 'git', 'systemctl', 'tmux', 
                         'rpmbuild', 'make', 'ip', 'tc', 'ss'):
            if len(parts) >= 2 and not parts[1].startswith('-'):
                commands.add(f"{main_cmd} {parts[1]}")
            else:
                commands.add(main_cmd)
        elif main_cmd in ('grep', 'tar', 'curl', 'wget', 'wget2'):
            commands.add(main_cmd)
            # Add flags
            for p in parts[1:]:
                if p.startswith('-') and len(p) <= 4 and not p.startswith('--'):
                    commands.add(p)
        else:
            commands.add(main_cmd)
    
    return commands, features


def analyze_package(pkg_dir):
    """Analyze a single package's test coverage."""
    pkg_name = pkg_dir.name
    test_dirs = [d for d in sorted(pkg_dir.iterdir()) if d.is_dir()]
    
    all_tested = set()
    test_details = []
    
    for td in test_dirs:
        test_sh = td / "test.sh"
        cmds, features = extract_tested_items(test_sh)
        all_tested.update(cmds)
        test_details.append({
            "name": td.name,
            "tested_commands": sorted(cmds),
            "tested_features": sorted(features),
        })
    
    # Get known commands for this package
    known_commands = PACKAGE_COMMANDS.get(pkg_name, [])
    known_cmd_names = {c[0] for c in known_commands}
    
    # Calculate coverage
    missing = known_cmd_names - all_tested
    extra = all_tested - known_cmd_names
    
    coverage_pct = 0
    if known_cmd_names:
        coverage_pct = round(100 * len(known_cmd_names - missing) / len(known_cmd_names), 1)
    
    return {
        "package": pkg_name,
        "test_count": len(test_dirs),
        "tested_commands": sorted(all_tested),
        "known_commands": sorted(known_cmd_names) if known_cmd_names else [],
        "missing_commands": sorted(missing),
        "extra_commands": sorted(extra),
        "coverage_pct": coverage_pct,
        "test_details": test_details,
    }


def main():
    results = []
    
    for pkg_dir in sorted(PKGS_DIR.iterdir()):
        if not pkg_dir.is_dir():
            continue
        result = analyze_package(pkg_dir)
        results.append(result)
    
    # Sort by coverage (ascending = gaps first)
    results.sort(key=lambda r: r["coverage_pct"])
    
    # Print summary
    print("=" * 100)
    print("  pkgs 测试覆盖率分析报告")
    print("=" * 100)
    print(f"  总包数: {len(results)}")
    print(f"  无已知命令参考的包: {sum(1 for r in results if not r['known_commands'])}")
    print(f"  有已知命令参考的包: {sum(1 for r in results if r['known_commands'])}")
    print()
    
    # Report: packages with gaps
    print("=" * 100)
    print("  需要改进的包 (覆盖率 < 80%)")
    print("=" * 100)
    gaps = [r for r in results if r["coverage_pct"] < 80 and r["known_commands"]]
    if gaps:
        print(f"{'Package':<25} {'Tests':<8} {'已知命令':<10} {'已测试':<10} {'缺失':<10} {'覆盖率':<10}")
        print("-" * 80)
        for r in gaps:
            print(f"{r['package']:<25} {r['test_count']:<8} {len(r['known_commands']):<10} {len(r['tested_commands']):<10} {len(r['missing_commands']):<10} {r['coverage_pct']:<9}%")
            if r["missing_commands"]:
                print(f"  Missing: {', '.join(r['missing_commands'][:20])}")
                if len(r['missing_commands']) > 20:
                    print(f"  ... and {len(r['missing_commands'])-20} more")
    
    print()
    print("=" * 100)
    print("  覆盖率较好的包 (80-99%)")
    print("=" * 100)
    good = [r for r in results if 80 <= r["coverage_pct"] < 100 and r["known_commands"]]
    for r in sorted(good, key=lambda x: x["coverage_pct"]):
        print(f"  {r['package']:<25} 覆盖率: {r['coverage_pct']}%  缺失: {', '.join(r['missing_commands'][:10])}")
    
    print()
    print("=" * 100)
    print("  完全覆盖的包 (100%)")
    print("=" * 100)
    perfect = [r for r in results if r["coverage_pct"] == 100 and r["known_commands"]]
    for r in perfect:
        print(f"  {r['package']:<25} ({len(r['known_commands'])} commands)")
    
    # Report: packages without known command reference
    print()
    print("=" * 100)
    print("  无已知命令参考的包 (需要手动评估)")
    print("=" * 100)
    no_ref = [r for r in results if not r["known_commands"]]
    for r in no_ref:
        cmds_str = ', '.join(r['tested_commands'][:10])
        more = f" ... (+{len(r['tested_commands'])-10} more)" if len(r['tested_commands']) > 10 else ""
        print(f"  {r['package']:<30} 测试={r['test_count']} 命令={cmds_str}{more}")
    
    # Output JSON for detailed analysis
    output_path = Path(os.environ.get("TEMP", "/tmp")) / "coverage_analysis.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n  Detailed JSON: {output_path}")


if __name__ == "__main__":
    main()