
#!/usr/bin/env python3
import json
import shutil

# 配置文件路径
CONFIG_PATH = '/root/.openclaw/openclaw.json'
BACKUP_PATH = '/root/.openclaw/openclaw.json.bak.delete-learner'

# 备份原文件
shutil.copy2(CONFIG_PATH, BACKUP_PATH)
print(f"✅ 已备份原文件到: {BACKUP_PATH}")

# 读取配置
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 1. 从 main agent 的 allowAgents 中移除 learner
for agent in config['agents']['list']:
    if agent['id'] == 'main':
        if 'subagents' in agent and 'allowAgents' in agent['subagents']:
            if 'learner' in agent['subagents']['allowAgents']:
                agent['subagents']['allowAgents'].remove('learner')
                print("✅ 已从 main agent 的 allowAgents 中移除 learner")

# 2. 从 agents list 中移除整个 learner agent
original_length = len(config['agents']['list'])
config['agents']['list'] = [
    agent for agent in config['agents']['list']
    if agent['id'] != 'learner'
]
new_length = len(config['agents']['list'])

if original_length > new_length:
    print(f"✅ 已从 agents list 中移除 learner agent (原: {original_length}, 现: {new_length})")

# 保存修改后的配置
with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("\n🎉 LearnerBot 删除成功！")
print("\n📋 当前 agents:")
for agent in config['agents']['list']:
    print(f"   - {agent['id']}: {agent['identity']['name']} {agent['identity']['emoji']}")

