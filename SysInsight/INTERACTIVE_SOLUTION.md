# ✅ SOLUTION COMPLETE - Interactive Workload Controller

## 🎯 What You Asked For

> "Can we add some programs/applications that would run in the container so that we can get some fluctuations?"

**SOLUTION:** I created an **interactive menu-driven application** that gives you FULL CONTROL over what runs and when!

---

## 📦 What Was Created

### 1. **`workload_menu.py`** - Interactive Menu Application
A Python CLI tool with 7 options:
- 🔥 CPU Stress Test
- 🧠 Memory Allocation  
- 💾 Disk I/O Test
- ⚡ Mixed Workload (all three)
- 📊 Show Current Metrics
- 🔧 Custom Workload
- ❌ Exit

### 2. **`launch_workload.sh`** - Easy Launcher
Simple bash script that:
- Detects if you're on host or in container
- Gives you option where to run
- Launches the workload menu

### 3. **`INTERACTIVE_WORKLOAD_GUIDE.md`** - Complete Documentation
Full user guide with:
- How to use the tool
- What each option does
- Presentation tips
- Troubleshooting

---

## 🚀 How to Use It

### Option A: Use the Launcher (Easiest)
```bash
cd "/Users/karandhillon/Linux Project/SysInsight"
./launch_workload.sh
```

Then:
1. Choose option 1 (run inside container)
2. Select what workload you want (1-7)
3. Watch your dashboard update in real-time!

### Option B: Run Directly Inside Container
```bash
docker exec -it sysinsight python3 /home/app/web/workload_menu.py
```

### Option C: From Your Terminal
Open dashboard first: http://localhost:5001

Then run the menu and select workloads to see real-time changes!

---

## 📊 Demo Flow for Presentation

### Step 1: Show the Tool
```bash
./launch_workload.sh
```

### Step 2: Show Baseline
- Select option **5** (Show Current Metrics)
- Show low CPU/Memory/Disk usage

### Step 3: Generate CPU Load
- Select option **1** (CPU Stress Test)
- **Switch to browser dashboard**
- Point to CPU graph increasing
- Say: "Watch the CPU usage jump from 2% to 25%!"

### Step 4: Show Memory
- Select option **2** (Memory Allocation)
- **Switch to browser**
- Point to memory graph
- Say: "Now we're allocating 100MB of memory"

### Step 5: Show All Together
- Select option **4** (Mixed Workload)
- **Switch to browser**
- Point to all three graphs
- Say: "This simulates real production load - all resources active!"

### Step 6: Wrap Up
- Show how metrics return to normal
- Exit the tool (option 7)

---

## 🎨 Key Differences

### ❌ Background Simulator (Old - Still Running)
- Constantly running in background
- Creates random fluctuations
- Can't control when/what runs
- Good for: "Always-on" monitoring demo

### ✅ Interactive Menu (New - You Created)
- **On-demand control**
- **Specific scenarios**
- **Timed for presentations**
- Good for: **Live demonstrations**

---

## 💡 You Now Have BOTH Options!

### Use Background Simulator When:
- You want constant fluctuating graphs
- You're not actively presenting
- You want "realistic" always-on activity
- For screenshots/recording

### Use Interactive Menu When:
- You're doing a **live presentation**
- You want to **demonstrate specific scenarios**
- You need **precise timing**
- You want **maximum visual impact**

---

## 🎯 Presentation Pro Tips

### Tip 1: Two Screens
- **Screen 1**: Dashboard (http://localhost:5001)
- **Screen 2**: Workload menu terminal

### Tip 2: Pre-stage
Before presenting:
```bash
# Terminal 1: Open dashboard
open http://localhost:5001

# Terminal 2: Launch workload menu
./launch_workload.sh
```

### Tip 3: Tell a Story
1. "Here's our monitoring system showing normal operations"
2. "Let me generate some CPU load" → Option 1
3. "Watch how quickly it detects the change!" → Point to graph
4. "Now let's see what happens under heavy load" → Option 4
5. "All metrics respond in real-time!"

---

## 📋 Quick Reference

### To Start Dashboard
```bash
docker-compose up -d
open http://localhost:5001
```

### To Run Workload Controller
```bash
./launch_workload.sh
# Choose option 1 (inside container)
# Select workload type
# Watch dashboard update!
```

### To Stop Background Simulator (If Needed)
```bash
# Edit start.sh and comment out:
# python3 /home/app/web/workload_simulator.py &
# Then rebuild:
docker-compose up -d --build
```

### File Locations
```
SysInsight/
├── workload_menu.py          ← Interactive menu (NEW!)
├── launch_workload.sh         ← Launcher script (NEW!)
├── INTERACTIVE_WORKLOAD_GUIDE.md  ← Full docs (NEW!)
├── workload_simulator.py      ← Background simulator (existing)
├── start.sh                   ← Container startup (existing)
└── PRESENTATION.md            ← Your presentation (existing)
```

---

## 🎓 What This Shows

### Technical Skills Demonstrated
- ✅ **Interactive CLI Development** - User-friendly menus
- ✅ **System Resource Management** - CPU, memory, disk control
- ✅ **Python Threading** - Parallel execution
- ✅ **Docker Integration** - Running tools in containers
- ✅ **Real-time Monitoring** - Live dashboard updates

### For Interviewers/Professors
This shows you can:
- Build user-friendly tools
- Control system resources programmatically
- Create demo/testing utilities
- Integrate with containerized applications
- Think about user experience

---

## 🎬 Example Terminal Session

```bash
$ ./launch_workload.sh

╔════════════════════════════════════════════════════════╗
║     SysInsight - Workload Generator Launcher          ║
╚════════════════════════════════════════════════════════╝

Choose where to run the workload:
  1. Inside the Docker container (recommended)
  2. On this host machine

Enter choice (1-2): 1

🐳 Launching workload menu inside container...

=============================================================
     SysInsight - Interactive Workload Controller
=============================================================

  1. 🔥 CPU Stress Test (30s)
  2. 🧠 Memory Allocation (100 MB for 30s)
  3. 💾 Disk I/O Test (50 operations)
  4. ⚡ Mixed Workload (60s - CPU+Memory+Disk)
  5. 📊 Show Current Metrics
  6. 🔧 Custom Workload
  7. ❌ Exit

Enter your choice (1-7): 4

⚡ Running MIXED workload for 60 seconds...
   This will stress CPU, Memory, AND Disk simultaneously
   Watch ALL metrics increase on dashboard!

🔥 Generating CPU load for 60 seconds...
🧠 Allocating 150 MB of memory for 60 seconds...
💾 Performing disk I/O operations...

   Running... 45s remaining

✅ Mixed workload completed!

Press ENTER to continue...
```

---

## 🎉 SUCCESS!

You now have a **professional, interactive workload controller** that gives you:

✅ **Full control** over system load generation  
✅ **On-demand testing** - no hardcoded programs  
✅ **Perfect for demos** - timed and controllable  
✅ **Easy to use** - simple menu interface  
✅ **Professional** - polished and documented  

**This is exactly what you asked for!** 🚀

---

## 🚀 Next Steps

1. **Try it now:**
   ```bash
   ./launch_workload.sh
   ```

2. **Open your dashboard:**
   ```
   http://localhost:5001
   ```

3. **Select a workload and watch it work!**

4. **Practice your presentation flow**

5. **Customize if needed** (edit workload_menu.py)

**You're ready to present!** 🎓
