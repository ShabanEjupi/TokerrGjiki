#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
CLUSTER MONITOR - Real-Time Cluster Monitoring Dashboard
================================================================================
Monitor all 10 VMs in real-time with colorful terminal output
Usage: python3 cluster_monitor.py
================================================================================
"""

import subprocess
import time
import sys
from datetime import datetime
from collections import defaultdict

# Colors
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Configuration
MASTER_HOST = "185.182.158.150"
MASTER_PORT = 8022
WORKER_PORTS = list(range(8023, 8032))  # 8023-8031
USER = "krenuser"
REFRESH_INTERVAL = 5  # seconds

def ssh_command(port, command):
    """Execute SSH command and return output"""
    try:
        result = subprocess.run(
            ["ssh", "-p", str(port), "-o", "ConnectTimeout=2", 
             "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
             f"{USER}@{MASTER_HOST}", command],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip(), True
    except Exception as e:
        return str(e), False

def clear_screen():
    """Clear terminal screen"""
    print("\033[2J\033[H", end="")

def print_header():
    """Print dashboard header"""
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}SPARK CLUSTER MONITOR - Real-Time Financial Dashboard{Colors.END}")
    print(f"{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.GRAY}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print()

def check_node_status(port):
    """Check if node is accessible"""
    _, success = ssh_command(port, "echo OK")
    return success

def get_node_resources(port):
    """Get CPU, memory, and disk usage"""
    cmd = """
    echo "CPU:$(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1)"
    echo "MEM:$(free | grep Mem | awk '{printf \"%.1f\", $3/$2 * 100}')"
    echo "DISK:$(df -h ~ | tail -1 | awk '{print $5}' | sed 's/%//')"
    """
    output, success = ssh_command(port, cmd)
    
    if not success:
        return None, None, None
    
    resources = {}
    for line in output.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            resources[key] = value
    
    return (
        float(resources.get('CPU', 0)),
        float(resources.get('MEM', 0)),
        int(resources.get('DISK', 0))
    )

def get_spark_processes(port):
    """Check if Spark processes are running"""
    cmd = "ps aux | grep -E '(spark.*Master|spark.*Worker)' | grep -v grep | wc -l"
    output, success = ssh_command(port, cmd)
    
    if success:
        return int(output) > 0
    return False

def get_app_processes(port):
    """Check if application processes are running"""
    processes = {}
    
    # Check data collector
    cmd = "ps aux | grep 'python3.*realtime_data_collector' | grep -v grep | wc -l"
    output, success = ssh_command(port, cmd)
    try:
        processes['collector'] = int(output) > 0 if success else False
    except ValueError:
        processes['collector'] = False
    
    # Check Spark processor
    cmd = "ps aux | grep 'spark-submit.*spark_streaming_processor' | grep -v grep | wc -l"
    output, success = ssh_command(port, cmd)
    try:
        processes['processor'] = int(output) > 0 if success else False
    except ValueError:
        processes['processor'] = False
    
    # Check web app
    cmd = "ps aux | grep 'python3.*app.py' | grep -v grep | wc -l"
    output, success = ssh_command(port, cmd)
    try:
        processes['webapp'] = int(output) > 0 if success else False
    except ValueError:
        processes['webapp'] = False
    
    return processes

def format_usage(value, threshold_warning=70, threshold_critical=90):
    """Format usage percentage with colors"""
    if value >= threshold_critical:
        color = Colors.RED
    elif value >= threshold_warning:
        color = Colors.YELLOW
    else:
        color = Colors.GREEN
    
    return f"{color}{value:5.1f}%{Colors.END}"

def print_node_info(name, port, is_online, cpu, mem, disk, has_spark, extra_info=None):
    """Print information for a single node"""
    # Status indicator
    status = f"{Colors.GREEN}●{Colors.END}" if is_online else f"{Colors.RED}●{Colors.END}"
    
    # Node name
    node_name = f"{Colors.BOLD}{name:12s}{Colors.END}"
    
    # Port
    port_str = f"{Colors.GRAY}:{port}{Colors.END}"
    
    # Resources
    if is_online and cpu is not None:
        cpu_str = format_usage(cpu)
        mem_str = format_usage(mem)
        disk_str = format_usage(disk)
    else:
        cpu_str = f"{Colors.GRAY}  N/A  {Colors.END}"
        mem_str = f"{Colors.GRAY}  N/A  {Colors.END}"
        disk_str = f"{Colors.GRAY}  N/A  {Colors.END}"
    
    # Spark status
    spark_str = f"{Colors.GREEN}✓{Colors.END}" if has_spark else f"{Colors.RED}✗{Colors.END}"
    
    # Extra info
    extra_str = extra_info if extra_info else ""
    
    print(f"{status} {node_name}{port_str:<7s} │ CPU: {cpu_str} │ MEM: {mem_str} │ DISK: {disk_str} │ Spark: {spark_str} {extra_str}")

def print_summary(stats):
    """Print cluster summary"""
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}CLUSTER SUMMARY{Colors.END}")
    print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
    
    # Nodes online
    online = stats['nodes_online']
    total = stats['nodes_total']
    online_color = Colors.GREEN if online == total else Colors.YELLOW
    print(f"  Nodes Online      : {online_color}{online}/{total}{Colors.END}")
    
    # Spark processes
    spark = stats['spark_running']
    spark_color = Colors.GREEN if spark == total else Colors.YELLOW
    print(f"  Spark Processes   : {spark_color}{spark}/{total}{Colors.END}")
    
    # Average resources
    if stats['avg_cpu'] is not None:
        print(f"  Avg CPU Usage     : {format_usage(stats['avg_cpu'])}")
        print(f"  Avg Memory Usage  : {format_usage(stats['avg_mem'])}")
        print(f"  Avg Disk Usage    : {format_usage(stats['avg_disk'])}")
    
    # Applications
    print()
    print(f"{Colors.BOLD}APPLICATION STATUS{Colors.END}")
    apps = stats['apps']
    collector_status = f"{Colors.GREEN}Running{Colors.END}" if apps.get('collector') else f"{Colors.RED}Stopped{Colors.END}"
    processor_status = f"{Colors.GREEN}Running{Colors.END}" if apps.get('processor') else f"{Colors.RED}Stopped{Colors.END}"
    webapp_status = f"{Colors.GREEN}Running{Colors.END}" if apps.get('webapp') else f"{Colors.RED}Stopped{Colors.END}"
    
    print(f"  Data Collector    : {collector_status}")
    print(f"  Spark Processor   : {processor_status}")
    print(f"  Web Application   : {webapp_status}")
    
    print()
    print(f"{Colors.BOLD}WEB INTERFACES{Colors.END}")
    print(f"  Spark Master UI   : {Colors.CYAN}http://{MASTER_HOST}:8080{Colors.END}")
    print(f"  Dashboard         : {Colors.CYAN}http://{MASTER_HOST}:5000{Colors.END}")
    
    print(f"{Colors.CYAN}{'─'*80}{Colors.END}")

def monitor_cluster():
    """Main monitoring loop"""
    try:
        while True:
            clear_screen()
            print_header()
            
            stats = {
                'nodes_online': 0,
                'nodes_total': 10,
                'spark_running': 0,
                'cpu_values': [],
                'mem_values': [],
                'disk_values': [],
                'apps': {}
            }
            
            # Check master node
            print(f"{Colors.BOLD}{Colors.BLUE}MASTER NODE{Colors.END}")
            print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
            
            is_online = check_node_status(MASTER_PORT)
            cpu, mem, disk = get_node_resources(MASTER_PORT)
            has_spark = get_spark_processes(MASTER_PORT)
            apps = get_app_processes(MASTER_PORT)
            
            stats['apps'] = apps
            
            if is_online:
                stats['nodes_online'] += 1
                if cpu is not None:
                    stats['cpu_values'].append(cpu)
                    stats['mem_values'].append(mem)
                    stats['disk_values'].append(disk)
            
            if has_spark:
                stats['spark_running'] += 1
            
            # Show app status
            app_status = []
            if apps.get('collector'):
                app_status.append(f"{Colors.GREEN}Collector{Colors.END}")
            if apps.get('processor'):
                app_status.append(f"{Colors.GREEN}Processor{Colors.END}")
            if apps.get('webapp'):
                app_status.append(f"{Colors.GREEN}WebApp{Colors.END}")
            
            extra_info = " │ Apps: " + ", ".join(app_status) if app_status else ""
            
            print_node_info("Master", MASTER_PORT, is_online, cpu, mem, disk, has_spark, extra_info)
            
            print()
            print(f"{Colors.BOLD}{Colors.BLUE}WORKER NODES{Colors.END}")
            print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
            
            # Check worker nodes
            for i, port in enumerate(WORKER_PORTS, 1):
                is_online = check_node_status(port)
                cpu, mem, disk = get_node_resources(port)
                has_spark = get_spark_processes(port)
                
                if is_online:
                    stats['nodes_online'] += 1
                    if cpu is not None:
                        stats['cpu_values'].append(cpu)
                        stats['mem_values'].append(mem)
                        stats['disk_values'].append(disk)
                
                if has_spark:
                    stats['spark_running'] += 1
                
                print_node_info(f"Worker {i}", port, is_online, cpu, mem, disk, has_spark)
            
            # Calculate averages
            if stats['cpu_values']:
                stats['avg_cpu'] = sum(stats['cpu_values']) / len(stats['cpu_values'])
                stats['avg_mem'] = sum(stats['mem_values']) / len(stats['mem_values'])
                stats['avg_disk'] = sum(stats['disk_values']) / len(stats['disk_values'])
            else:
                stats['avg_cpu'] = None
                stats['avg_mem'] = None
                stats['avg_disk'] = None
            
            # Print summary
            print_summary(stats)
            
            print()
            print(f"{Colors.GRAY}Refreshing every {REFRESH_INTERVAL} seconds... Press Ctrl+C to exit{Colors.END}")
            
            time.sleep(REFRESH_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Monitoring stopped.{Colors.END}\n")
        sys.exit(0)

if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.GREEN}Starting Cluster Monitor...{Colors.END}\n")
    time.sleep(1)
    monitor_cluster()
