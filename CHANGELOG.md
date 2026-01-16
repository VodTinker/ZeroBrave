# Changelog

All notable changes to ZeroBrave will be documented in this file.

## [1.1.0] - 2026-01-16 (by @vodtinker)

### Added
- Full CLI with arguments: `--dry-run`, `--backup`, `--restore`, `--local`
- macOS support
- Backup/restore functionality
- Permission validation (sudo/admin check)
- Brave installation detection
- Comprehensive logging system
- Unit tests (11 tests)

### Changed
- `QuicAllowed` → `true` (better privacy & performance)
- `SafeBrowsingProtectionLevel` → `2` (Enhanced, was incorrectly set to 1)
- `DiskCacheSize` → 100MB (was 1MB, too restrictive)
- `ComponentUpdatesEnabled` → `true` (security)

### Removed
- `CertificateTransparencyEnforcementDisabledForUrls` (security risk)

### Fixed
- JSON comments causing parse errors (JSONC now properly formatted)

## [1.0.0] - Initial Release (by @rompelhd)

### Added
- Basic policy application for Linux and Windows
- Privacy-focused default policies
- AI features disabled (Leo, Gemini, Lens)
- Telemetry completely disabled
- Third-party cookies blocked
