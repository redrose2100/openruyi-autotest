#!/usr/bin/env python3
"""
Enhanced pkgs test coverage analysis.
Parses BOTH directory names AND test.sh contents to identify tested features.
"""
import os
import re
import json
from pathlib import Path
from collections import defaultdict

PKGS_DIR = Path(r"E:\code\openruyi-autotest\tests\functional\pkgs")

# Map: package name -> (command/feature, category, detail)
# Based on RPM package manifests and common usage
PACKAGE_FEATURES = {}

def add_pkg(name, features):
    PACKAGE_FEATURES[name] = features

# ============================================================
# Core system packages with rich command sets
# ============================================================

add_pkg("coreutils", [
    # File ops
    ("cp", "file_copy"), ("mv", "move"), ("rm", "remove"), ("rmdir", "remove"),
    ("install", "install"), ("ln", "links"), ("link", "links"),
    ("unlink", "links"), ("readlink", "links"),
    ("mkdir", "dirs"), ("touch", "files"),
    # Viewing
    ("cat", "view"), ("tac", "view"), ("nl", "view"),
    ("head", "view"), ("tail", "view"), ("od", "view"),
    # Text
    ("sort", "text"), ("uniq", "text"), ("cut", "text"), ("tr", "text"),
    ("paste", "text"), ("comm", "text"), ("join", "text"),
    ("fmt", "text"), ("fold", "text"), ("expand", "text"), ("unexpand", "text"),
    # Checksums
    ("cksum", "checksum"), ("md5sum", "checksum"), ("sha1sum", "checksum"),
    ("sha224sum", "checksum"), ("sha256sum", "checksum"),
    ("sha384sum", "checksum"), ("sha512sum", "checksum"),
    ("b2sum", "checksum"), ("sum", "checksum"),
    # Boolean
    ("true", "bool"), ("false", "bool"), ("test", "bool"), ("[", "bool"),
    # Env
    ("env", "env"), ("printenv", "env"), ("date", "env"),
    ("printf", "env"),
    # System
    ("uname", "sysinfo"), ("who", "sysinfo"), ("whoami", "sysinfo"),
    ("id", "sysinfo"), ("groups", "sysinfo"), ("hostname", "sysinfo"),
    ("users", "sysinfo"), ("logname", "sysinfo"),
    # File ops
    ("dd", "fileops"), ("truncate", "fileops"),
    ("shred", "fileops"), ("sync", "fileops"),
    # Counting
    ("wc", "count"), ("du", "count"), ("df", "count"), ("stat", "count"),
    # Path
    ("basename", "path"), ("dirname", "path"), ("pwd", "path"),
    ("realpath", "path"), ("mktemp", "path"),
    # Permissions
    ("chmod", "perm"), ("chown", "perm"), ("chgrp", "perm"),
    # Process
    ("nice", "proc"), ("nohup", "proc"), ("stdbuf", "proc"),
    # Flow
    ("sleep", "flow"), ("timeout", "flow"), ("yes", "flow"),
    # IO
    ("tee", "io"),
    # Split
    ("split", "split"), ("csplit", "split"),
    # Special
    ("stty", "special"), ("pathchk", "special"),
    ("tsort", "special"), ("ptx", "special"), ("dircolors", "special"),
    # Encoding
    ("base32", "encode"), ("base64", "encode"), ("basenc", "encode"),
    # Numbers
    ("seq", "num"), ("factor", "num"), ("shuf", "num"), ("numfmt", "num"),
    # Listing
    ("ls", "list"), ("dir", "list"), ("vdir", "list"),
    # Output
    ("echo", "output"),
])

add_pkg("grep", [
    ("basic_pattern", "grep 'pattern' file"), ("pipe_input", "echo | grep"),
    ("egrep", "egrep"), ("fgrep", "fgrep"),
    ("-E", "extended regex"), ("-F", "fixed strings"), ("-G", "basic regex"),
    ("-P", "perl regex (if supported)"),
    ("-i", "case insensitive"), ("-v", "invert match"),
    ("-c", "count"), ("-n", "line numbers"),
    ("-l", "list matching files"), ("-L", "list non-matching files"),
    ("-o", "only matching"), ("-q", "quiet"),
    ("-r", "recursive"), ("-R", "recursive deref"),
    ("-w", "word match"), ("-x", "line match"),
    ("-A", "after context"), ("-B", "before context"), ("-C", "context"),
    ("-e", "multiple patterns"), ("-f", "pattern from file"),
    ("-H", "show filename"), ("-h", "no filename"),
    ("-m", "max count"), ("-s", "silent errors"),
    ("--color", "color output"),
    ("multi_file", "grep across files"),
])

add_pkg("tar", [
    ("-c", "create archive"), ("-x", "extract"), ("-t", "list contents"),
    ("-r", "append"), ("-u", "update"), ("--delete", "delete"),
    ("-f", "file name"), ("-v", "verbose"),
    ("-z", "gzip"), ("-j", "bzip2"), ("-J", "xz"),
    ("--zstd", "zstd"), ("--lzma", "lzma"), ("--lzip", "lzip"),
    ("-C", "change dir"), ("--strip-components", "strip paths"),
    ("--exclude", "exclude"), ("--wildcards", "wildcard"),
    ("--listed-incremental", "incremental backup"),
    ("--diff", "diff/verify"),
    ("--preserve-permissions", "preserve"),
    ("--transform", "transform names"),
    ("special_files", "symlinks/devices"),
    ("error_handling", "error cases"),
])

