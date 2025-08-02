# Logging System Documentation

## Overview

The RealtimeVoiceChat project now includes an enhanced logging system that provides both console and file logging capabilities. The logging system is designed to help with debugging, monitoring, and troubleshooting server operations.

## Features

### Dual Output Logging
- **Console Logging**: Colored, formatted output for real-time monitoring
- **File Logging**: Detailed logs saved to timestamped files in `./logs/` directory

### Log Levels
- **DEBUG**: Detailed debugging information (file only)
- **INFO**: General information about server operations
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for problems that need attention

### Log File Management
- Automatic timestamped log file creation
- Log rotation and cleanup utilities
- Configurable retention policies

## Configuration

### Basic Setup

The logging system is automatically configured when the server starts:

```python
from logsetup import setup_logging
setup_logging(logging.DEBUG, enable_file_logging=True, file_level=logging.DEBUG, console_level=logging.INFO)
```

### Parameters

- `level`: Root logger level (default: `logging.INFO`)
- `enable_file_logging`: Enable/disable file logging (default: `True`)
- `file_level`: Log level for file output (default: `logging.DEBUG`)
- `console_level`: Log level for console output (default: `logging.INFO`)

## Log File Format

### Console Format
```
MM:SS.cs logger_name LEVEL message
```

Example:
```
20:03.69 server       INFO 🖥️👋 Welcome to local real-time voice chat
20:03.70 websocket    INFO 🖥️✅ Client connected via WebSocket.
```

### File Format
```
YYYY-MM-DD HH:MM:SS logger_name        LEVEL    filename:line - message
```

Example:
```
2025-08-02 04:20:03 server             INFO     server.py:8 - 🖥️👋 Welcome to local real-time voice chat
2025-08-02 04:20:03 websocket          INFO     server.py:893 - 🖥️✅ Client connected via WebSocket.
```

## Log Files

### Location
Log files are stored in the `./logs/` directory with the naming pattern:
```
server_YYYYMMDD_HHMMSS.log
```

Example: `server_20250802_042003.log`

### File Management
- Each server start creates a new log file
- Files are automatically timestamped
- Old files can be cleaned up using the cleanup utility

## Utilities

### Log Viewer (`log_viewer.py`)

View and analyze log files with various options:

```bash
# List available log files
python log_viewer.py --list

# Show last 50 lines of most recent log
python log_viewer.py --tail 50

# Follow log file in real-time
python log_viewer.py --follow

# Filter by log level
python log_viewer.py --level ERROR

# Search for specific terms
python log_viewer.py --search "websocket"

# Show log statistics
python log_viewer.py --stats

# View specific log file
python log_viewer.py --file server_20250802_042003.log
```

### Log Cleanup (`log_cleanup.py`)

Manage log file retention and cleanup:

```bash
# Show logs directory information
python log_cleanup.py --info

# Clean up logs older than 7 days (dry run)
python log_cleanup.py --days 7 --dry-run

# Clean up logs older than 7 days
python log_cleanup.py --days 7

# Clean up logs older than 30 days
python log_cleanup.py --days 30
```

## Usage Examples

### Starting the Server
The server automatically sets up logging when started:

```bash
./run_server.sh
```

This will:
1. Create the `./logs/` directory if it doesn't exist
2. Set up console and file logging
3. Create a new timestamped log file
4. Display the log file path in the console

### Monitoring Logs

#### Real-time Monitoring
```bash
# Follow the current log file
python log_viewer.py --follow

# Or use standard Unix tools
tail -f logs/server_*.log
```

#### Error Analysis
```bash
# Find all errors in recent logs
python log_viewer.py --level ERROR

# Search for specific error patterns
python log_viewer.py --search "disconnect"
```

#### Performance Analysis
```bash
# Show log statistics
python log_viewer.py --stats

# Check log file sizes
python log_cleanup.py --info
```

## Log Messages

### Common Log Messages

