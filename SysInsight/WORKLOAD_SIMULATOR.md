# Workload Simulator

The SysInsight container now includes a **Workload Simulator** that runs in the background to create realistic system activity. This ensures the monitoring dashboard displays meaningful fluctuations in CPU, memory, and disk usage.

## What It Does

The workload simulator creates 5 different types of background activity:

### 1. CPU Worker 🔥
- Creates **wave patterns** of CPU usage (20-50%)
- Performs prime number calculations
- String operations and transformations
- Mathematical computations
- 60-second cycles with varying intensity

### 2. Memory Worker 🧠
- Gradually **allocates memory** (5-15 MB chunks)
- Maintains up to 20 allocations (~100-300 MB)
- Randomly frees memory to create fluctuations
- Simulates real application memory patterns

### 3. Disk Worker 💾
- **Writes files** (1-5 MB each)
- Reads random existing files
- Maintains 20 active files
- Automatic cleanup of old files
- Creates realistic I/O patterns

### 4. Network Simulator 🌐
- Simulates **data processing** bursts
- Processes 100-500 "network packets"
- JSON parsing simulation
- Periodic activity spikes

### 5. Periodic Spike Generator ⚡
- Creates **activity spikes** every 30-60 seconds
- Intensive computations for 3-8 seconds
- Simulates batch processing or scheduled tasks
- Makes graphs more dynamic

## Expected Behavior

With the workload simulator running, you should see:

- **CPU Usage**: Fluctuating between 20-60% with periodic spikes
- **Memory Usage**: Gradually increasing then decreasing in cycles
- **Disk I/O**: Steady read/write activity with occasional bursts
- **Real-time Charts**: Dynamic line graphs showing changes over time

## Monitoring the Simulator

The workload simulator logs its activity:

```bash
# View simulator logs
docker logs sysinsight | grep "Workload"

# Or watch in real-time
docker logs sysinsight -f
```

Example output:
```
🚀 SysInsight Workload Simulator Starting
Started CPU-Worker
Started Memory-Worker
Started Disk-Worker
Started Network-Worker
Started Spike-Worker
✅ All workload simulators running
📊 Monitor at: http://localhost:5001
📈 System: CPU=34.2%, Memory=18.5%
```

## Control & Configuration

The workload simulator:
- ✅ **Starts automatically** with the container
- ✅ **Runs in background** (doesn't block main app)
- ✅ **Safe resource usage** (won't overload container)
- ✅ **Automatic cleanup** (removes temporary files)
- ✅ **Stops with container** (clean shutdown)

## Manual Testing (Optional)

You can also run the standalone stress test script:

```bash
# Inside the container
python stress_test.py --mode combined --duration 60

# Different modes
python stress_test.py --mode cpu --duration 30
python stress_test.py --mode memory --duration 30
python stress_test.py --mode disk --duration 30
python stress_test.py --mode wave
```

## Technical Details

**Resource Limits** (from docker-compose.yml):
- Max CPU: 1.0 core
- Max Memory: 512 MB
- The simulator respects these limits

**File Locations**:
- Temp files: `/tmp/sysinsight_workload/`
- Logs: Container stdout/stderr
- Simulator script: `/home/app/web/workload_simulator.py`

## Benefits for Presentations

Having realistic activity provides:
1. **Dynamic visualizations** - Charts show real changes
2. **Alert demonstrations** - Warning/critical states can be triggered
3. **Real-world simulation** - Mimics production environments
4. **Better engagement** - More interesting than flat lines
5. **Feature showcase** - All monitoring capabilities visible

## Disable Workload Simulator

If you want to run without the simulator:

**Option 1**: Modify `start.sh`:
```bash
# Comment out workload simulator line
# python3 /home/app/web/workload_simulator.py &

# Just run Gunicorn
exec gunicorn -c gunicorn_config.py wsgi:app
```

**Option 2**: Override CMD in docker-compose.yml:
```yaml
services:
  web:
    # ...
    command: gunicorn -c gunicorn_config.py wsgi:app
```

## Troubleshooting

**High CPU/Memory?**
- The simulator is designed to stay within container limits
- Adjust intensity in `workload_simulator.py`

**No fluctuations?**
- Check if workload simulator is running: `docker exec sysinsight ps aux | grep workload`
- View logs: `docker logs sysinsight`

**Want more/less activity?**
- Edit `workload_simulator.py` and rebuild container
- Adjust sleep times, allocation sizes, or worker counts
