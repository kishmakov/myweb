<!-- Header: How to use CLion for LLDB development -->
<!-- Tag: apple -->
<!-- Tag: cpp -->
<!-- Summary: Tricks for comfy environment setup -->
<!-- Summary: for building and debugging LLDB with CLion. -->

## Check out

There are two main repositories for llvm-project: core one 
[github.com/llvm/llvm-project](github.com/llvm/llvm-project) 
and another, managed by Apple 
[github.com/apple/llvm-project](github.com/apple/llvm-project). 
Apparently, core repo serves as an accumulating base, while Apple makes its edits 
through its version (for example, stupid rename of `master` branch firstly 
happened in Apple's repo).

For building `lldb` with Swift support, one needs to check out Apple's repo. 
The resulting checkout should look similar to 

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

If, for some reasons, you want to manage both origins, you could add to 
`swift-project/llvm-project/.git/config` something like:

```ini
[remote "llvm"]
	url = git@github.com:llvm/llvm-project.git
	fetch = +refs/heads/*:refs/remotes/llvm/*
```

It could help preserve disk space since llvm is big.

[comment]: <> (In order to utils/update-checkout --scheme release/5.3)

## Project load and build