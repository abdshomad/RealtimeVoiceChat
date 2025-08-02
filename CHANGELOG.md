# Changelog

All notable changes to the RealtimeVoiceChat project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Enhanced Logging System**: Comprehensive logging with dual output (console and file)
  - Automatic log file creation in `./logs/` directory with timestamped filenames
  - Different log levels for console (INFO) and file (DEBUG) output
  - Colored console output with custom time formatting
  - Detailed file logging with source file and line information
- **Log Analysis Tools**: 
  - `log_viewer.py`: View, filter, and analyze log files
  - `log_cleanup.py`: Manage log file retention and cleanup
  - Support for real-time log following, level filtering, and statistics
- **Log Management Features**:
  - Automatic logs directory creation
  - Configurable log retention policies
  - Log file statistics and analysis
  - Error handling for logging setup failures
- Environment variable support for HOST and PORT configuration
- Graceful fallback from KokoroEngine to CoquiEngine when KokoroEngine is unavailable
- Dotenv integration for .env file loading
- Enhanced error handling for missing dependencies
- Modern Python setup with pyproject.toml and uv package management
- Improved logging with colored configuration output
- Installation scripts (install.sh, run_server.sh) for easier setup
- IDE configuration (.cursorrules) for better development experience
- Project status update reflecting community-driven development model

### Changed
- Enhanced `logsetup.py` with dual output logging and improved error handling
- Updated `server.py` to use enhanced logging with file output
- Modified `run_server.sh` to ensure logs directory exists
- Updated README.md to reflect community-driven development status and include logging documentation
- Improved error handling in audio_module.py for missing TTS engines
- Enhanced server.py configuration to use environment variables
- Migrated from pip to uv for package management

### Fixed
- Import errors when KokoroEngine is not available
- Hardcoded server configuration values
- Missing error handling for optional dependencies

## [1.0.0] - 2024-12-19

### Added
- Initial release of RealtimeVoiceChat
- Real-time voice chat functionality
- Multiple TTS engine support (Coqui, Orpheus, Kokoro)
- Web-based interface with WebRTC audio streaming
- Docker support for easy deployment
- GPU acceleration support
- Turn detection and conversation management
- LLM integration for AI responses
- Speech-to-text and text-to-speech processing
- Cross-platform compatibility

### Features
- Low-latency audio processing (< 500ms target)
- Interruption support for natural conversations
- Multiple deployment options (Docker, local)
- Modern web interface with audio controls
- Real-time transcription and response display
- Context-aware conversation management
- Support for multiple AI backends

### Technical
- Python-based server with FastAPI
- WebSocket communication for real-time audio
- CUDA support for GPU acceleration
- Modular architecture for easy extension
- Comprehensive logging and error handling
- Production-ready deployment configuration

---

## Version History

### Version 1.0.0
- **Release Date:** December 19, 2024
- **Status:** Initial stable release
- **Key Features:** Complete real-time voice chat system
- **Architecture:** Client-server with WebSocket communication
- **Deployment:** Docker and local installation support

### Unreleased Changes
- **Date:** Ongoing development
- **Status:** Community-driven development
- **Focus:** Stability improvements and feature enhancements
- **Contributions:** Open to community contributions

---

## Contributing

When contributing to this project, please:

1. Follow the existing code style and conventions
2. Add appropriate tests for new functionality
3. Update documentation for any changes
4. Include a brief description of changes in commit messages
5. Test thoroughly before submitting pull requests

## Release Process

1. **Development:** Features and fixes are developed in feature branches
2. **Testing:** All changes are tested thoroughly
3. **Review:** Pull requests are reviewed by maintainers
4. **Merge:** Approved changes are merged to main branch
5. **Release:** Stable versions are tagged and released

---

## Notes

- This project has transitioned to community-driven development
- High-quality pull requests are welcome and will be reviewed
- Focus is on stability, performance, and user experience
- Documentation is updated as features are completed
- Community contributions help maintain and improve the project 