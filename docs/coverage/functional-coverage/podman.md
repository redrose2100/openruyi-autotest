# podman 功能测试覆盖详情

共 **7** 个测试套，**16** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_podman_image_operations | 2 cases | podman images: list images |
| | | podman image list |
| test_podman_container_operations | 3 cases | podman ps: list containers |
| | | podman ps -a: all containers |
| | | podman container list |
| test_podman_network_operations | 2 cases | podman network ls |
| | | podman network inspect |
| test_podman_volume_operations | 1 cases | podman volume ls |
| test_podman_system_operations | 2 cases | podman system info |
| | | podman system df: disk usage |
| test_podman_help_commands | 5 cases | podman manifest help |
| | | podman healthcheck help |
| | | podman events help |
| | | podman pod list |
| | | podman-remote help |
| test_podman_error_handling | 1 cases | podman: invalid command |
