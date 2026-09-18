# tmux 功能测试覆盖详情

共 **22** 个测试套，**179** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_tmux_server_management | 8 cases | start-server: start tmux server |
| | | list-sessions: initial state |
| | | has-session: check nonexistent |
| | | list-clients: list connected clients |
| | | list-commands: list all commands |
| | | list-commands: filter specific command |
| | | list-commands: format output |
| | | server-access -l: list access |
| test_tmux_session_creation_and_management | 21 cases | new-session -d: create detached session |
| | | has-session: verify session exists |
| | | new-session -d: with start directory |
| | | has-session: verify sess2 exists |
| | | new-session -e: set environment |
| | | new-session -F: format output |
| | | new-session: set dimensions |
| | | new-session -A: attach if exists |
| | | list-sessions: list all sessions |
| | | list-sessions -F: formatted |
| | | rename-session: rename sess2 |
| | | has-session: verify renamed session |
| | | lock-session: lock session |
| | | switch-client -t: switch to session |
| | | attach-session -d: attach and detach others |
| | | detach-client -P |
| | | detach-client -a: all in session |
| | | suspend-client: suspend client |
| | | lock-client: lock client |
| | | refresh-client -S: status line only |
| | | refresh-client -L: lease |
| test_tmux_window_management | 29 cases | new-window: create window |
| | | new-window -d: detached |
| | | new-window -c: with directory |
| | | new-window -e: with env |
| | | list-windows: list all windows |
| | | list-windows -a: all sessions |
| | | list-windows -F: formatted |
| | | select-window: by name |
| | | select-window: by index |
| | | select-window -l: last window |
| | | select-window -n: next |
| | | select-window -p: previous |
| | | rename-window: rename window |
| | | next-window: next |
| | | previous-window: prev |
| | | last-window: last |
| | | move-window -a: after |
| | | move-window -b: before |
| | | swap-window |
| | | link-window: link window |
| | | unlink-window: unlink |
| | | kill-window: create temp window |
| | | kill-window: kill window |
| | | rotate-window: rotate |
| | | rotate-window -D: downward |
| | | respawn-window -k: respawn |
| | | resize-window: set size |
| | | resize-window -U: up |
| | | resize-window -D: down |
| test_tmux_pane_management | 38 cases | split-window: horizontal split |
| | | split-window -h: vertical split |
| | | split-window -v: vertical explicit |
| | | split-window -l: with size |
| | | split-window -d: don't focus |
| | | split-window -f: full size |
| | | split-window -b: before |
| | | split-window -I: create empty pane |
| | | list-panes: list panes |
| | | list-panes -as: all panes |
| | | list-panes -F: formatted |
| | | display-panes: show pane IDs |
| | | select-pane: by ID |
| | | select-pane -l: last pane |
| | | select-pane -U: up |
| | | select-pane -D: down |
| | | select-pane -L: left |
| | | select-pane -R: right |
| | | resize-pane -y: height |
| | | resize-pane -x: width |
| | | resize-pane -U: up |
| | | resize-pane -D: down |
| | | resize-pane -L: left |
| | | resize-pane -R: right |
| | | resize-pane -Z: zoom |
| | | break-pane -d: break pane to new window |
| | | join-pane: join pane back |
| | | move-pane: move pane |
| | | swap-pane: swap panes |
| | | last-pane: switch to last pane |
| | | kill-pane: create temp pane |
| | | kill-pane: kill pane |
| | | kill-pane -a: kill all but current |
| | | capture-pane -p: print to stdout |
| | | capture-pane: range capture |
| | | capture-pane -J: join lines |
| | | pipe-pane -o: pipe output |
| | | respawn-pane -k: respawn |
| test_tmux_layout_management | 7 cases | select-layout: even-horizontal |
| | | select-layout: even-vertical |
| | | select-layout: main-horizontal |
| | | select-layout: main-vertical |
| | | select-layout: tiled |
| | | next-layout: cycle layouts |
| | | previous-layout: prev layout |
| test_tmux_buffer_management | 13 cases | set-buffer -b: named buffer |
| | | set-buffer: direct data |
| | | set-buffer -a: append |
| | | list-buffers: list all buffers |
| | | list-buffers -F: formatted |
| | | show-buffer: show buffer contents |
| | | paste-buffer: paste buffer |
| | | paste-buffer -d: delete after paste |
| | | delete-buffer: create temp buffer |
| | | delete-buffer: delete buffer |
| | | save-buffer: create buffer |
| | | save-buffer: save to file |
| | | load-buffer: load from file |
| test_tmux_key_bindings_and_input | 13 cases | list-keys: list all keys |
| | | list-keys -T: prefix table |
| | | list-keys -T: root table |
| | | list-keys -a: all keys |
| | | list-keys -N: with notes |
| | | bind-key -n: bind to key |
| | | unbind-key -n: unbind key |
| | | bind-key -T: bind in table |
| | | unbind-key -T: unbind in table |
| | | send-keys: send text |
| | | send-keys -l: literal |
| | | send-keys -H: hex |
| | | send-prefix: send prefix key |
| test_tmux_options_and_settings | 10 cases | set-option -g: global |
| | | set-option -a: append |
| | | set-option: mouse on |
| | | set-option -s: server option |
| | | set-window-option: monitor activity |
| | | set-window-option -g: global |
| | | show-options -g: global options |
| | | show-options -s: server options |
| | | show-window-options: window options |
| | | show-window-options -g: global window options |
| test_tmux_environment_variables | 5 cases | set-environment -g: global env |
| | | set-environment: session env |
| | | set-environment -gur: update then remove |
| | | show-environment -g: global env |
| | | show-environment: session env |
| test_tmux_hooks | 5 cases | set-hook: session-created |
| | | set-hook: client-attached |
| | | show-hooks -g: global hooks |
| | | set-hook -gu: remove global hook |
| | | set-hook -gu: remove hook |
| test_tmux_messages_and_display | 5 cases | display-message: show message |
| | | display-message -p: print format |
| | | show-messages: message log |
| | | display-popup -C: close popup |
| | | clear-history: clear pane history |
| test_tmux_conditional_and_shell_execution | 5 cases | if-shell: true condition |
| | | run-shell: run shell command |
| | | run-shell -b: background |
| | | command-prompt: open prompt |
| | | confirm-before: confirm dialog |
| test_tmux_source_and_configuration | 1 cases | source-file: source config |
| test_tmux_copy_mode | 1 cases | copy-mode: enter copy mode |
| test_tmux_find_window | 1 cases | find-window: search windows |
| test_tmux_choose_commands_interactive | 2 cases | choose-tree -G: tree display |
| | | choose-client: client selection |
| test_tmux_clock_mode | 1 cases | clock-mode: show clock |
| test_tmux_lock_management | 2 cases | lock-server: lock server |
| | | lock-session: lock session |
| test_tmux_show_prompt_history | 2 cases | show-prompt-history: prompt history |
| | | clear-prompt-history: clear prompt history |
| test_tmux_waitfor_event_channels | 1 cases | wait-for -L: lock channel |
| test_tmux_cleanup_kill_sessions | 7 cases | kill-session: kill renamed_sess |
| | | kill-session: kill sess_fmt |
| | | kill-session: kill sess_sz |
| | | kill-session: kill sess_flags |
| | | kill-session: kill sess_env |
| | | kill-session: kill main test session |
| | | kill-server: terminate server |
| test_tmux_error_handling | 2 cases | Error: nonexistent session |
| | | Error: invalid option |
