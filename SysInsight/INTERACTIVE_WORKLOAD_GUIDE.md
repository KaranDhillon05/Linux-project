# 🎮 Interactive Workload Controller - User Guide

## What is This?

A **simple menu-driven application** that lets you generate different types of system load **on demand** to see real-time changes in your SysInsight monitoring dashboard.

**No hardcoded programs running in background!** You control when and what runs.

---

## 🚀 Quick Start

### Method 1: Launch Script (Easiest)
```bash
./launch_workload.sh
```

This will give you options to run inside the container or on your host.

### Method 2: Run Directly in Container
```bash
docker exec -it sysinsight python3 /home/app/web/workload_menu.py
```

### Method 3: Run on Host Machine
```bash
python3 workload_menu.py
```

---

## 📋 What Can You Do?

The interactive menu offers these options:

### 1. 🔥 CPU Stress Test (30s)
- Generates **CPU load** for 30 seconds
- You'll see **CPU% increase** on your dashboard
- Good for testing CPU monitoring

**What happens:**
- Performs mathematical calculations continuously
- CPU usage jumps to 10-30%
- Returns to normal after 30 seconds

### 2. 🧠 Memory Allocation (100 MB for 30s)
- Allocates **100 MB of memory** and holds it for 30 seconds
- You'll see **Memory% increase** on your dashboard
- Good for testing memory monitoring

**What happens:**
- Allocates memory in chunks
- Memory usage increases gradually
- Memory is freed after 30 seconds

### 3. 💾 Disk I/O Test (50 operations)
- Performs **50 file read/write operations**
- You'll see **Disk I/O increase** on your dashboard
- Good for testing disk monitoring

**What happens:**
- Creates temporary files (1MB each)
- Reads them back
- Deletes them (auto-cleanup)
- Disk I/O stats increase

### 4. ⚡ Mixed Workload (60s)
- Runs **CPU + Memory + Disk** all at once for 60 seconds
- You'll see **ALL metrics increase** simultaneously
- Best for demonstrating full system monitoring

**What happens:**
- Stresses all three resources at the same time
- Most dramatic dashboard changes
- Perfect for presentations!

### 5. 📊 Show Current Metrics
- Displays current system stats from the API
- Shows CPU%, Memory%, Disk I/O
- No load generated, just displays info

### 6. 🔧 Custom Workload
- Create your own custom test
- Choose type: CPU, Memory, or Disk
- Set duration and size
- Full control!

### 7. ❌ Exit
- Cleanly exits the application

---

## 🎬 Usage Example

```
$ ./launch_workload.sh

╔════════════════════════════════════════════════════════╗
║     SysInsight - Workload Generator Launcher          ║
╚════════════════════════════════════════════════════════╝

🐳 Launching workload menu inside container...

=============================================================
     SysInsight - Interactive Workload Controller
=============================================================

┌────────────────────────────────────────────────────────┐
│                   WORKLOAD OPTIONS                     │
└────────────────────────────────────────────────────────┘

  1. 🔥 CPU Stress Test (30s)
  2. 🧠 Memory Allocation (100 MB for 30s)
  3. 💾 Disk I/O Test (50 operations)
  4. ⚡ Mixed Workload (60s - CPU+Memory+Disk)
  5. 📊 Show Current Metrics
  6. 🔧 Custom Workload
  7. ❌ Exit

Enter your choice (1-7): 
```

---

## 📊 For Your Presentation

### Step-by-Step Demo Flow:

1. **Open your dashboard** in browser:
   ```
   http://localhost:5001
   ```

2. **Run the workload controller** in terminal:
   ```bash
   ./launch_workload.sh
   ```

3. **Show baseline metrics** (Option 5):
   - Shows current low usage
   - "As you can see, the system is idle..."

4. **Run CPU stress** (Option 1):
   - Select option 1
   - Switch to browser
   - Point out: "Watch the CPU graph increase in real-time!"
   - Wait 30 seconds
   - Point out: "See how it returns to normal?"

5. **Run mixed workload** (Option 4):
   - Select option 4
   - Switch to browser
   - "Now let's stress all three resources simultaneously"
   - Point out all three graphs changing
   - "This demonstrates real-world server load"

6. **Show metrics again** (Option 5):
   - "And we can query the API to see exact values"

---

