# curl 功能测试覆盖详情

共 **6** 个测试套，**11** 个测试点

| Test Suite | Test Case | Test Point |
|------------|-----------|------------|
| test_curl_basic_download | 2 cases | curl 下载示例页面 |
| | | curl -I: 仅获取响应头 |
| test_curl_output_options | 2 cases | curl -o: 输出到文件 |
| | | curl -O: 远程文件名 |
| test_curl_verbose_mode | 2 cases | curl -v: 详细模式 |
| | | curl -s: 静默模式 |
| test_curl_basic | 3 cases | curl -L: 跟随重定向 |
| | | curl -k: 忽略SSL证书 |
| | | curl --connect-timeout: 连接超时 |
| test_curl_wcurl | 1 cases | wcurl 帮助 |
| test_curl_error_handling | 1 cases | curl: 无效选项 |
