$resultFile = "$env:TEMP\pkg_analysis.csv"
$pkgsDir = "E:\code\openruyi-autotest\tests\functional\pkgs"
"pkg,test_dirs,total_rlRun,total_rlAssert,avg_rlRun,max_rlRun,has_lib_sh" | Out-File $resultFile -Encoding UTF8
foreach ($pkgDir in (Get-ChildItem $pkgsDir -Directory | Sort-Object Name)) {
    $pkg = $pkgDir.Name
    $testDirs = @(Get-ChildItem $pkgDir.FullName -Directory)
    $totalRlRun = 0; $totalRlAssert = 0; $maxRlRun = 0
    $hasLibSh = Test-Path (Join-Path $pkgDir.FullName "lib.sh")
    foreach ($td in $testDirs) {
        $testSh = Join-Path $td.FullName "test.sh"
        if (Test-Path $testSh) {
            $content = Get-Content $testSh -Raw
            $rc = ([regex]::Matches($content, '\srlRun\s+"')).Count
            $ac = ([regex]::Matches($content, 'rlAssert')).Count
            $totalRlRun += $rc; $totalRlAssert += $ac
            if ($rc -gt $maxRlRun) { $maxRlRun = $rc }
        }
    }
    $avg = if ($testDirs.Count -gt 0) { [math]::Round($totalRlRun / $testDirs.Count, 1) } else { 0 }
    "$pkg,$($testDirs.Count),$totalRlRun,$totalRlAssert,$avg,$maxRlRun,$hasLibSh" | Out-File $resultFile -Append -Encoding UTF8
}
Write-Host "Analysis complete: $resultFile"
$data = Import-Csv $resultFile
$only1 = ($data | Where-Object { [int]$_.test_dirs -eq 1 }).Count
$few2_5 = ($data | Where-Object { [int]$_.test_dirs -ge 2 -and [int]$_.test_dirs -le 5 }).Count
$med6_15 = ($data | Where-Object { [int]$_.test_dirs -ge 6 -and [int]$_.test_dirs -le 15 }).Count
$many16 = ($data | Where-Object { [int]$_.test_dirs -ge 16 }).Count
Write-Host "=== 测试数量分布 ==="
Write-Host "1个测试: $only1 个包"
Write-Host "2-5个: $few2_5 个包"
Write-Host "6-15个: $med6_15 个包"
Write-Host "16+个: $many16 个包"