#!/usr/bin/env python3
"""
自主学习系统 - 磁盘空间管理
防止学习过程中产生的临时文件和搜索资料导致磁盘爆炸
"""

import os
import sys
import shutil
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta


class DiskSpaceManager:
    """磁盘空间管理器"""
    
    def __init__(self, 
                 workspace: str = None,
                 max_cache_size_mb: int = 500,  # 最大缓存大小（MB）
                 max_skills_size_mb: int = 1000,  # 最大技能文件总大小（MB）
                 retention_days: int = 30,  # 保留天数
                 min_free_space_gb: float = 5.0):  # 最小剩余空间（GB）
        
        self.workspace = workspace or str(Path.home() / ".openclaw" / "learner-workspace")
        self.max_cache_size_mb = max_cache_size_mb
        self.max_skills_size_mb = max_skills_size_mb
        self.retention_days = retention_days
        self.min_free_space_gb = min_free_space_gb
        
        # 目录定义
        self.cache_dir = Path(self.workspace) / "cache"
        self.temp_dir = Path(self.workspace) / "temp"
        self.skills_dir = Path(self.workspace) / "skills"
        self.logs_dir = Path(self.workspace) / "logs"
        
        # 确保目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保所有目录都存在"""
        for directory in [self.cache_dir, self.temp_dir, self.skills_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def check_disk_space(self) -> Dict[str, Any]:
        """
        检查磁盘空间
        
        返回: 磁盘空间信息
        """
        # 获取磁盘信息
        total, used, free = shutil.disk_usage(self.workspace)
        
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        # 获取各目录大小
        cache_size = self._get_dir_size(self.cache_dir)
        temp_size = self._get_dir_size(self.temp_dir)
        skills_size = self._get_dir_size(self.skills_dir)
        logs_size = self._get_dir_size(self.logs_dir)
        
        return {
            "disk": {
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(free_gb, 2),
                "used_percent": round(used / total * 100, 1),
                "is_critical": free_gb < self.min_free_space_gb
            },
            "workspace": {
                "cache_mb": round(cache_size / (1024**2), 2),
                "temp_mb": round(temp_size / (1024**2), 2),
                "skills_mb": round(skills_size / (1024**2), 2),
                "logs_mb": round(logs_size / (1024**2), 2),
                "total_mb": round((cache_size + temp_size + skills_size + logs_size) / (1024**2), 2)
            },
            "limits": {
                "max_cache_mb": self.max_cache_size_mb,
                "max_skills_mb": self.max_skills_size_mb,
                "retention_days": self.retention_days,
                "min_free_gb": self.min_free_space_gb
            }
        }
    
    def _get_dir_size(self, directory: Path) -> int:
        """获取目录大小（字节）"""
        if not directory.exists():
            return 0
        
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, IOError):
                        pass
        except (OSError, IOError):
            pass
        
        return total_size
    
    def cleanup_if_needed(self) -> Dict[str, Any]:
        """
        如果需要，执行清理
        
        返回: 清理结果
        """
        result = {
            "cleaned": False,
            "freed_mb": 0,
            "actions": []
        }
        
        # 检查磁盘空间
        disk_info = self.check_disk_space()
        
        # 1. 如果剩余空间不足，执行紧急清理
        if disk_info["disk"]["is_critical"]:
            print(f"⚠️  磁盘空间不足！剩余 {disk_info['disk']['free_gb']} GB")
            freed = self._emergency_cleanup()
            result["freed_mb"] += freed
            result["actions"].append(f"紧急清理: 释放 {freed} MB")
        
        # 2. 检查缓存大小
        cache_mb = disk_info["workspace"]["cache_mb"]
        if cache_mb > self.max_cache_size_mb:
            print(f"⚠️  缓存超过限制！当前 {cache_mb} MB, 限制 {self.max_cache_size_mb} MB")
            freed = self._cleanup_cache()
            result["freed_mb"] += freed
            result["actions"].append(f"清理缓存: 释放 {freed} MB")
        
        # 3. 清理临时文件
        freed = self._cleanup_temp_files()
        if freed > 0:
            result["freed_mb"] += freed
            result["actions"].append(f"清理临时文件: 释放 {freed} MB")
        
        # 4. 清理过期文件
        freed = self._cleanup_old_files()
        if freed > 0:
            result["freed_mb"] += freed
            result["actions"].append(f"清理过期文件: 释放 {freed} MB")
        
        # 5. 检查技能文件总大小
        skills_mb = disk_info["workspace"]["skills_mb"]
        if skills_mb > self.max_skills_size_mb:
            print(f"⚠️  技能文件超过限制！当前 {skills_mb} MB, 限制 {self.max_skills_size_mb} MB")
            freed = self._cleanup_old_skills()
            result["freed_mb"] += freed
            result["actions"].append(f"清理旧技能: 释放 {freed} MB")
        
        # 6. 清理日志
        freed = self._cleanup_logs()
        if freed > 0:
            result["freed_mb"] += freed
            result["actions"].append(f"清理日志: 释放 {freed} MB")
        
        result["cleaned"] = len(result["actions"]) > 0
        
        return result
    
    def _emergency_cleanup(self) -> int:
        """紧急清理（释放尽可能多的空间）"""
        freed = 0
        
        # 清理所有临时文件
        freed += self._cleanup_temp_files()
        
        # 清理所有缓存
        freed += self._cleanup_cache()
        
        # 清理所有日志
        freed += self._cleanup_logs()
        
        # 清理检查点
        freed += self._cleanup_checkpoints()
        
        return freed
    
    def _cleanup_temp_files(self) -> int:
        """清理临时文件"""
        freed = 0
        
        if not self.temp_dir.exists():
            return freed
        
        try:
            for item in self.temp_dir.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink()
                        freed += size
                    elif item.is_dir():
                        size = self._get_dir_size(item)
                        shutil.rmtree(item)
                        freed += size
                except (OSError, IOError):
                    pass
        except (OSError, IOError):
            pass
        
        if freed > 0:
            print(f"✅ 清理临时文件: 释放 {freed / (1024**2):.2f} MB")
        
        return int(freed / (1024**2))  # 转换为 MB
    
    def _cleanup_cache(self) -> int:
        """清理缓存"""
        freed = 0
        
        if not self.cache_dir.exists():
            return freed
        
        try:
            for item in self.cache_dir.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink()
                        freed += size
                    elif item.is_dir():
                        size = self._get_dir_size(item)
                        shutil.rmtree(item)
                        freed += size
                except (OSError, IOError):
                    pass
        except (OSError, IOError):
            pass
        
        if freed > 0:
            print(f"✅ 清理缓存: 释放 {freed / (1024**2):.2f} MB")
        
        return int(freed / (1024**2))  # 转换为 MB
    
    def _cleanup_old_files(self) -> int:
        """清理过期文件"""
        freed = 0
        cutoff_time = datetime.now() - timedelta(days=self.retention_days)
        
        for directory in [self.cache_dir, self.temp_dir]:
            if not directory.exists():
                continue
            
            try:
                for item in directory.iterdir():
                    try:
                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if mtime < cutoff_time:
                            if item.is_file():
                                size = item.stat().st_size
                                item.unlink()
                                freed += size
                            elif item.is_dir():
                                size = self._get_dir_size(item)
                                shutil.rmtree(item)
                                freed += size
                    except (OSError, IOError):
                        pass
            except (OSError, IOError):
                pass
        
        if freed > 0:
            print(f"✅ 清理过期文件: 释放 {freed / (1024**2):.2f} MB")
        
        return int(freed / (1024**2))  # 转换为 MB
    
    def _cleanup_old_skills(self) -> int:
        """清理旧的技能文件"""
        freed = 0
        
        if not self.skills_dir.exists():
            return freed
        
        # 获取所有技能文件并按时间排序
        skills = []
        try:
            for item in self.skills_dir.iterdir():
                if item.is_file() and item.suffix == '.md':
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                    size = item.stat().st_size
                    skills.append((item, mtime, size))
        except (OSError, IOError):
            pass
        
        # 按时间排序（最新的在前）
        skills.sort(key=lambda x: x[1], reverse=True)
        
        # 计算总大小，删除旧文件直到满足限制
        total_size = sum(s[2] for s in skills)
        max_size_bytes = self.max_skills_size_mb * 1024**2
        
        for skill_path, mtime, size in reversed(skills):  # 从最旧的开始删除
            if total_size <= max_size_bytes:
                break
            
            try:
                skill_path.unlink()
                total_size -= size
                freed += size
                print(f"   删除旧技能: {skill_path.name} ({size / 1024:.2f} KB)")
            except (OSError, IOError):
                pass
        
        if freed > 0:
            print(f"✅ 清理旧技能: 释放 {freed / (1024**2):.2f} MB")
        
        return int(freed / (1024**2))  # 转换为 MB
    
    def _cleanup_logs(self) -> int:
        """清理日志文件"""
        freed = 0
        
        if not self.logs_dir.exists():
            return freed
        
        cutoff_time = datetime.now() - timedelta(days=7)  # 只保留7天的日志
        
        try:
            for item in self.logs_dir.iterdir():
                try:
                    if item.is_file():
                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if mtime < cutoff_time:
                            size = item.stat().st_size
                            item.unlink()
                            freed += size
                except (OSError, IOError):
                    pass
        except (OSError, IOError):
            pass
        
        if freed > 0:
            print(f"✅ 清理日志: 释放 {freed / (1024**2):.2f} MB")
        
        return int(freed / (1024**2))  # 转换为 MB
    
    def _cleanup_checkpoints(self) -> int:
        """清理检查点文件"""
        freed = 0
        
        # 清理 /tmp 下的检查点文件
        tmp_dir = Path("/tmp")
        if not tmp_dir.exists():
            return freed
        
        try:
            for item in tmp_dir.glob("learner_checkpoint_*.json"):
                try:
                    size = item.stat().st_size
                    item.unlink()
                    freed += size
                except (OSError, IOError):
                    pass
        except (OSError, IOError):
            pass
        
        if freed > 0:
            print(f"✅ 清理检查点: 释放 {freed / (1024**2):.2f} MB")
        
        return int(freed / (1024**2))  # 转换为 MB
    
    def monitor_during_learning(self, interval_seconds: int = 60):
        """
        学习过程中定期监控磁盘空间
        
        参数:
            interval_seconds: 检查间隔（秒）
        """
        print("🔍 开始磁盘空间监控...")
        
        while True:
            # 检查磁盘空间
            disk_info = self.check_disk_space()
            
            # 显示状态
            print(f"\n📊 磁盘状态:")
            print(f"   剩余空间: {disk_info['disk']['free_gb']} GB / {disk_info['disk']['total_gb']} GB")
            print(f"   工作空间: {disk_info['workspace']['total_mb']} MB")
            print(f"     - 缓存: {disk_info['workspace']['cache_mb']} MB")
            print(f"     - 临时: {disk_info['workspace']['temp_mb']} MB")
            print(f"     - 技能: {disk_info['workspace']['skills_mb']} MB")
            print(f"     - 日志: {disk_info['workspace']['logs_mb']} MB")
            
            # 如果需要清理，执行清理
            if disk_info["disk"]["is_critical"]:
                print("\n⚠️  磁盘空间不足，执行清理...")
                cleanup_result = self.cleanup_if_needed()
                
                if cleanup_result["cleaned"]:
                    print(f"✅ 清理完成: 释放 {cleanup_result['freed_mb']} MB")
                    for action in cleanup_result["actions"]:
                        print(f"   - {action}")
            
            # 等待下一次检查
            time.sleep(interval_seconds)


