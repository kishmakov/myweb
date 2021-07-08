<!-- Header: CLion for LLDB Development -->
<!-- Tag: apple -->
<!-- Tag: cpp -->
<!-- Summary: Tricks for comfy environment setup -->
<!-- Summary: for building and debugging LLDB with CLion. -->

## Check Out

There are two main repositories for llvm-project: core one 
[github.com/llvm/llvm-project](https://github.com/llvm/llvm-project) 
and another, managed by Apple 
[github.com/apple/llvm-project](https://github.com/apple/llvm-project). 
Apple uses core repository as a base for its development branches and 
upstreams its fixes. For space optimization, it is convenient to check 
out both `llvm` origins into one location. 

For building `lldb` with Swift support, one needs to check out Swift's repo 
[github.com/apple/swift](https://github.com/apple/swift) and to clone the rest with 
command `./swift/utils/update-checkout --clone-with-ssh`.
Resulting checkout should look similar to 

```plaintext
swift-project/
├── build
├── cmark
├── indexstore-db
├── llbuild
├── llvm-project
├── ninja
├── sourcekit-lsp
├── swift
├── swift-argument-parser
├── ...
├── swiftpm
└── yams
```

Additional remotes are supposed to be mentioned in `./llvm-project/.git/config`
```ini
[remote "llvm"]
	url = ssh://git@github.com/llvm/llvm-project.git
	fetch = +refs/heads/*:refs/remotes/llvm/*
[remote "jb"]
    url = ssh://git@git.jetbrains.team/llvm/llvm-project.git
    fetch = +refs/heads/*:refs/remotes/jb/*
```
and to be fetched from within `./llvm-project` via `git fetch jb`.

[comment]: <> (In order to utils/update-checkout --scheme release/5.3)

## Project load and build

Swift bundle is supposed to be built with `./swift/utils/build-toolchain`. 
Inside it delegates the job to the main building script `./swift/utils/build-script`. 
By default `build-toolchain` could generate excessive command, one could 
lighten it to something similar to
```bash
SKIP_XCODE_VERSION_CHECK=1 ./swift/utils/build-script --swift-darwin-supported-archs="x86_64" \
  --lldb --llbuild --libcxx --release-debuginfo --compiler-vendor=apple --lldb-no-debugserver \ 
  --lldb-use-system-debugserver --lldb-build-type=Debug  --build-ninja \
  '--extra-cmake-options=-DLLDB_FRAMEWORK_COPY_SWIFT_RESOURCES=0 -DCMAKE_C_FLAGS="-gline-tables-only" -DCMAKE_CXX_FLAGS="-gline-tables-only"' \
   --build-subdir=buildbot_osx --swift-enable-ast-verifier=0 --no-swift-stdlib-assertions \
   --skip-test-lldb --skip-test-swift --skip-test-llbuild --skip-test-lldb --skip-test-cmark \
   --sccache
```

After project is built `./llvm-project/llvm` should be opened in CLion. To import 
project, next CMake options should be used (*Preferences > Build, Execution, Deployment > CMake*):

```plaintext
-GNinja
-DLLVM_ENABLE_PROJECTS="libcxx;clang;lldb"
-DCMAKE_BUILD_TYPE="DEBUG"
-DCMAKE_CXX_FLAGS="-g -O0"
-DCMAKE_CXX_FLAGS_RELEASE="-g -O0"
-DLLVM_TARGETS_TO_BUILD="X86;AArch64"
-DLLVM_ENABLE_ASSERTIONS=YES
-DLLVM_ENABLE_LIBXML2=NO
-DLLVM_INCLUDE_EXAMPLES=OFF
-DLLVM_INCLUDE_BENCHMARKS=OFF
-DLLVM_INCLUDE_TESTS=OFF
-DLLVM_TOOLS_BINARY_DIR=/Users/kirill.shmakov/Repos/swift-project/build/buildbot_osx/llvm-macosx-x86_64/bin
-DLLDB_BUILD_FRAMEWORK=YES
-DLLDB_USE_SYSTEM_DEBUGSERVER=OFF
-DLLDB_ENABLE_LIBEDIT=NO
-DLLDB_ENABLE_CURSES=NO
-DLLDB_ENABLE_LZMA=NO
-DLLVM_EXTERNAL_SWIFT_SOURCE_DIR=/Users/kirill.shmakov/Repos/swift-project/swift
```

After import completed it is possible to build `lldb` with local changes 
from within CLion (just select *lldb* run configuration). Results would 
be stored at `./llvm-project/llvm/cmake-build-debug`. 