add_pkg("systemd", [
    ("systemctl", "service management"),
    ("journalctl", "journal query"),
    ("hostnamectl", "hostname"),
    ("timedatectl", "time/date"),
    ("localectl", "locale"),
    ("loginctl", "login/session"),
    ("busctl", "D-Bus"),
    ("systemd-run", "run commands"),
    ("systemd-analyze", "system analysis"),
    ("systemd-cgls", "cgroup listing"),
    ("systemd-cgtop", "cgroup top"),
    ("systemd-delta", "config diff"),
    ("systemd-detect-virt", "detect virt"),
    ("systemd-escape", "string escape"),
    ("systemd-inhibit", "inhibit"),
    ("systemd-notify", "notify"),
    ("systemd-path", "path query"),
    ("systemd-tmpfiles", "tmpfiles"),
    ("systemd-machine-id-setup", "machine id"),
    ("systemd-firstboot", "firstboot"),
    ("systemd-id128", "id128"),
    ("systemd-mount", "mount units"),
    ("systemd-ac-power", "ac power check"),
    ("systemd-creds", "credentials"),
    ("systemd-cat", "cat to journal"),
    ("systemd-stdio-bridge", "stdio bridge"),
    ("systemd-socket-activate", "socket activation"),
    ("coredumpctl", "coredump"),
    ("oomctl", "OOM management"),
    ("systemd-run0", "privilege escalation"),
    ("systemd-sysext", "sysext"),
    ("systemd-confext", "confext"),
    ("systemd-ask-password", "ask password"),
    ("poweroff/reboot", "power commands"),
    ("error_handling", "error cases"),
])

add_pkg("git", [
    ("init", "init repo"), ("clone", "clone"),
    ("add/rm/mv", "staging"), ("commit", "commit"),
    ("log/show", "history"), ("diff", "diff"),
    ("branch", "branch"), ("tag", "tag"),
    ("merge", "merge"), ("rebase", "rebase"),
    ("remote", "remote ops"), ("fetch/pull/push", "sync"),
    ("stash", "stash"),
    ("reset/restore", "undo"),
    ("clean/gc", "cleanup"),
    ("config", "config"),
    ("grep/blame", "search"),
    ("bisect", "bisect"),
    ("cherry-pick", "cherry-pick"),
    ("submodule", "submodule"),
    ("worktree", "worktree"),
    ("reflog", "reflog"),
    ("archive", "archive"),
    ("am/format-patch", "email patch"),
    ("error_handling", "error cases"),
])

add_pkg("tmux", [
    ("new-session", "create session"), ("attach", "attach"),
    ("detach", "detach"), ("kill-session", "kill session"),
    ("list-sessions", "list sessions"),
    ("new-window", "create window"), ("split-window", "split"),
    ("kill-window", "kill window"), ("select-window", "select"),
    ("select-pane", "select pane"), ("swap-pane", "swap pane"),
    ("resize-pane", "resize pane"),
    ("send-keys", "send keys"),
    ("copy-mode", "copy mode"),
    ("set-option", "set option"), ("show-options", "show options"),
    ("source-file", "source config"),
    ("list-keys", "list keys"),
    ("display-message", "display"),
    ("capture-pane", "capture"),
    ("save-buffer", "buffer ops"),
    ("command-prompt", "command prompt"),
    ("clock-mode", "clock"),
    ("choose-tree", "choose tree"),
    ("find-window", "find window"),
    ("if-shell/run-shell", "scripting"),
    ("pipe-pane", "pipe"),
    ("server-info", "server info"),
])

add_pkg("curl", [
    ("basic_get", "HTTP GET"), ("-o/-O", "output to file"),
    ("-L", "follow redirect"), ("-s/-S", "silent/show error"),
    ("-v", "verbose"), ("-I", "HEAD request"),
    ("-X", "custom method"), ("-H", "custom header"),
    ("-d", "POST data"), ("-F", "multipart form"),
    ("-u", "user auth"), ("-x", "proxy"),
    ("-k", "insecure SSL"), ("--cacert", "CA cert"),
    ("--cert/--key", "client cert"),
    ("--connect-timeout", "timeout"), ("-m", "max time"),
    ("--retry", "retry"),
    ("-A", "user agent"), ("-b/-c", "cookies"),
    ("-w", "write-out vars"), ("-D", "dump headers"),
    ("-T", "upload"), ("-C", "resume"),
    ("--limit-rate", "rate limit"),
    ("--resolve", "DNS resolve"),
    ("--compressed", "compressed"),
    ("--data-raw", "raw data"), ("--json", "JSON data"),
    ("-G", "GET with data"),
    ("error_handling", "error cases"),
])

