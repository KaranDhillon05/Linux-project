#!/usr/bin/env python3
"""
SysInsight Interactive Workload Controller
A simple menu-driven tool to generate different types of system load on demand
"""

import os
import sys
import time
import threading
import subprocess
from datetime import datetime

class WorkloadController:
    def __init__(self):
        self.active_processes = []
        self.running = True
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def show_banner(self):
        """Display application banner"""
        self.clear_screen()
        print("=" * 60)
        print("     SysInsight - Interactive Workload Controller")
        print("=" * 60)
        print()
    
    def cpu_stress(self, duration=30):
        """Generate CPU load"""
        print(f"\n🔥 Generating CPU load for {duration} seconds...")
        print("   Watch your dashboard at http://localhost:5001")
        
        end_time = time.time() + duration
        start_time = time.time()
        
        while time.time() < end_time and self.running:
            # CPU-intensive work
            _ = sum(i ** 2 for i in range(10000))
            
            # Show progress
            elapsed = int(time.time() - start_time)
            if elapsed % 5 == 0:
                remaining = duration - elapsed
                print(f"   [{elapsed}s/{duration}s] - {remaining}s remaining...")
                time.sleep(1)
        
        print("✅ CPU stress completed!\n")
    
    def memory_allocate(self, size_mb=100, duration=30):
        """Allocate memory"""
        print(f"\n🧠 Allocating {size_mb} MB of memory for {duration} seconds...")
        print("   Watch memory usage increase on dashboard")
        
        # Allocate memory
        data = []
        chunk_size = 1024 * 1024  # 1MB
        
        for i in range(size_mb):
            data.append(bytearray(chunk_size))
            if i % 20 == 0 and i > 0:
                print(f"   Allocated {i} MB...")
        
        print(f"   Holding {size_mb} MB for {duration} seconds...")
        time.sleep(duration)
        
        # Release memory
        data.clear()
        print("✅ Memory released!\n")
    
    def disk_io(self, count=50):
        """Generate disk I/O"""
        print(f"\n💾 Performing {count} disk I/O operations...")
        print("   Watch disk I/O increase on dashboard")
        
        temp_dir = "/tmp/sysinsight_test"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            for i in range(count):
                file_path = f"{temp_dir}/test_{i}.dat"
                
                # Write 1MB file
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(1024 * 1024))
                
                # Read it back
                with open(file_path, 'rb') as f:
                    _ = f.read()
                
                # Delete it
                os.remove(file_path)
                
                if i % 10 == 0 and i > 0:
                    print(f"   Processed {i}/{count} files...")
            
            print(f"✅ Disk I/O completed ({count} files)!\n")
        
        finally:
            # Cleanup
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def mixed_load(self, duration=60):
        """Run mixed CPU, memory, and disk load"""
        print(f"\n⚡ Running MIXED workload for {duration} seconds...")
        print("   This will stress CPU, Memory, AND Disk simultaneously")
        print("   Watch ALL metrics increase on dashboard!\n")
        
        # Run different workloads in parallel threads
        threads = []
        
        # CPU thread
        cpu_thread = threading.Thread(
            target=self.cpu_stress, 
            args=(duration,),
            daemon=True
        )
        threads.append(cpu_thread)
        
        # Memory thread
        mem_thread = threading.Thread(
            target=self.memory_allocate,
            args=(150, duration),
            daemon=True
        )
        threads.append(mem_thread)
        
        # Disk thread (multiple rounds)
        def disk_worker():
            end_time = time.time() + duration
            while time.time() < end_time and self.running:
                self.disk_io(10)
                time.sleep(2)
        
        disk_thread = threading.Thread(target=disk_worker, daemon=True)
        threads.append(disk_thread)
        
        # Start all
        for t in threads:
            t.start()
        
        # Wait with progress
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            print(f"   Running... {remaining}s remaining", end='\r')
            time.sleep(1)
        
        print("\n✅ Mixed workload completed!\n")
    
    def show_current_stats(self):
        """Show current system stats"""
        print("\n📊 Current System Metrics:")
        print("-" * 60)
        
        try:
            import requests
            response = requests.get('http://localhost:5001/api/metrics/all', timeout=5)
            data = response.json()
            
            print(f"  CPU Usage:    {data['cpu']['percent']}%")
            print(f"  Memory Usage: {data['memory']['virtual']['percent']}%")
            print(f"  Disk I/O:     {data['disk']['io_stats']['write_mb']:.2f} MB written")
            print(f"  Status:       {data['alerts']['cpu']}/{data['alerts']['memory']}/{data['alerts']['disk']}")
        except Exception as e:
            print(f"  ⚠️  Could not fetch metrics: {e}")
            print(f"  Make sure container is running: docker ps")
        
        print("-" * 60)
        print()
    
    def show_menu(self):
        """Display main menu"""
        print("\n┌────────────────────────────────────────────────────────┐")
        print("│                   WORKLOAD OPTIONS                     │")
        print("└────────────────────────────────────────────────────────┘")
        print()
        print("  1. 🔥 CPU Stress Test (30s)")
        print("  2. 🧠 Memory Allocation (100 MB for 30s)")
        print("  3. 💾 Disk I/O Test (50 operations)")
        print("  4. ⚡ Mixed Workload (60s - CPU+Memory+Disk)")
        print("  5. 📊 Show Current Metrics")
        print("  6. 🔧 Custom Workload")
        print("  7. ❌ Exit")
        print()
    
    def custom_workload(self):
        """Custom workload configuration"""
        print("\n🔧 Custom Workload Configuration")
        print("-" * 60)
        
        try:
            print("\nSelect workload type:")
            print("  1. CPU")
            print("  2. Memory")
            print("  3. Disk")
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == '1':
                duration = int(input("Duration in seconds (default 30): ") or "30")
                self.cpu_stress(duration)
            
            elif choice == '2':
                size = int(input("Memory size in MB (default 100): ") or "100")
                duration = int(input("Duration in seconds (default 30): ") or "30")
                self.memory_allocate(size, duration)
            
            elif choice == '3':
                count = int(input("Number of file operations (default 50): ") or "50")
                self.disk_io(count)
            
            else:
                print("Invalid choice!")
        
        except ValueError:
            print("Invalid input! Using defaults...")
            self.cpu_stress(30)
    
    def run(self):
        """Main application loop"""
        while self.running:
            self.show_banner()
            self.show_menu()
            
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == '1':
                self.cpu_stress(30)
                input("\nPress ENTER to continue...")
            
            elif choice == '2':
                self.memory_allocate(100, 30)
                input("\nPress ENTER to continue...")
            
            elif choice == '3':
                self.disk_io(50)
                input("\nPress ENTER to continue...")
            
            elif choice == '4':
                self.mixed_load(60)
                input("\nPress ENTER to continue...")
            
            elif choice == '5':
                self.show_current_stats()
                input("\nPress ENTER to continue...")
            
            elif choice == '6':
                self.custom_workload()
                input("\nPress ENTER to continue...")
            
            elif choice == '7':
                print("\n👋 Goodbye!\n")
                self.running = False
                break
            
            else:
                print("\n❌ Invalid choice! Please select 1-7.")
                time.sleep(2)


def main():
    """Entry point"""
    print("\n" + "=" * 60)
    print("  Welcome to SysInsight Workload Controller!")
    print("=" * 60)
    print("\n  This tool lets you generate different system loads")
    print("  to see real-time changes in your monitoring dashboard.")
    print("\n  Dashboard: http://localhost:5001")
    print("=" * 60)
    
    input("\nPress ENTER to start...")
    
    controller = WorkloadController()
    
    try:
        controller.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        controller.running = False
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\nCleaning up...")
        time.sleep(1)


if __name__ == '__main__':
    main()
