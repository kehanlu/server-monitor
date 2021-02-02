import os
import json

class GPU():
    def __init__(self, index, name, memory_total, memory_free, memory_used, utilization_gpu):
        self.index = index
        self.name = name
        self.memory_total = int(memory_total.split()[0])
        self.memory_free = int(memory_free.split()[0])
        self.memory_used = int(memory_used.split()[0])
        self.utilization_gpu = int(utilization_gpu.split()[0])
    def __repr__(self):
        return f"GPU {self.index}: {self.name:20.20},{self.memory_used:>10}/{self.memory_total:<10},{self.utilization_gpu}"

    def get_info(self):
        return {
            "index": self.index,
            "name": self.name,
            "memory_total": self.memory_total,
            "memory_free": self.memory_free,
            "memory_used": self.memory_used,
            "utilization_gpu": self.utilization_gpu
        }

class NvidiaSMI():    
    def __init__(self):
        query = [
            "index",
            "name",
            "memory.total",
            "memory.free",
            "memory.used",
            "utilization.gpu",
        ]
        self.gpu_list = list()
        for gpu_info in os.popen(f"nvidia-smi --query-gpu={','.join(query)} --format=csv,noheader").readlines():
            gpu_info = gpu_info.strip().split(',')
            gpu = dict()
            for c,info in zip(query, gpu_info):
                c = c.replace(".","_")
                gpu[c] = info.strip()
            self.gpu_list.append(GPU(**gpu))
        
        self.processes = list()
        for process in os.popen("nvidia-smi --query-compute-apps=gpu_name,name,used_gpu_memory --format=csv,noheader").readlines():
            p = process.split(',')
            self.processes.append({
                "gpu_name": p[0].strip(),
                "process_name": p[1].strip(),
                "memory_used": p[2].strip()
            })
            
    def show(self):
        for gpu in self.gpu_list:
            print(gpu)

    def to_json(self):
        return json.dumps({
            "gpus": [gpu.get_info() for gpu in self.gpu_list],
            "processes": self.processes
        })
    def get_info(self):
        return {
            "gpus": [gpu.get_info() for gpu in self.gpu_list],
            "processes": self.processes
        }

class RAM():
    def __init__(self):
        info = os.popen("free -g").read().split('\n')[1].split()
        self.info = {
            'total': int(info[1]),
            'used': int(info[2]),
            'available': int(info[6])
        }

    def to_json(self):
        return self.info

    def get_info(self):
        return self.info