add_pkg("wget", [
    ("basic", "download"), ("-O", "output file"),
    ("-o", "log file"), ("-q/-nv/-v", "verbosity"),
    ("-c", "continue"), ("-t", "retries"),
    ("-T", "timeout"), ("--dns-timeout", "DNS timeout"),
    ("--user/--password", "auth"),
    ("--header", "custom header"),
    ("--post-data/--post-file", "POST"),
    ("--method", "HTTP method"),
    ("--no-check-certificate", "SSL"),
    ("-r", "recursive"), ("-l", "recursion level"),
    ("-np", "no parent"), ("-nd", "no directories"),
    ("-A/-R", "accept/reject"),
    ("--spider", "spider mode"),
    ("-i", "input file"),
    ("--limit-rate", "rate limit"),
    ("-P", "directory prefix"),
    ("--content-disposition", "content disp"),
    ("-N", "timestamping"),
    ("--convert-links", "convert links"),
    ("--no-clobber", "no clobber"),
    ("--secure-protocol", "protocol"),
    ("error_handling", "error cases"),
])

add_pkg("wget2", [
    ("basic", "download"), ("-O", "output file"),
    ("-o", "log file"), ("-q/-v", "verbosity"),
    ("-c", "continue"), ("-t", "retries"),
    ("-T", "timeout"),
    ("--user/--password", "auth"),
    ("--header", "custom header"),
    ("--post-data/--post-file", "POST"),
    ("--method", "HTTP method"),
    ("--no-check-certificate", "SSL"),
    ("-r", "recursive"), ("-l", "level"),
    ("-np", "no parent"), ("-nd", "no directories"),
    ("-A/-R", "accept/reject"),
    ("--spider", "spider mode"),
    ("--limit-rate", "rate limit"),
    ("-P", "directory prefix"),
    ("--progress", "progress bar"),
    ("--filter-mime-type", "MIME filter"),
    ("--stats-server", "stats"),
    ("--http2", "HTTP/2"),
    ("--max-threads", "max threads"),
    ("--chunk-size", "chunk size"),
    ("--dns-cache", "DNS cache"),
    ("--verify-sig", "verify signature"),
    ("--ocsp", "OCSP"),
    ("--robotstxt", "robots.txt"),
    ("error_handling", "error cases"),
])

add_pkg("openssl", [
    ("version", "version info"), ("list", "list commands"),
    ("genrsa/rsa", "RSA key pair"),
    ("req/x509", "certificate req/sign"),
    ("s_client", "TLS client"), ("s_server", "TLS server"),
    ("enc/dec", "symmetric encrypt"),
    ("dgst", "hash/digest"),
    ("rand", "random bytes"),
    ("passwd", "password hash"),
    ("pkcs12", "PKCS#12"),
    ("verify", "certificate verify"),
    ("ciphers", "cipher list"),
    ("speed", "benchmark"),
    ("ocsp", "OCSP"),
    ("crl", "CRL"),
    ("ts", "timestamp"),
    ("pkey/pkeyutl", "key operations"),
    ("dhparam", "DH params"),
    ("ecparam", "EC params"),
    ("asn1parse", "ASN.1 parse"),
])

add_pkg("openssh", [
    ("ssh", "remote shell"), ("sshd", "daemon"),
    ("ssh-keygen", "key generation"),
    ("ssh-copy-id", "copy public key"),
    ("ssh-agent/ssh-add", "agent"),
    ("ssh-keyscan", "host key scan"),
    ("scp", "remote copy"), ("sftp", "SFTP"),
    ("config", "SSH config files"),
    ("authorized_keys", "authorized keys"),
])

add_pkg("openssh-clients", [
    ("ssh", "remote shell"), ("scp", "remote copy"),
    ("sftp", "SFTP"), ("ssh-keygen", "key gen"),
    ("ssh-copy-id", "copy id"),
    ("ssh-keyscan", "keyscan"),
    ("ssh-agent/ssh-add", "agent"),
])

add_pkg("python", [
    ("python3", "interpreter"), ("-c", "command"),
    ("-m", "module"), ("-i", "interactive"),
    ("-V", "version"),
    ("-m pip", "pip module"), ("-m venv", "venv"),
    ("-m http.server", "HTTP server"),
    ("-m json.tool", "JSON formatter"),
    ("pip3", "pip command"),
    ("pydoc3", "pydoc"),
    ("python3 -m ensurepip", "ensure pip"),
])

add_pkg("rpm", [
    ("-q", "query"), ("-i", "install"), ("-e", "erase"),
    ("-U", "upgrade"), ("-F", "freshen"),
    ("-V", "verify"), ("-K", "signature check"),
    ("-a", "query all"), ("-l", "list files"),
    ("-c", "config files"), ("-d", "doc files"),
    ("-R", "requires"), ("--provides", "provides"),
    ("--whatrequires", "what requires"),
    ("--whatprovides", "what provides"),
    ("--changelog", "changelog"),
    ("--scripts", "scripts"), ("--triggers", "triggers"),
    ("--import", "import GPG key"),
    ("--test", "test mode"),
    ("--nodeps", "no deps"),
    ("-v", "verbose"),
    ("--qf", "query format"),
    ("rpmkeys", "key management"),
])

add_pkg("rpmbuild", [
    ("rpmbuild", "build RPM"),
    ("-ba", "build all"), ("-bb", "build binary"),
    ("-bp", "prep stage"), ("-bc", "compile stage"),
    ("-bi", "install stage"), ("-bl", "list check"),
    ("-bs", "source only"),
    ("--define", "macro define"),
    ("--with/--without", "with/without"),
    ("--target", "target arch"),
    ("--nodeps", "no deps check"),
    ("--rebuild", "rebuild from SRPM"),
    ("rpmdev-setuptree", "setup build tree"),
    ("rpmspec", "parse spec"),
])

