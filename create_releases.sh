#!/bin/bash

# Extract release notes for 1.0.0
cat << 'EOF' > release_1_0_0.md
### Added
- Initial public release of PPPlayer.
- Spotify-powered music metadata.
- YouTube-powered audio playback.
- Playlists, favorites and listening history.
- macOS, Windows and Linux support.
EOF

# Extract release notes for 1.0.1
cat << 'EOF' > release_1_0_1.md
### Added
- Autoplay recommendations when the playback queue is ending.
- Custom Spotify and YouTube API credentials.
- Discover section with personalized recommendations.
- Additional language support.
- Added dynamic tooltip that follows the mouse cursor on the seekbar.

### Changed
- Improved playback queue persistence.
- Improved macOS media control integration.
- Updated player animations using Material 3 Expressive-inspired motion.

### Fixed
- Fixed duplicate macOS Now Playing controls caused by WebKit.
- Fixed station tracks not being highlighted correctly.
- Fixed playback state restoration after restarting the app.
- Fixed playback pausing/stopping unexpectedly when dragging the seekbar.
- Fixed bottom player bar rendering fully transparent and unreadable on macOS when playing music.
EOF

# Extract release notes for 1.0.2
cat << 'EOF' > release_1_0_2.md
### Improved
- Context-aware Autoplay prioritizes original artist before falling back to related artists.
- Tiered Recommendation Engine accurately pulls exact artist tracks without mismatched searches.
- Autoplay uses explicit playback context instead of only relying on majority queue items.
EOF

# Extract release notes for 1.0.3
cat << 'EOF' > release_1_0_3.md
### Added
- Hybrid playback engine providing robust background processing and lock-screen playback capabilities.
- Deduplication and generation IDs to prevent overlapping and stale media commands across WebView bridge.

### Fixed
- Fixed an issue where the song queue would sometimes not automatically advance to the next track.
- Fixed a bug where a paused track would unexpectedly resume when handing off from foreground to PiP or background.
- Accurate millisecond precision reporting for current track position and playback duration.
- Eliminated several IDE linter errors and cleaned up redundant files.
EOF

# Create tags
git tag v1.0.0 066fd14
git tag v1.0.1 82857e0
git tag v1.0.2 bbc7ec6
git tag v1.0.3 98d4d25
git push --tags

# Create releases
gh release create v1.0.0 --title "v1.0.0" --notes-file release_1_0_0.md
gh release create v1.0.1 --title "v1.0.1" --notes-file release_1_0_1.md
gh release create v1.0.2 --title "v1.0.2" --notes-file release_1_0_2.md

# For v1.0.3 we will attach the binaries
gh release create v1.0.3 --title "v1.0.3" --notes-file release_1_0_3.md PPPlayer-macOS.zip app/build/app/outputs/flutter-apk/app-release.apk#PPPlayer-Android.apk
