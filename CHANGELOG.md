# Changelog

All notable changes to PPPlayer will be documented in this file.

## [Unreleased]

## [1.0.2] - 2026-09-09

### Improved
- Context-aware Autoplay prioritizes original artist before falling back to related artists.
- Tiered Recommendation Engine accurately pulls exact artist tracks without mismatched searches.
- Autoplay uses explicit playback context instead of only relying on majority queue items.

## [1.0.1] - 2026-09-09

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

---

## [1.0.0] - 2026-09-XX

### Added
- Initial public release of PPPlayer.
- Spotify-powered music metadata.
- YouTube-powered audio playback.
- Playlists, favorites and listening history.
- macOS, Windows and Linux support.