add_pkg("bash", [
    ("bash", "interactive shell"),
    ("-c", "execute command"), ("-s", "stdin"),
    ("-x", "xtrace"), ("-v", "verbose"),
    ("-n", "syntax check"), ("-e", "errexit"),
    ("-u", "nounset"), ("-o pipefail", "pipefail"),
    ("if/then/else", "conditional"),
    ("for loop", "for loop"), ("while loop", "while"),
    ("case", "case"), ("function", "function"),
    ("|", "pipe"), (">/>>", "redirect"), ("<", "input redirect"),
    ("2>/2>&1", "stderr redirect"),
    ("&&/||", "logical operators"),
    ("$var", "variable"), ("${param}", "expansion"),
    ("$()", "command substitution"),
    ("$(())", "arithmetic"),
    ("trap", "signal trap"), ("eval", "eval"),
    ("source/\.", "source"),
    ("array", "indexed array"), ("declare -A", "assoc array"),
    ("${#}", "length"), ("${%}", "pattern remove"),
    ("${//}", "pattern replace"),
    ("<<<", "herestring"), ("<<", "heredoc"),
    ("*", "glob"), ("?", "glob"),
    ("alias", "alias"), ("export", "export"),
    ("readonly", "readonly"), ("declare", "declare"),
    ("read", "read input"), ("mapfile", "mapfile"),
    ("shopt", "shell options"), ("set", "set options"),
    ("error_handling", "error handling"),
])

add_pkg("vim", [
    ("vim/vi", "editor basics"),
    ("vimdiff", "diff mode"), ("vimtutor", "tutor"),
    ("xxd", "hex dump"),
    ("-c", "command line"), ("-e", "ex mode"),
    ("-R", "readonly"), ("-b", "binary"),
    ("-n", "no swap"), ("-r", "recovery"),
    ("-s", "silent/script"),
    ("-u", "vimrc"),
    ("i/a/o", "insert/append/open"),
    ("dd/yy/p", "delete/yank/put"),
    ("u/Ctrl-r", "undo/redo"),
    ("v/V", "visual mode"),
    (":q/:w/:e", "file commands"),
    (":set", "settings"),
    (":%s", "substitute"),
    ("/search", "search"),
    (":syntax", "syntax highlighting"),
    ("error_handling", "error handling"),
])

add_pkg("make", [
    ("make", "basic build"),
    ("-f", "alternate Makefile"),
    ("-C", "change directory"),
    ("-j", "parallel jobs"),
    ("-k", "keep going"),
    ("-n", "dry run"),
    ("-B", "always make"),
    ("-d", "debug output"),
    ("-s", "silent"),
    ("-i", "ignore errors"),
    ("-e", "env overrides"),
    ("-p", "print database"),
    ("-q", "question mode"),
    ("-t", "touch targets"),
    ("targets", "target management"),
    ("variables", "variable expansion"),
    ("error_handling", "error handling"),
])

add_pkg("gdb", [
    ("gdb", "debugger"), ("gdbserver", "remote debug"),
    ("-p", "attach to pid"), ("-c", "core file"),
    ("break", "breakpoints"), ("watch", "watchpoints"),
    ("run", "run program"), ("continue", "continue"),
    ("step", "step into"), ("next", "step over"),
    ("print", "print value"), ("backtrace", "stack trace"),
    ("info", "info commands"), ("list", "list source"),
    ("set/show", "settings"),
    ("frame", "stack frame"), ("thread", "thread ops"),
    ("disassemble", "disassembly"),
])

add_pkg("gcc", [
    ("gcc", "C compiler"), ("g++", "C++ compiler"),
    ("gfortran", "Fortran"),
    ("-o", "output file"), ("-c", "compile only"),
    ("-E", "preprocess only"), ("-S", "assembly only"),
    ("-Wall", "all warnings"), ("-Werror", "warnings as errors"),
    ("-g", "debug info"),
    ("-O0/-O2/-O3/-Os", "optimization levels"),
    ("-std", "language standard"),
    ("-I", "include path"), ("-L", "library path"),
    ("-l", "link library"),
    ("-shared", "shared library"),
    ("-fPIC/-fPIE", "position independent"),
    ("-D", "define macro"), ("-U", "undefine"),
    ("-static", "static link"),
    ("-march", "target arch"),
    ("-v", "verbose"),
    ("multi_file", "multi-file compile"),
    ("error_handling", "error handling"),
])

add_pkg("clang", [
    ("clang", "C compiler"), ("clang++", "C++ compiler"),
    ("clang-tidy", "static analysis"),
    ("clang-format", "code formatting"),
    ("clang-check", "syntax check"),
    ("clang-query", "AST query"),
    ("scan-build", "static analysis wrapper"),
    ("-o", "output"), ("-c", "compile only"),
    ("-g", "debug"), ("-Wall", "warnings"),
    ("-std", "language standard"),
])

add_pkg("binutils", [
    ("as", "assembler"), ("ld", "linker"),
    ("objdump", "disassemble"), ("objcopy", "copy/convert"),
    ("nm", "list symbols"), ("size", "section sizes"),
    ("strings", "print strings"), ("strip", "strip symbols"),
    ("readelf", "ELF info"), ("ar", "archive"),
    ("ranlib", "archive index"),
    ("addr2line", "address to line"),
    ("c++filt", "demangle C++"),
    ("gprof", "profiling"),
])

