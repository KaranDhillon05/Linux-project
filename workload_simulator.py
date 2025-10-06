#!/usr/bin/env python3
"""
Workload Simulator - Creates realistic system activity for SysInsight monitoring
This runs in the background to generate CPU, memory, and disk fluctuations
"""

import time
import random
import threading
import os
import psutil
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkloadSimulator:
    """Simulates various system workloads"""
    
    def __init__(self):
        self.running = True
        self.cpu_intensity = 30  # Base CPU intensity
        self.memory_allocations = []
        self.temp_dir = "/tmp/sysinsight_workload"
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def stop(self):
        """Stop all workload simulations"""
        self.running = False
        logger.info("Stopping workload simulator...")
    
    def cpu_worker(self):
        """
        Simulates varying CPU workload
        Creates wave patterns of CPU usage
        """
        logger.info("🔥 CPU worker started")
        cycle = 0
        
        while self.running:
            # Create wave pattern: low -> medium -> high -> medium -> low
            wave_position = (cycle % 60) / 60.0  # 60-second cycle
            intensity = 20 + (30 * abs(0.5 - wave_position) * 2)  # 20-50%
            
            # Do some CPU-intensive work
            duration = 0.5 + (intensity / 100)
            start = time.time()
            
            while time.time() - start < duration:
                # Prime number calculation
                num = random.randint(1000, 10000)
                is_prime = all(num % i != 0 for i in range(2, int(num ** 0.5) + 1))
                
                # String operations
                text = "SysInsight" * random.randint(10, 100)
                _ = text.upper().lower().replace("S", "s")
                
                # Mathematical operations
                _ = sum(i * i for i in range(random.randint(100, 500)))
            
            # Rest period
            time.sleep(max(0.1, 1.0 - duration))
            cycle += 1
            
            if cycle % 30 == 0:
                logger.debug(f"CPU cycle {cycle}, intensity: {intensity:.1f}%")
    
    def memory_worker(self):
        """
        Simulates memory allocation and deallocation
        Creates gradual memory usage patterns
        """
        logger.info("🧠 Memory worker started")
        
        while self.running:
            # Gradually increase memory
            if len(self.memory_allocations) < 20:
                # Allocate 5-15 MB
                size = random.randint(5, 15) * 1024 * 1024
                data = bytearray(size)
                # Fill with random data
                for i in range(0, len(data), 1024):
                    data[i] = random.randint(0, 255)
                self.memory_allocations.append(data)
                logger.debug(f"Allocated {size / (1024*1024):.1f} MB")
            
            # Occasionally free some memory
            if len(self.memory_allocations) > 5 and random.random() < 0.3:
                freed = self.memory_allocations.pop(random.randint(0, len(self.memory_allocations) - 1))
                logger.debug(f"Freed {len(freed) / (1024*1024):.1f} MB")
            
            time.sleep(random.uniform(2, 5))
    
    def disk_worker(self):
        """
        Simulates disk I/O operations
        Creates file read/write activity
        """
        logger.info("💾 Disk worker started")
        file_counter = 0
        
        while self.running:
            try:
                # Write files
                if random.random() < 0.7:
                    file_path = f"{self.temp_dir}/workload_{file_counter}.dat"
                    size = random.randint(1, 5) * 1024 * 1024  # 1-5 MB
                    
                    with open(file_path, 'wb') as f:
                        f.write(os.urandom(size))
                    
                    file_counter += 1
                    logger.debug(f"Wrote file {file_counter} ({size / (1024*1024):.1f} MB)")
                
                # Read random existing file
                files = [f for f in os.listdir(self.temp_dir) if f.startswith('workload_')]
                if files:
                    file_to_read = random.choice(files)
                    with open(f"{self.temp_dir}/{file_to_read}", 'rb') as f:
                        _ = f.read()
                    logger.debug(f"Read file {file_to_read}")
                
                # Cleanup old files (keep only 20)
                if len(files) > 20:
                    oldest_files = sorted(files)[:10]
                    for old_file in oldest_files:
                        os.remove(f"{self.temp_dir}/{old_file}")
                    logger.debug(f"Cleaned up {len(oldest_files)} old files")
                
            except Exception as e:
                logger.error(f"Disk worker error: {e}")
            
            time.sleep(random.uniform(1, 3))
    
    def network_simulator(self):
        """
        Simulates network-like activity (data processing)
        Creates periodic bursts of activity
        """
        logger.info("🌐 Network simulator started")
        
        while self.running:
            # Simulate processing incoming data
            if random.random() < 0.4:  # 40% chance of burst
                burst_size = random.randint(100, 500)
                data = []
                
                for _ in range(burst_size):
                    # Simulate JSON parsing
                    fake_data = {
                        'timestamp': time.time(),
                        'value': random.random(),
                        'status': random.choice(['ok', 'warning', 'error']),
                        'data': [random.randint(0, 100) for _ in range(10)]
                    }
                    data.append(str(fake_data))
                
                # Process the data
                _ = ''.join(data)
                logger.debug(f"Processed burst of {burst_size} items")
            
            time.sleep(random.uniform(2, 6))
    
    def periodic_spike(self):
        """
        Creates periodic CPU/memory spikes
        Simulates batch processing or scheduled tasks
        """
        logger.info("⚡ Periodic spike simulator started")
        
        while self.running:
            # Wait 30-60 seconds between spikes
            time.sleep(random.uniform(30, 60))
            
            if not self.running:
                break
            
            logger.info("🔥 Generating activity spike...")
            
            # CPU spike
            spike_duration = random.uniform(3, 8)
            end_time = time.time() + spike_duration
            
            while time.time() < end_time and self.running:
                # Intensive computation
                _ = sum(i ** 2 for i in range(random.randint(10000, 50000)))
                _ = [random.random() for _ in range(random.randint(1000, 5000))]
            
            logger.info("✅ Activity spike completed")
    
    def run(self):
        """Start all workload simulators"""
        logger.info("="*60)
        logger.info("🚀 SysInsight Workload Simulator Starting")
        logger.info("="*60)
        
        # Create worker threads
        workers = [
            threading.Thread(target=self.cpu_worker, name="CPU-Worker", daemon=True),
            threading.Thread(target=self.memory_worker, name="Memory-Worker", daemon=True),
            threading.Thread(target=self.disk_worker, name="Disk-Worker", daemon=True),
            threading.Thread(target=self.network_simulator, name="Network-Worker", daemon=True),
            threading.Thread(target=self.periodic_spike, name="Spike-Worker", daemon=True),
        ]
        
        # Start all workers
        for worker in workers:
            worker.start()
            logger.info(f"Started {worker.name}")
        
        logger.info("="*60)
        logger.info("✅ All workload simulators running")
        logger.info("📊 Monitor at: http://localhost:5001")
        logger.info("="*60)
        
        # Keep main thread alive
        try:
            while self.running:
                # Log system stats every 30 seconds
                time.sleep(30)
                if self.running:
                    cpu = psutil.cpu_percent(interval=1)
                    mem = psutil.virtual_memory().percent
                    logger.info(f"📈 System: CPU={cpu:.1f}%, Memory={mem:.1f}%")
        except KeyboardInterrupt:
            logger.info("\n⚠️  Received shutdown signal")
        finally:
            self.stop()
            # Wait for threads to finish
            time.sleep(2)
            logger.info("🛑 Workload simulator stopped")


if __name__ == '__main__':
    simulator = WorkloadSimulator()
    simulator.run()
