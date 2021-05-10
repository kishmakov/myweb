<!-- Header: CLion for LLDB Development -->
<!-- Tag: apple -->
<!-- Tag: cpp -->
<!-- Summary: Tricks for comfy environment setup -->
<!-- Summary: for building and debugging LLDB with CLion. -->

## Check Out

There are two main repositories for llvm-project: core one 
[github.com/llvm/llvm-project](github.com/llvm/llvm-project) 
and another, managed by Apple 
[github.com/apple/llvm-project](github.com/apple/llvm-project). 
Apple uses core repository as a base for its development branches and 
upstreams its fixes. For space optimization, it is convenient to check 
out both `llvm` origins into one location. 

For building `lldb` with Swift support, one needs to check out Swift's repo 
[github.com/apple/swift](github.com/apple/swift) and to clone the rest with 
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
and to be fetched from within `llvm-project` via `git fetch jb`.

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