add_pkg("findutils", [
    ("find", "find files"), ("locate", "locate files"),
    ("updatedb", "update locate DB"),
    ("xargs", "build and execute"),
    ("-name", "by name"), ("-type", "by type"),
    ("-size", "by size"), ("-mtime", "by time"),
    ("-user", "by user"), ("-perm", "by permission"),
    ("-exec", "execute on match"),
    ("-delete", "delete matches"),
    ("-print", "print matches"),
    ("-maxdepth/-mindepth", "depth control"),
    ("-empty", "empty files/dirs"),
    ("-newer", "newer than"),
    ("-o/-a/-not", "logical operators"),
    ("xargs -n/-I/-P/-0", "xargs options"),
])

add_pkg("sed", [
    ("sed", "stream editor"),
    ("s/pattern/replace/", "substitution"),
    ("/pattern/d", "delete lines"),
    ("/pattern/p", "print lines"),
    ("-n", "quiet mode"),
    ("-e", "multiple expressions"),
    ("-f", "script file"),
    ("-i", "in-place edit"),
    ("-r/-E", "extended regex"),
    ("address ranges", "line addressing"),
    ("y/old/new/", "transliterate"),
])

add_pkg("procps-ng", [
    ("ps", "process status"),
    ("top", "process monitor"),
    ("free", "memory info"),
    ("pgrep", "grep processes"),
    ("pkill", "kill by name"),
    ("pmap", "memory map"),
    ("pwdx", "working directory"),
    ("uptime", "system uptime"),
    ("vmstat", "virtual memory stats"),
    ("w", "who and what"),
    ("watch", "periodic command"),
    ("pidwait", "wait for pid"),
    ("sysctl", "kernel params"),
    ("skill", "signal by criteria"),
    ("snice", "renice by criteria"),
    ("slabtop", "slab info"),
    ("tload", "load graph"),
])

add_pkg("psmisc", [
    ("fuser", "file users"),
    ("killall", "kill by name"),
    ("peekfd", "peek file descriptors"),
    ("prtstat", "process stats"),
    ("pstree", "process tree"),
])

add_pkg("util-linux", [
    ("mount/umount", "filesystem mount"),
    ("fdisk", "partition table"),
    ("partx", "partition management"),
    ("lsblk", "list block devices"),
    ("findmnt", "find mount"),
    ("blkid", "block device ID"),
    ("wipefs", "wipe filesystem"),
    ("losetup", "loop device"),
    ("swapon/swapoff", "swap"),
    ("dmesg", "kernel messages"),
    ("flock", "file locking"),
    ("fallocate", "allocate space"),
    ("rename", "rename files"),
    ("uuidgen", "UUID generate"),
    ("script/scriptreplay", "terminal recording"),
    ("hardlink", "hardlink files"),
    ("lslogins", "user login info"),
    ("lscpu", "CPU info"),
    ("lsipc", "IPC info"),
    ("lslocks", "file locks"),
    ("lsmem", "memory info"),
    ("lsns", "namespaces"),
    ("fstrim", "discard unused blocks"),
    ("setarch", "set architecture"),
    ("unshare", "unshare namespaces"),
    ("nsenter", "enter namespace"),
    ("taskset", "CPU affinity"),
    ("column", "columnate output"),
    ("hexdump", "hex dump"),
    ("cal", "calendar"),
    ("whereis", "locate binary"),
    ("kill", "send signal"),
    ("logger", "syslog message"),
    ("mcookie", "magic cookie"),
    ("namei", "path resolution"),
    ("more", "pager"),
    ("rev", "reverse lines"),
])

add_pkg("iproute2", [
    ("ip addr", "address"), ("ip link", "link"),
    ("ip route", "routing"), ("ip neigh", "neighbor"),
    ("ip rule", "routing rule"),
    ("ip netns", "network namespace"),
    ("ip tunnel", "tunnel"), ("ip monitor", "monitor"),
    ("ss", "socket stats"),
    ("tc", "traffic control"),
    ("bridge", "bridge control"),
    ("devlink", "device link"),
    ("lnstat", "link stats"),
    ("nstat", "network stats"),
    ("rdma", "RDMA"),
    ("tipc", "TIPC protocol"),
])

add_pkg("pciutils", [
    ("lspci", "list PCI devices"),
    ("setpci", "configure PCI"),
    ("update-pciids", "update PCI IDs"),
    ("-v/-vv", "verbose levels"),
    ("-k", "show kernel drivers"),
    ("-n/-nn", "numeric IDs"),
    ("-t", "tree view"),
    ("-s", "slot filter"),
    ("-d", "device filter"),
    ("-x", "hex dump"),
    ("-D", "show domains"),
])

add_pkg("iputils", [
    ("ping", "ICMP echo"), ("ping6", "ICMPv6 echo"),
    ("arping", "ARP ping"),
    ("tracepath", "path MTU discovery"),
    ("traceroute", "UDP traceroute"),
    ("clockdiff", "clock difference"),
    ("rdisc", "router discovery"),
])

