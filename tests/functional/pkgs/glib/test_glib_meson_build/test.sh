#!/bin/bash
# Functional test: glib - meson build integration
# Verifies glib-2.0, gobject-2.0, gio-2.0 can be found via pkg-config
# in a meson build project, confirming devel packages are functional.
# Beakerlib-based test with lifecycle management.
# Shared suite setup/cleanup via ../lib.sh (install once, uninstall once)

. /usr/share/beakerlib/beakerlib.sh || exit 1
. "$(dirname "$0")/../lib.sh"

rlJournalStart
    rlPhaseStartSetup "Environment setup"
        glibSetup
        TmpDir=$(mktemp -d)
        rlRun "cd $TmpDir" 0 "Enter temporary test directory"
        # glibSetup only installs the glib runtime package; this test also needs
        # the build toolchain and the devel package that provides the pkg-config
        # file. openRuyi names are ninja (not ninja-build) and glib-devel
        # (not glib2-devel). Its repo needs --nogpgcheck --setopt=sslverify=0.
        echo "${TEST_SERVER_1_PASSWORD:-openruyi}" | sudo -S dnf install -y \
            --nogpgcheck --setopt=sslverify=0 \
            meson ninja glib-devel pkgconf-pkg-config gcc-c++ 2>&1 | tail -5
        rlRun "command -v meson" 0 "meson is available"
        rlRun "pkg-config --exists glib-2.0" 0 "glib-2.0 pkg-config file is available"
    rlPhaseEnd

    rlPhaseStartTest "meson_build_with_glib"
        # Write a minimal meson.build that depends on glib/gobject/gio
        cat > meson.build << 'MESON_EOF'
project('test_glib', 'c',
        version : '0.1.0',
        license : 'MIT',
        default_options : [
          'b_asneeded=True',
          'b_lundef=True',
          'c_std=gnu11',
          'warning_level=2',
        ],
        meson_version : '>=0.37.0')

glib = dependency('glib-2.0', version : '>=2.44')
gobject = dependency('gobject-2.0', version : '>=2.44')
gio = dependency('gio-2.0', version : '>=2.44')
MESON_EOF
        rlRun "cat meson.build" 0 "Display generated meson.build"

        # Run meson setup to verify dependencies resolve
        rlRun "meson setup builddir" 0 "Run meson setup with glib dependencies"
        rlRun "test -f builddir/build.ninja" 0 "Verify build.ninja was generated"

        # Check meson output references glib
        rlRun "meson introspect builddir --dependencies | grep -i glib" 0 "Verify glib dependency detected"
    rlPhaseEnd

    rlPhaseStartCleanup "Clean up test environment"
        rlRun "cd /" 0 "Leave test directory"
        if [ -n "$TmpDir" ] && [ -d "$TmpDir" ]; then
            rlRun "rm -rf $TmpDir" 0 "Clean up temporary test directory"
        fi
        # glib Package managed by lib.sh's reference counting auto-uninstall
    rlPhaseEnd

    rlJournalPrintText
rlJournalEnd