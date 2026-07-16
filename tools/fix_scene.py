#!/usr/bin/env python3
"""外科手术式修复 MainScene.scene：
- 给名为 GameManager 的节点(90) 补上 GameManager 脚本组件（之前缺失）
- 新增 FoodSpawner 节点与组件（之前完全缺失）
- 绑定所有交叉引用
不改动任何已有 UI 布局与绑定。
"""
import json, shutil, os
from pathlib import Path

SCENE = Path('assets/scenes/MainScene.scene')
BACKUP = Path('assets/scenes/MainScene.scene.bak')

# 反向推导出的 Cocos 压缩 uuid（已用 4 个已知脚本验证）
GM_TYPE = '1ccfcftmqNAFoz0YQNf9/3n'      # GameManager
FS_TYPE = 'ca8e4bg8Y1DrbMHNepPtF6z'      # FoodSpawner
FOOD_PREFAB_UUID = 'e47b70e3-718e-420a-ba57-f487bfc414d4'

def main():
    shutil.copy(SCENE, BACKUP)
    arr = json.load(open(SCENE, encoding='utf-8'))

    def add(obj):
        obj['__id__'] = len(arr)
        arr.append(obj)
        return obj['__id__']

    def ref(i):
        return {'__id__': i}

    # 关键已有索引
    NODE_GM = 90          # 名为 GameManager 的节点
    COMP_SC = 91         # 该节点上的 SnakeController 组件
    COMP_GRID = 87       # GameBoard 上的 GridSystem
    COMP_UI = 80         # Canvas 上的 UIManager
    COMP_AUDIO = 96      # AudioManager 节点上的 AudioManager
    NODE_FOODCONTAINER = 83

    # 新增 FoodSpawner 节点
    fs_node_id = add({
        '__type__': 'cc.Node',
        '_name': 'FoodSpawner',
        '_objFlags': 0,
        '__editorExtras__': {},
        '_parent': ref(1),
        '_children': [],
        '_active': True,
        '_components': [],   # 稍后填入
        '_prefab': None,
        '_lpos': {'__type__': 'cc.Vec3', 'x': 0, 'y': 0, 'z': 0},
        '_lrot': {'__type__': 'cc.Quat', 'x': 0, 'y': 0, 'z': 0, 'w': 1},
        '_lscale': {'__type__': 'cc.Vec3', 'x': 1, 'y': 1, 'z': 1},
        '_layer': 1073741824,
        '_euler': {'__type__': 'cc.Vec3', 'x': 0, 'y': 0, 'z': 0},
        '_id': ''
    })

    # 新增 FoodSpawner 组件
    fs_comp_id = add({
        '__type__': FS_TYPE,
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': ref(fs_node_id),
        '_enabled': True,
        '__prefab': None,
        'gridSystem': ref(COMP_GRID),
        'snakeController': ref(COMP_SC),
        'foodPrefab': {'__uuid__': FOOD_PREFAB_UUID, '__expectedType__': 'cc.Prefab'},
        'foodContainer': ref(NODE_FOODCONTAINER),
        '_id': ''
    })
    arr[fs_node_id]['_components'] = [ref(fs_comp_id)]

    # 新增 GameManager 组件（挂到原 GameManager 节点 90）
    gm_comp_id = add({
        '__type__': GM_TYPE,
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': ref(NODE_GM),
        '_enabled': True,
        '__prefab': None,
        'gridSystem': ref(COMP_GRID),
        'snakeController': ref(COMP_SC),
        'foodSpawner': ref(fs_comp_id),
        'uiManager': ref(COMP_UI),
        'audioManager': ref(COMP_AUDIO),
        '_id': ''
    })

    # 把 GameManager 组件挂到节点 90（与已有 SnakeController 共存）
    arr[NODE_GM]['_components'] = [ref(COMP_SC), ref(gm_comp_id)]

    # 将 FoodSpawner 节点加入场景根节点
    scene_idx = None
    for i, o in enumerate(arr):
        if isinstance(o, dict) and o.get('__type__') == 'cc.Scene':
            scene_idx = i
            break
    arr[scene_idx]['_children'].append(ref(fs_node_id))

    json.dump(arr, open(SCENE, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print('OK. backup ->', BACKUP)
    print('added FoodSpawner node id =', fs_node_id, 'comp id =', fs_comp_id)
    print('added GameManager comp id =', gm_comp_id)
    print('node90 components =', arr[NODE_GM]['_components'])
    print('scene children =', arr[scene_idx]['_children'])

if __name__ == '__main__':
    main()