add_pkg("podman", [
    ("run", "run container"), ("ps", "list containers"),
    ("images", "list images"), ("pull", "pull image"),
    ("build", "build image"), ("exec", "exec in container"),
    ("logs", "view logs"), ("rm/rmi", "remove container/image"),
    ("stop/start/restart", "lifecycle"),
    ("inspect", "inspect object"),
    ("commit", "commit container"),
    ("tag", "tag image"), ("push", "push image"),
    ("cp", "copy files"), ("top/stats", "monitoring"),
    ("port", "port mapping"),
    ("network", "network management"),
    ("volume", "volume management"),
    ("secret", "secret management"),
    ("pod", "pod management"),
    ("save/load", "save/load image"),
    ("export/import", "export/import"),
    ("system", "system management"),
    ("generate", "generate config"),
    ("healthcheck", "health check"),
    ("machine", "podman machine"),
    ("login/logout", "registry auth"),
    ("search", "search images"),
    ("info/version", "system info"),
])

add_pkg("dnf5-plugins", [
    ("dnf5 copr", "COPR plugin"),
    ("dnf5 builddep", "build deps"),
    ("dnf5 config-manager", "config manager"),
    ("dnf5 download", "download pkgs"),
    ("dnf5 needs-restarting", "needs restart"),
    ("dnf5 repoclosure", "repo closure"),
    ("dnf5 repograph", "repo graph"),
    ("dnf5 repomanage", "repo manage"),
    ("dnf5 reposync", "repo sync"),
])

add_pkg("weston", [
    ("weston", "compositor"),
    ("weston-terminal", "terminal emulator"),
    ("weston-info", "display info"),
    ("weston-debug", "debug tool"),
    ("--backend", "select backend"),
    ("--shell", "select shell"),
    ("--tty", "TTY selection"),
    ("--modules", "load modules"),
])

add_pkg("labwc", [
    ("labwc", "compositor"),
    ("-C/--config", "config file"),
    ("-s", "startup command"),
    ("-d", "debug logging"),
    ("-v", "version"),
])

add_pkg("sddm", [
    ("sddm", "display manager"),
    ("sddm-greeter", "login greeter"),
    ("sddm.conf", "configuration"),
])

add_pkg("systemd-timesyncd", [
    ("timedatectl", "time/date control"),
    ("systemd-timesyncd", "NTP sync service"),
    ("timesyncd.conf", "configuration"),
])

# Library packages
add_pkg("audit", [
    ("auditctl", "audit control"),
    ("aureport", "audit reports"),
    ("ausearch", "audit search"),
    ("autrace", "audit trace"),
    ("augenrules", "generate rules"),
    ("aulast", "audit login"),
    ("aulastlog", "audit lastlog"),
    ("ausyscall", "syscall lookup"),
])

add_pkg("glibc", [
    ("ldd", "shared lib deps"),
    ("ldconfig", "lib cache"),
    ("locale", "locale info"),
    ("localedef", "compile locale"),
    ("iconv", "charset convert"),
    ("getconf", "system config"),
    ("getent", "database entries"),
    ("gencat", "message catalog"),
])

add_pkg("glib", [
    ("gsettings", "GSettings"),
    ("gdbus", "D-Bus"),
    ("gio", "GIO commands"),
    ("gresource", "resource compiler"),
    ("glib-compile-schemas", "schema compiler"),
])

add_pkg("lvm2", [
    ("lvm", "LVM management"),
    ("pvcreate/pvdisplay/pvs/pvremove", "physical volumes"),
    ("vgcreate/vgdisplay/vgs/vgremove", "volume groups"),
    ("lvcreate/lvdisplay/lvs/lvremove", "logical volumes"),
])

add_pkg("libxml2", [
    ("xmllint", "XML validator/formatter"),
    ("xmlcatalog", "XML catalog"),
])

add_pkg("libxslt", [
    ("xsltproc", "XSLT processor"),
])

add_pkg("sqlite", [
    ("sqlite3", "SQLite shell"),
    ("sqldiff", "diff databases"),
    ("sqlite3_analyzer", "analyze DB"),
])

add_pkg("nettle", [
    ("nettle-hash", "hash utility"),
    ("nettle-lfib-stream", "random stream"),
    ("nettle-pbkdf2", "PBKDF2"),
    ("pkcs1-conv", "PKCS#1 convert"),
    ("sexp-conv", "S-expression convert"),
])

add_pkg("gnutls", [
    ("gnutls-cli", "TLS client"),
    ("gnutls-serv", "TLS server"),
    ("certtool", "certificate tool"),
    ("psktool", "PSK tool"),
    ("srptool", "SRP tool"),
])

add_pkg("p11-kit", [
    ("p11-kit", "PKCS#11 tool"),
    ("trust", "trust module"),
])

add_pkg("pam", [
    ("faillock", "failure lock"),
    ("mkhomedir_helper", "home dir helper"),
    ("pam_timestamp_check", "timestamp check"),
    ("unix_chkpwd", "password check"),
    ("unix_update", "password update"),
])

add_pkg("cracklib", [
    ("cracklib-check", "check password"),
    ("cracklib-format", "format dictionary"),
    ("cracklib-packer", "pack dictionary"),
    ("cracklib-unpacker", "unpack dictionary"),
])

