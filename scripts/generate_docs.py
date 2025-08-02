#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动生成 Titan SDK 文档脚本
扫描 project 目录下的所有项目，完整拷贝每个项目目录到 source 下。
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List

class DocGenerator:
    def __init__(self, project_dir: str = "project", output_dir: str = "source"):
        self.project_dir = Path(project_dir)
        self.output_dir = Path(output_dir)
        self.categories = {
            "basic": [],
            "driver": [],
            "component": []
        }
        
    def scan_projects(self) -> Dict[str, List[str]]:
        """扫描 project 目录，按类别分类项目"""
        if not self.project_dir.exists():
            print(f"错误: {self.project_dir} 目录不存在")
            return {}
            
        for item in self.project_dir.iterdir():
            if item.is_dir():
                project_name = item.name
                if project_name.startswith("Titan_basic_"):
                    self.categories["basic"].append(project_name)
                elif project_name.startswith("Titan_driver_"):
                    self.categories["driver"].append(project_name)
                elif project_name.startswith("Titan_component_"):
                    self.categories["component"].append(project_name)
                    
        return self.categories
    
    def copy_project_directory(self, project_name: str, category: str):
        """完整拷贝项目目录"""
        source_project = self.project_dir / project_name
        dest_project = self.output_dir / f"{category}_examples" / project_name
        
        if source_project.exists():
            # 删除目标目录（如果存在）
            if dest_project.exists():
                shutil.rmtree(dest_project)
            
            # 完整拷贝项目目录
            shutil.copytree(source_project, dest_project)
            print(f"拷贝项目: {project_name} -> {dest_project}")
    
    def generate_category_index(self, category: str, projects: List[str]) -> str:
        """生成分类索引页面"""
        category_names = {
            "basic": "基础功能示例",
            "driver": "驱动示例", 
            "component": "组件示例"
        }
        
        category_name = category_names.get(category, category.title())
        
        content = f"""{category_name}
{'=' * len(category_name)}

这里包含了 Titan SDK 的 {category_name}。

.. toctree::
   :maxdepth: 2
   :caption: {category_name}

"""
        
        # 为每个项目生成文档链接
        for project in projects:
            # 生成项目标题
            title = project.replace("Titan_", "").replace("_", " ").title()
            
            # 添加到分类页面
            content += f"   {project}/README\n"
        
        content += f"\n这些示例展示了 Titan SDK 的 {category_name}。\n"
        return content
    
    def generate_main_index(self):
        """生成主索引页面"""
        content = """.. Titan_SDK_Docs documentation master file, created by sphinx-quickstart

欢迎来到 Titan_SDK_Docs 文档！
================================

.. toctree::
   :maxdepth: 2
   :caption: 目录

   getting_started/index
   basic_examples/index
   driver_examples/index
   component_examples/index
   usage/index
   api/index
   faq/index
   guide/index

项目简介
--------
这里是 Titan_SDK_Docs 的简要介绍。

Titan SDK 提供了丰富的示例项目，包括基础功能、驱动示例和组件示例。

"""
        
        index_path = self.output_dir / "index.rst"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def run(self):
        """运行文档生成器"""
        print("开始扫描项目...")
        categories = self.scan_projects()
        
        if not any(categories.values()):
            print("未找到任何项目")
            return
            
        print(f"找到项目:")
        for category, projects in categories.items():
            print(f"  {category}: {len(projects)} 个项目")
            for project in projects:
                print(f"    - {project}")
        
        # 生成分类索引和拷贝项目
        for category, projects in categories.items():
            if projects:
                print(f"\n处理 {category} 分类...")
                
                # 创建分类目录
                category_dir = self.output_dir / f"{category}_examples"
                category_dir.mkdir(parents=True, exist_ok=True)
                
                # 拷贝每个项目
                for project in projects:
                    self.copy_project_directory(project, category)
                
                # 生成分类索引
                index_content = self.generate_category_index(category, projects)
                index_path = category_dir / "index.rst"
                
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(index_content)
                
                print(f"已生成: {index_path}")
        
        # 生成主索引
        print("\n生成主索引...")
        self.generate_main_index()
        
        print("\n文档生成完成!")

if __name__ == "__main__":
    generator = DocGenerator()
    generator.run() 