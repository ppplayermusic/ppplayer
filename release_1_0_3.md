### Added
- Hybrid playback engine providing robust background processing and lock-screen playback capabilities.
- Deduplication and generation IDs to prevent overlapping and stale media commands across WebView bridge.

### Fixed
- Fixed an issue where the song queue would sometimes not automatically advance to the next track.
- Fixed a bug where a paused track would unexpectedly resume when handing off from foreground to PiP or background.
- Accurate millisecond precision reporting for current track position and playback duration.
- Eliminated several IDE linter errors and cleaned up redundant files.