add_pkg("cryptsetup", [
    ("cryptsetup", "dm-crypt management"),
    ("luksFormat/luksOpen/luksClose", "LUKS operations"),
    ("integritysetup", "integrity setup"),
    ("veritysetup", "verity setup"),
])

add_pkg("acl", [
    ("getfacl", "get ACL"), ("setfacl", "set ACL"),
    ("chacl", "change ACL"),
])

add_pkg("attr", [
    ("getfattr", "get attributes"),
    ("setfattr", "set attributes"),
])

add_pkg("kmod", [
    ("lsmod", "list modules"),
    ("modinfo", "module info"),
    ("modprobe", "load/unload module"),
    ("insmod", "insert module"),
    ("rmmod", "remove module"),
    ("depmod", "dependency gen"),
])

add_pkg("kbd", [
    ("dumpkeys", "dump keymap"),
    ("showkey", "show keycodes"),
    ("loadkeys", "load keymap"),
    ("setfont", "set console font"),
])

add_pkg("krb5", [
    ("kinit", "get ticket"),
    ("klist", "list tickets"),
    ("kdestroy", "destroy tickets"),
    ("kpasswd", "change password"),
    ("kadmin", "admin tool"),
])

add_pkg("popt", [
    ("popt", "option parsing dev library"),
])

add_pkg("mpfr", [
    ("mpfr", "multi-precision FP dev library"),
])

add_pkg("gmp", [
    ("gmp", "GNU MP dev library"),
])

add_pkg("mpc", [
    ("mpc", "complex number dev library"),
])

add_pkg("isl", [
    ("isl", "integer set library"),
])

add_pkg("readline", [
    ("readline", "line-editing dev library"),
])

# ============================================================
# Test extraction logic
# ============================================================

def parse_dir_name(dir_name):
    """Parse test directory name to extract tested features.
    Format: test_{pkg}_{feature1}__{feature2}___flag
    __ = functional group separator
    ___ = specific flag/parameter indicator
    """
    # Remove test_ prefix
    name = dir_name
    if name.startswith("test_"):
        name = name[len("test_"):]
    
    # Remove package prefix (first segment)
    parts = name.split("__", 1)
    if len(parts) > 1:
        name = parts[1]
    
    # Split by __ for feature groups, ___ for flags
    features = []
    # First split by triple underscore for flags
    segments = re.split(r'_{3,}', name)
    for seg in segments:
        # Then split by double underscore for feature groups
        sub = re.split(r'_{2,}', seg)
        for s in sub:
            s = s.strip('_').replace('_', ' ')
            if s and len(s) > 1:
                features.append(s)
    
    return features

def extract_tested_from_rlrun(test_sh_path):
    """Extract commands/features from rlRun calls in a test script."""
    if not test_sh_path.exists():
        return set()
    try:
        content = test_sh_path.read_text(encoding='utf-8')
    except:
        return set()
    
    found = set()
    # Find all rlRun commands
    for m in re.finditer(r'rlRun\s+"([^"]*)"\s+\d+\s+"([^"]*)"', content):
        cmd = m.group(1).strip()
        desc = m.group(2).strip()
        
        # Extract binary names
        words = cmd.split()
        if not words:
            continue
        
        first = words[0]
        # Skip infrastructure commands
        if first in ('cd', 'echo', 'mkdir', 'rm', 'touch', 'printf', 'test', 
                      'ls', 'ln', 'sudo', 'true', 'false', 'chmod', 'chown',
                      'cat', 'grep', 'diff', 'if', '[', '!', 'TmpDir=$(mktemp'):
            continue
        
        found.add(first)
        
        # Extract subcommands for known tools
        if first in ('git', 'podman', 'dnf5', 'tmux', 'ip', 'systemctl', 
                      'rpmbuild', 'lvm', 'curl', 'wget', 'wget2', 'openssl',
                      'docker', 'rpm'):
            if len(words) >= 2:
                sub = words[1]
                if not sub.startswith('-'):
                    found.add(f"{first} {sub}")
        
        # Extract flags
        for w in words[1:]:
            if w.startswith('-') and len(w) <= 5 and not w.startswith('--'):
                found.add(w)
    
    return found

def analyze_package(pkg_dir):
    """Analyze a package's test coverage comprehensively."""
    pkg_name = pkg_dir.name
    test_dirs = sorted([d for d in pkg_dir.iterdir() if d.is_dir() and d.name.startswith('test_')])
    
    all_tested_features = set()
    test_list = []
    
    for td in test_dirs:
        # Parse directory name
        dir_features = parse_dir_name(td.name)
        
        # Parse test.sh content
        test_sh = td / "test.sh"
        cmd_features = extract_tested_from_rlrun(test_sh)
        
        combined = set(dir_features) | cmd_features
        all_tested_features.update(combined)
        
        test_list.append({
            "dir": td.name,
            "dir_features": sorted(dir_features),
            "cmd_features": sorted(cmd_features),
            "all_tested": sorted(combined),
        })
    
    # Known features for this package
    known = PACKAGE_FEATURES.get(pkg_name, [])
    known_names = {f[0] for f in known}
    
    # Coverage calculation
    tested_names = set()
    # Normalize tested features
    for f in all_tested_features:
        fl = f.lower()
        for kn in known_names:
            kl = kn.lower()
            if fl == kl or fl in kl or kl in fl:
                tested_names.add(kn)
                break
    
    missing = known_names - tested_names
    
    coverage_pct = 0
    if known_names:
        coverage_pct = round(100 * len(known_names - missing) / len(known_names), 1)
    
    return {
        "package": pkg_name,
        "test_count": len(test_dirs),
        "tested_raw": sorted(all_tested_features),
        "tested_mapped": sorted(tested_names),
        "known_commands": sorted(known_names),
        "missing_commands": sorted(missing),
        "coverage_pct": coverage_pct,
        "has_lib_sh": (pkg_dir / "lib.sh").exists(),
        "test_list": test_list,
    }


