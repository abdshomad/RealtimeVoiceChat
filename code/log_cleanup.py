#!/usr/bin/env python3
"""
Log Cleanup Utility for RealtimeVoiceChat

A utility to clean up old log files and manage log retention.
"""

import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import shutil

def get_log_files(logs_dir: str = "../logs") -> list:
    """Get all log files in the logs directory."""
    logs_path = Path(logs_dir)
    if not logs_path.exists():
        print(f"❌ Logs directory not found: {logs_path}")
        return []
    
    log_files = list(logs_path.glob("server_*.log"))
    return sorted(log_files, reverse=True)  # Most recent first

def cleanup_old_logs(logs_dir: str = "../logs", days: int = 7, dry_run: bool = False):
    """Remove log files older than specified days."""
    logs_path = Path(logs_dir)
    if not logs_path.exists():
        print(f"❌ Logs directory not found: {logs_path}")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    log_files = get_log_files(logs_dir)
    
    files_to_delete = []
    total_size = 0
    
    for log_file in log_files:
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        if mtime < cutoff_date:
            files_to_delete.append(log_file)
            total_size += log_file.stat().st_size
    
    if not files_to_delete:
        print(f"✅ No log files older than {days} days found")
        return
    
    print(f"📁 Found {len(files_to_delete)} log files older than {days} days")
    print(f"💾 Total size to free: {total_size / 1024:.1f} KB")
    
    if dry_run:
        print("🔍 Dry run - would delete:")
        for log_file in files_to_delete:
            size = log_file.stat().st_size
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            print(f"  {log_file.name} ({size} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("🗑️ Deleting old log files...")
        for log_file in files_to_delete:
            try:
                log_file.unlink()
                print(f"  ✅ Deleted: {log_file.name}")
            except Exception as e:
                print(f"  ❌ Failed to delete {log_file.name}: {e}")
        
        print(f"✅ Cleanup completed. Freed {total_size / 1024:.1f} KB")

def show_log_directory_info(logs_dir: str = "../logs"):
    """Show information about the logs directory."""
    logs_path = Path(logs_dir)
    if not logs_path.exists():
        print(f"❌ Logs directory not found: {logs_path}")
        return
    
    log_files = get_log_files(logs_dir)
    
    if not log_files:
        print("📁 Logs directory is empty")
        return
    
    total_size = sum(f.stat().st_size for f in log_files)
    oldest_file = log_files[-1]
    newest_file = log_files[0]
    
    print(f"📁 Logs directory: {logs_path}")
    print(f"📄 Total log files: {len(log_files)}")
    print(f"💾 Total size: {total_size / 1024:.1f} KB")
    print(f"⏰ Oldest log: {oldest_file.name} ({datetime.fromtimestamp(oldest_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"⏰ Newest log: {newest_file.name} ({datetime.fromtimestamp(newest_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Show files by age
    print("\n📊 Log files by age:")
    for i, log_file in enumerate(log_files[:10]):  # Show top 10
        size = log_file.stat().st_size
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        age = datetime.now() - mtime
        print(f"  {i+1:2d}. {log_file.name} ({size} bytes, {age.days} days old)")

def main():
    parser = argparse.ArgumentParser(description="Log Cleanup for RealtimeVoiceChat")
    parser.add_argument("--logs-dir", default="../logs", help="Logs directory path")
    parser.add_argument("--days", type=int, default=7, help="Delete logs older than N days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without actually deleting")
    parser.add_argument("--info", action="store_true", help="Show logs directory information")
    
    args = parser.parse_args()
    
    if args.info:
        show_log_directory_info(args.logs_dir)
    else:
        cleanup_old_logs(args.logs_dir, args.days, args.dry_run)

if __name__ == "__main__":
    main() 