def manage_disk_space():
    """磁盘空间管理（便捷函数）"""
    manager = DiskSpaceManager()
    
    # 检查磁盘空间
    print("📊 磁盘空间检查")
    print("="*60)
    disk_info = manager.check_disk_space()
    
    print(f"磁盘总容量: {disk_info['disk']['total_gb']} GB")
    print(f"已使用: {disk_info['disk']['used_gb']} GB ({disk_info['disk']['used_percent']}%)")
    print(f"剩余空间: {disk_info['disk']['free_gb']} GB")
    
    if disk_info["disk"]["is_critical"]:
        print("⚠️  警告: 剩余空间不足！")
    
    print()
    print(f"工作空间使用:")
    print(f"  缓存: {disk_info['workspace']['cache_mb']} MB / {disk_info['limits']['max_cache_mb']} MB")
    print(f"  临时: {disk_info['workspace']['temp_mb']} MB")
    print(f"  技能: {disk_info['workspace']['skills_mb']} MB / {disk_info['limits']['max_skills_mb']} MB")
    print(f"  日志: {disk_info['workspace']['logs_mb']} MB")
    print(f"  总计: {disk_info['workspace']['total_mb']} MB")
    print()
    
    # 执行清理
    print("🧹 执行清理...")
    print("="*60)
    cleanup_result = manager.cleanup_if_needed()
    
    if cleanup_result["cleaned"]:
        print(f"✅ 清理完成！")
        print(f"   释放空间: {cleanup_result['freed_mb']} MB")
        print("   执行操作:")
        for action in cleanup_result["actions"]:
            print(f"   - {action}")
    else:
        print("✅ 无需清理")
    
    return disk_info


if __name__ == "__main__":
    # 测试
    print("🧪 磁盘空间管理测试")
    print()
    
    result = manage_disk_space()
    
    print()
    print("="*60)
    print("✅ 测试完成")