def main():
    results = []
    for pkg_dir in sorted(PKGS_DIR.iterdir()):
        if not pkg_dir.is_dir():
            continue
        results.append(analyze_package(pkg_dir))
    
    # Categorize
    with_ref = [r for r in results if PACKAGE_FEATURES.get(r["package"])]
    no_ref = [r for r in results if not PACKAGE_FEATURES.get(r["package"])]
    
    # Sort by coverage
    with_ref.sort(key=lambda r: r["coverage_pct"])
    no_ref.sort(key=lambda r: r["test_count"], reverse=True)
    
    print("=" * 90)
    print("  pkgs 功能测试覆盖率分析报告 (v2)")
    print("=" * 90)
    print(f"  总包数: {len(results)}")
    print(f"  有功能参考的包: {len(with_ref)}")
    print(f"  无功能参考的包: {len(no_ref)}")
    print()
    
    # === Section 1: Packages needing improvement ===
    print("=" * 90)
    print("  【重点改进】覆盖率 < 60% 的包")
    print("=" * 90)
    low = [r for r in with_ref if r["coverage_pct"] < 60]
    if low:
        for r in low:
            missing_preview = ", ".join(r["missing_commands"][:8])
            more = "..." if len(r["missing_commands"]) > 8 else ""
            print(f"\n--- {r['package']} (覆盖率: {r['coverage_pct']}%, 测试={r['test_count']}) ---")
            print(f"  已覆盖: {', '.join(r['tested_mapped'][:15])}")
            print(f"  缺失: {missing_preview}{more} ({len(r['missing_commands'])} total)")
    
    # === Section 2: Moderate coverage ===
    print("\n" + "=" * 90)
    print("  【中等覆盖】覆盖率 60%-89% 的包")
    print("=" * 90)
    med = [r for r in with_ref if 60 <= r["coverage_pct"] < 90]
    for r in med:
        print(f"  {r['package']:<20} 覆盖率: {r['coverage_pct']}%  缺失: {', '.join(r['missing_commands'][:5])}")
    
    # === Section 3: Good coverage ===
    print("\n" + "=" * 90)
    print("  【覆盖良好】覆盖率 >= 90% 的包")
    print("=" * 90)
    good = [r for r in with_ref if r["coverage_pct"] >= 90]
    for r in good:
        print(f"  {r['package']:<20} 覆盖率: {r['coverage_pct']}%  ({r['test_count']} tests) 缺失: {', '.join(r['missing_commands']) if r['missing_commands'] else '无'}")
    
    # === Section 4: No reference packages ===
    print("\n" + "=" * 90)
    print("  【需人工评估】无功能参考的包 (按测试数量排序)")
    print("=" * 90)
    print(f"  {'Package':<30} {'Tests':<8} {'已有功能点':<15}")
    print(f"  {'-'*30} {'-'*8} {'-'*30}")
    for r in no_ref[:50]:
        features = ', '.join(r['tested_raw'][:6])
        more = f" ... +{len(r['tested_raw'])-6}" if len(r['tested_raw']) > 6 else ""
        print(f"  {r['package']:<30} {r['test_count']:<8} {features}{more}")
    
    print(f"\n  ... 还有 {len(no_ref)-50} 个包省略")
    
    # === Section 5: Library packages (1 test, only file check) ===
    print("\n" + "=" * 90)
    print("  【库文件验证型】仅验证 .so 文件存在 (仅1个测试)")
    print("=" * 90)
    lib_only = [r for r in results if r["test_count"] == 1 and 
                all(any(x in f for f in r["tested_raw"]) 
                    for x in ['ls', 'pkg-config'])]
    print(f"  共 {len(lib_only)} 个纯库文件验证型包（无功能测试）")
    for r in lib_only:
        print(f"    - {r['package']}")
    
    # === Section 6: Packages needing test case splitting ===
    print("\n" + "=" * 90)
    print("  【需要拆分】复杂测试用例识别 (单个测试含 5+ 个独立功能)")
    print("=" * 90)
    for r in results[:]:
        if r["test_count"] <= 1:
            continue
        # Check if any test dir groups many features
        for t in r.get("test_list", []):
            if len(t["all_tested"]) >= 5:
                print(f"  {r['package']:<25} {t['dir']:<60} 包含 {len(t['all_tested'])} 个功能点")
                if len(t["all_tested"]) >= 8:
                    print(f"    → 建议拆分为 {len(t['all_tested'])//2} 个独立测试")
    
    # Save JSON
    output_path = Path(os.environ.get("TEMP", "/tmp")) / "coverage_analysis_v2.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n详细JSON: {output_path}")

if __name__ == "__main__":
    main()