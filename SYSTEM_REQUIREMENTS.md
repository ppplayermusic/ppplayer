# PPPlayer System Requirements

This document outlines the system requirements for running and building PPPlayer across all officially supported platforms. These requirements are derived directly from the project's build configurations, native dependencies, and release artifacts.

---

## macOS

| Requirement | Details |
| :--- | :--- |
| **Minimum OS** | macOS 10.15 Catalina |
| **Architecture** | Universal (Apple Silicon `arm64` + Intel `x86_64`) |
| **Internet** | Required for music streaming and metadata |
| **Disk Space** | ~112 MB for the `.app` bundle (DMG size: ~42 MB) |
| **Status** | CONFIRMED |

**Evidence:**
- `MACOSX_DEPLOYMENT_TARGET = 10.15` in `macos/Runner.xcodeproj/project.pbxproj` and `macos/Podfile`.
- `lipo -info` on the compiled binary verifies the presence of both `x86_64` and `arm64` in the fat file.

---

## iOS

| Requirement | Details |
| :--- | :--- |
| **Minimum OS** | iOS 13.0 |
| **Device Family** | iPhone & iPad |
| **Architecture** | `arm64` |
| **Status** | CONFIRMED |

**Evidence:**
- `IPHONEOS_DEPLOYMENT_TARGET = 13.0` in `ios/Runner.xcodeproj/project.pbxproj` and `platform :ios, '13.0'` in `ios/Podfile`. 
- Plugin deployment targets enforce a minimum of iOS 13.0.
- `TARGETED_DEVICE_FAMILY = "1,2"` natively supports both iPhone and iPad layouts.
- iOS 13.0 organically enforces 64-bit architecture.

---

## Android

| Requirement | Details |
| :--- | :--- |
| **Minimum OS** | Android 7.0 (Nougat) / API Level 24 |
| **Supported ABIs** | `arm64-v8a`, `armeabi-v7a`, `x86_64` |
| **Disk Space** | APK size: ~116 MB |
| **Status** | CONFIRMED |

**Evidence:**
- `build/app/intermediates/merged_manifests/release/processReleaseManifest/AndroidManifest.xml` explicitly sets `android:minSdkVersion="24"` during compilation, overriding Flutter's default `minSdk=21` due to plugin requirements.
- Extracted ABIs from `app-release.apk` inside the `lib/` directory conform to the listed architectures.

---

## Windows

| Requirement | Details |
| :--- | :--- |
| **Minimum OS** | Windows 10 (64-bit) |
| **Architecture** | `x64` |
| **Status** | DERIVED (From Flutter constraints) |

**Evidence:**
- PPPlayer uses Flutter 3.44.8, which officially dropped support for Windows 7/8, making Windows 10 (64-bit) the strict baseline. 

---

## Linux

| Requirement | Details |
| :--- | :--- |
| **Status** | EXPERIMENTAL |
| **Minimum OS** | Ubuntu 20.04 (or equivalent) |
| **Dependencies**| `GTK 3`, `pkg-config`, `ninja-build` |

**Evidence:**
- The `linux/` target has been bootstrapped, allowing the project to compile with `flutter build linux`. Flutter Linux desktop applications rely on GTK 3 and standard GNU/Linux tooling.
