# ZeroBrave - Future Roadmap

Ideas and features planned for future versions.

## v1.2.0 - Interactive TUI ✅ COMPLETED

### Terminal User Interface
- [x] Create interactive TUI using `rich` or `textual`
- [x] Toggle options for each policy category
- [x] Visual preview of changes before applying
- [x] Keyboard navigation (arrow keys, hotkeys)
- [x] Works over SSH and headless servers

### TUI Mockup
```
┌───────── ZeroBrave v1.2.0 ──────────────┐
│                                       │
│  [1] ✓ Disable AI Features           │
│  [2] ✓ Block Telemetry               │
│  [3] ✓ Block Third-Party Cookies     │
│  [4] ✓ Disable Autofill              │
│  [5] ✗ Enable Tor                    │
│  [6] ✓ Enhanced Safe Browsing        │
│                                      │
│  [A] Apply  [B] Backup  [R] Restore  │
│  [Q] Quit                            │
└──────────────────────────────────────────┘
```

### Dependencies
- `rich` - For styled terminal output
- `textual` (optional) - For more complex TUI

## v1.3.0 - Policy Profiles (for future use)

- [ ] Predefined profiles: "Strict", "Balanced", "Minimal"
- [ ] Custom profile saving/loading
- [ ] Export/import profiles as JSON

## v2.0.0 - Distribution (if needed)

- [ ] Publish to PyPI (`pip install zerobrave`)
- [ ] Create `.deb` package for Debian/Ubuntu
- [ ] Create `.rpm` package for Fedora/RHEL
- [ ] GitHub Actions CI/CD
- [ ] Automatic releases
