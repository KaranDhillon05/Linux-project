#!/usr/bin/env python3
"""
System Stress Test Script
Generates CPU, Memory, and Disk load to demonstrate SysInsight monitoring
"""

import time
import multiprocessing
import os
import argparse
from datetime import datetime

def cpu_stress(duration=30, intensity=100):
    """
    Generate CPU load
    
    Args:
        duration: How long to run (seconds)
        intensity: CPU usage target (1-100%)
    """
    print(f"🔥 Starting CPU stress test for {duration} seconds at {intensity}% intensity...")
    
    end_time = time.time() + duration
    work_time = intensity / 100
    sleep_time = 1 - work_time
    
    while time.time() < end_time:
        # Busy work
        start = time.time()
        while time.time() - start < work_time:
            _ = sum(i*i for i in range(1000))
        
        # Sleep to control intensity
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    print("✅ CPU stress test completed")

def memory_stress(duration=30, size_mb=100):
    """
    Generate memory load
    
    Args:
        duration: How long to hold memory (seconds)
        size_mb: Amount of memory to allocate (MB)
    """
    print(f"🧠 Starting memory stress test for {duration} seconds, allocating {size_mb}MB...")
    
    # Allocate memory
    data = []
    chunk_size = 1024 * 1024  # 1MB chunks
    
    for i in range(size_mb):
        data.append(bytearray(chunk_size))
        if i % 10 == 0:
            print(f"   Allocated {i}MB...")
    
    print(f"   Holding {size_mb}MB for {duration} seconds...")
    time.sleep(duration)
    
    # Clean up
    data.clear()
    print("✅ Memory stress test completed")

def disk_stress(duration=30, file_size_mb=10):
    """
    Generate disk I/O load
    
    Args:
        duration: How long to perform I/O (seconds)
        file_size_mb: Size of files to write (MB)
    """
    print(f"💾 Starting disk stress test for {duration} seconds, writing {file_size_mb}MB files...")
    
    test_dir = "/tmp/sysinsight_stress"
    os.makedirs(test_dir, exist_ok=True)
    
    end_time = time.time() + duration
    file_count = 0
    
    try:
        while time.time() < end_time:
            file_path = f"{test_dir}/test_{file_count}.dat"
            
            # Write file
            with open(file_path, 'wb') as f:
                f.write(os.urandom(file_size_mb * 1024 * 1024))
            
            # Read file
            with open(file_path, 'rb') as f:
                _ = f.read()
            
            # Delete file
            os.remove(file_path)
            
            file_count += 1
            if file_count % 5 == 0:
                print(f"   Processed {file_count} files...")
    
    finally:
        # Cleanup
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
    
    print(f"✅ Disk stress test completed ({file_count} files processed)")

def run_combined_stress(duration=60):
    """
    Run CPU, Memory, and Disk stress tests simultaneously
    """
    print(f"\n{'='*60}")
    print(f"🚀 SYSINSIGHT STRESS TEST DEMO")
    print(f"{'='*60}")
    print(f"Duration: {duration} seconds")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nWatch your dashboard at: http://localhost:5001")
    print(f"{'='*60}\n")
    
    # Create processes for parallel execution
    processes = [
        multiprocessing.Process(target=cpu_stress, args=(duration, 50)),
        multiprocessing.Process(target=memory_stress, args=(duration, 200)),
        multiprocessing.Process(target=disk_stress, args=(duration, 5))
    ]
    
    # Start all processes
    for p in processes:
        p.start()
    
    # Wait for completion
    for p in processes:
        p.join()
    
    print(f"\n{'='*60}")
    print(f"✅ All stress tests completed!")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

def run_wave_pattern(cycles=3, cycle_duration=20):
    """
    Create a wave pattern of increasing/decreasing load
    """
    print(f"\n🌊 Running wave pattern stress test ({cycles} cycles)...")
    
    for cycle in range(cycles):
        print(f"\n--- Cycle {cycle + 1}/{cycles} ---")
        
        # Ramp up
        print("📈 Ramping up load...")
        cpu_stress(duration=cycle_duration//2, intensity=30 + (cycle * 20))
        
        # Ramp down
        print("📉 Ramping down load...")
        time.sleep(cycle_duration//2)
    
    print("\n✅ Wave pattern completed")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SysInsight Stress Test - Generate system load for monitoring demo'
    )
    
    parser.add_argument(
        '--mode',
        choices=['cpu', 'memory', 'disk', 'combined', 'wave'],
        default='combined',
        help='Type of stress test to run (default: combined)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Duration in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--intensity',
        type=int,
        default=50,
        help='CPU intensity 1-100%% (default: 50)'
    )
    
    parser.add_argument(
        '--memory-mb',
        type=int,
        default=200,
        help='Memory to allocate in MB (default: 200)'
    )
    
    args = parser.parse_args()
    
    print("\n⚠️  IMPORTANT: Open http://localhost:5001 to watch real-time changes!\n")
    time.sleep(3)
    
    if args.mode == 'cpu':
        cpu_stress(args.duration, args.intensity)
    elif args.mode == 'memory':
        memory_stress(args.duration, args.memory_mb)
    elif args.mode == 'disk':
        disk_stress(args.duration)
    elif args.mode == 'wave':
        run_wave_pattern()
    else:  # combined
        run_combined_stress(args.duration)
    
    print("\n🎉 Stress test complete! Check your graphs for the activity.\n")
