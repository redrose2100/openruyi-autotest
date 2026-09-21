$pkgs = @('libaio','libarchive','json-c','jitterentropy','ncurses','libcap','lvm2','kbd','beakerlib','iproute2')
foreach ($pkg in $pkgs) {
    Write-Host "===== $pkg ====="
    $dirs = Get-ChildItem "E:\code\openruyi-autotest\tests\functional\pkgs\$pkg" -Directory -ErrorAction SilentlyContinue
    if ($dirs) {
        $testSh = Join-Path $dirs[0].FullName "test.sh"
        if (Test-Path $testSh) {
            $content = Get-Content $testSh -Raw
            if ($content -match '(?s)rlPhaseStartTest\s+"([^"]+)"(.*?)rlPhaseEnd') {
                $name = $Matches[1]
                $body = $Matches[2]
                $cmds = [regex]::Matches($body, 'rlRun\s+"([^"]+)"') | ForEach-Object { $_.Groups[1].Value }
                Write-Host "  Test: $name"
                foreach ($c in $cmds) { Write-Host "    > $c" }
            }
        }
    }
    Write-Host ""
}