# curl 功能测试覆盖详情

共 **6** 个测试用例，**11** 个测试点

| 软件包 | 测试用例 | 测试点 |
|--------|----------|--------|
| curl | test_curl_basic_download | curl 下载示例页面 |
| | | curl -I: 仅获取响应头 |
| curl | test_curl_output_options | curl -o: 输出到文件 |
| | | curl -O: 远程文件名 |
| curl | test_curl_verbose_mode | curl -v: 详细模式 |
| | | curl -s: 静默模式 |
| curl | test_curl_basic | curl -L: 跟随重定向 |
| | | curl -k: 忽略SSL证书 |
| | | curl --connect-timeout: 连接超时 |
| curl | test_curl_wcurl | wcurl 帮助 |
| curl | test_curl_error_handling | curl: 无效选项 |