## 🎯 Benefits vs Background Simulator

### Background Simulator (Old Way)
- ✅ Automatic fluctuations
- ❌ Always running (can't control)
- ❌ Hardcoded behavior
- ❌ Can't demonstrate specific scenarios

### Interactive Menu (New Way)
- ✅ **Full control** - you decide when to run
- ✅ **On-demand** - only runs when you want
- ✅ **Customizable** - adjust duration, size, type
- ✅ **Perfect for demos** - trigger specific scenarios
- ✅ **Clean** - no background noise

---

## 🔧 Customization

### Modify Duration
```bash
# In the menu, select option 6 (Custom Workload)
# Then specify your own duration
```

### Modify Intensity

Edit `workload_menu.py` and change these values:

**CPU Stress:**
```python
# Line 36: Change range for more/less work
_ = sum(i ** 2 for i in range(10000))  # Increase 10000 for more load
```

**Memory Allocation:**
```python
# Line 50: Change default size
def memory_allocate(self, size_mb=100, duration=30):  # Change 100 to 200
```

**Disk I/O:**
```python
# Line 75: Change file size
f.write(os.urandom(1024 * 1024))  # 1MB, increase for larger files
```

---

## 🎮 Usage Tips

### Tip 1: Open Dashboard First
Always have `http://localhost:5001` open **before** running workloads so you can see changes in real-time.

### Tip 2: Use Mixed Workload for Impact
Option 4 (Mixed Workload) creates the most dramatic visual changes - perfect for presentations!

### Tip 3: Check Metrics Before & After
Use Option 5 to show the baseline, run a workload, then show Option 5 again to prove the change.

### Tip 4: Run Inside Container
For best results, always run inside the Docker container (this is what's being monitored).

### Tip 5: Custom Duration for Presentations
Use Option 6 to set exact durations that match your presentation timing.

---

## 🐛 Troubleshooting

### Menu won't start
```bash
# Check if container is running
docker ps

# If not, start it
docker-compose up -d
```

### Can't fetch metrics (Option 5)
```bash
# Check if Flask app is responding
curl http://localhost:5001/health

# Check container logs
docker logs sysinsight
```

### "Command not found"
```bash
# Make sure script is executable
chmod +x launch_workload.sh
chmod +x workload_menu.py
```

### Running on host but monitoring container?
The dashboard monitors the **container**, so run workloads **inside the container** for them to show up:
```bash
docker exec -it sysinsight python3 /home/app/web/workload_menu.py
```

---

## 📝 Commands Cheat Sheet

```bash
# Launch the menu (recommended)
./launch_workload.sh

# Run directly in container
docker exec -it sysinsight python3 /home/app/web/workload_menu.py

# Run on host
python3 workload_menu.py

# Copy updated file to container (if you modify it)
docker cp workload_menu.py sysinsight:/home/app/web/workload_menu.py

# Check what's running in container
docker exec sysinsight ps aux

# View dashboard
open http://localhost:5001  # macOS
xdg-open http://localhost:5001  # Linux
```

---

## 🎓 What This Demonstrates

### Technical Skills
- **System Programming**: Understanding CPU, memory, disk operations
- **Python Threading**: Parallel workload execution
- **Interactive CLIs**: User-friendly menu interfaces
- **Docker Integration**: Running tools inside containers
- **Real-time Monitoring**: Seeing live system changes

### For Presentations
- **Control**: You decide what runs and when
- **Clarity**: Each workload demonstrates specific monitoring
- **Impact**: Visual proof of monitoring capabilities
- **Professional**: Clean, interactive, polished tool

---

## 🚀 Quick Demo Script

**For a 3-minute demo:**

1. "Let me show you the interactive workload controller" (15 sec)
2. Run `./launch_workload.sh` (5 sec)
3. "First, let's see baseline metrics" - Option 5 (10 sec)
4. "Now let's generate some CPU load" - Option 1 (30 sec)
5. Switch to dashboard - "Watch the CPU graph update" (20 sec)
6. "Now let's stress all resources" - Option 4 (60 sec)
7. Switch to dashboard - "All three metrics responding" (30 sec)
8. "And we're back to normal" - show graphs returning (20 sec)

**Total: ~3 minutes of impressive demo!**

---

**Enjoy your interactive workload controller!** 🎉