#### Server Startup
```
🖥️👋 Welcome to local real-time voice chat
📁 Server logs will be saved to: /path/to/logs/server_YYYYMMDD_HHMMSS.log
📊 Logging setup: 2 handlers, logger level: DEBUG
🖥️⚙️ [PARAM] Starting engine: orpheus
🖥️⚙️ [PARAM] Direct streaming: ON
🖥️⚙️ [PARAM] Audio queue size limit set to: 50
🖥️▶️ Server starting up
```

#### WebSocket Connections
```
🖥️✅ Client connected via WebSocket.
🖥️📥 ←←Client: {"type": "audio", "data": "..."}
🖥️📤 →→Client: {"type": "transcription", "text": "..."}
🖥️❌ WebSocket session ended.
```

#### Audio Processing
```
🖥️🎙️ Recording started. TTS Client Playing: False
🖥️🧠 HOT: 'Hello, how are you today?'
🖥️✅ FINAL USER REQUEST (STT Callback): 'Hello, how are you today?'
🖥️💬 PARTIAL ASSISTANT ANSWER: 'Hello! I'm doing well, thank you for asking.'
🖥️✅ FINAL ASSISTANT ANSWER (Sending): 'Hello! I'm doing well, thank you for asking.'
```

#### Error Handling
```
🖥️⚠️ WARNING disconnect in process_incoming_data: WebSocketDisconnect()
🖥️💥 RUNTIME_ERROR in process_incoming_data: ConnectionResetError()
🖥️⚠️ Ignoring client message with invalid JSON
```

## Troubleshooting

### Common Issues

#### Log Files Not Created
- Check that the `./logs/` directory exists and is writable
- Verify that file logging is enabled in the configuration
- Check for disk space issues

#### High Log Volume
- Adjust log levels to reduce verbosity
- Use cleanup utility to remove old logs
- Consider implementing log rotation for long-running servers

#### Performance Impact
- File logging has minimal performance impact
- Console logging with colors may have slight overhead
- Consider disabling file logging in production if not needed

### Debugging Tips

1. **Use DEBUG level for file logging** to get detailed information
2. **Filter logs by level** to focus on specific issues
3. **Search for error patterns** to identify recurring problems
4. **Monitor log file sizes** to prevent disk space issues
5. **Use log statistics** to understand usage patterns

## Configuration Options

### Environment Variables
- `LOG_LEVEL`: Set the root log level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE_LEVEL`: Set the file log level
- `LOG_CONSOLE_LEVEL`: Set the console log level
- `LOG_ENABLE_FILE`: Enable/disable file logging (true/false)

### Custom Configuration
You can customize the logging setup by modifying the `setup_logging()` call in `server.py`:

```python
# Minimal logging (console only)
setup_logging(logging.INFO, enable_file_logging=False)

# Verbose logging (all levels to file)
setup_logging(logging.DEBUG, enable_file_logging=True, file_level=logging.DEBUG, console_level=logging.INFO)

# Production logging (warnings and errors only)
setup_logging(logging.WARNING, enable_file_logging=True, file_level=logging.WARNING, console_level=logging.WARNING)
```

## Best Practices

1. **Regular Cleanup**: Use the cleanup utility to prevent disk space issues
2. **Monitor Log Sizes**: Check log file sizes regularly
3. **Error Analysis**: Use log filtering to identify and fix issues
4. **Performance Monitoring**: Use log statistics to monitor server performance
5. **Backup Important Logs**: Archive important log files before cleanup

## Integration with Other Tools

### Log Aggregation
The log files can be easily integrated with log aggregation systems:
- **ELK Stack**: Logstash can parse the log format
- **Splunk**: Log files can be monitored and indexed
- **Grafana**: Log statistics can be visualized

### Monitoring
- **File size monitoring**: Alert on large log files
- **Error rate monitoring**: Track error frequency
- **Performance monitoring**: Monitor log entry rates

## Future Enhancements

- [ ] Log rotation based on file size
- [ ] Structured logging (JSON format)
- [ ] Remote logging capabilities
- [ ] Log compression for old files
- [ ] Integration with monitoring systems 