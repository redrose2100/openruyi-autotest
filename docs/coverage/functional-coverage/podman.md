# podman 功能测试覆盖详情

共 **7** 个测试用例，**16** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| podman | test_podman_image_operations | podman images: list images |
| | | podman image list |
| podman | test_podman_container_operations | podman ps: list containers |
| | | podman ps -a: all containers |
| | | podman container list |
| podman | test_podman_network_operations | podman network ls |
| | | podman network inspect |
| podman | test_podman_volume_operations | podman volume ls |
| podman | test_podman_system_operations | podman system info |
| | | podman system df: disk usage |
| podman | test_podman_help_commands | podman manifest help |
| | | podman healthcheck help |
| | | podman events help |
| | | podman pod list |
| | | podman-remote help |
| podman | test_podman_error_handling | podman: invalid command |
