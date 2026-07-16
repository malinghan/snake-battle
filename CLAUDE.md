# CLAUDE.md — SnakeBattle 贪吃蛇大作战

> 本文件面向 AI 助手（Claude / CodeBuddy 等），帮助快速理解项目结构、开发流程与关键技术约束。

## 项目概述

基于 **Cocos Creator 3.8.8** 的经典贪吃蛇游戏。单场景、单 Canvas、网格驱动，支持键盘 + 触屏滑动操控，含主菜单 / HUD / 暂停 / 游戏结束四套 UI 面板，最高分用 `localStorage` 持久化。

- 引擎版本：Cocos Creator 3.8.8（**3.x API，非 2.x**）
- 语言：TypeScript
- 设计分辨率：720 × 1280（竖屏）
- 网格：20 × 20，每格 30px，棋盘 600 × 600

## 项目结构

```
SnakeBattle/
├── assets/
│   ├── scenes/
│   │   ├── MainScene.scene          # 唯一场景（顶层 JSON 数组，首元素 cc.SceneAsset）
│   │   └── GameBoard.prefab         # GameBoard 预制体（当前场景内联使用，未通过 prefab 实例化）
│   ├── scripts/                     # 7 个脚本
│   │   ├── GameConfig.ts            # 全局常量：网格/速度/颜色/方向枚举/游戏状态枚举
│   │   ├── GridSystem.ts            # 网格坐标系：gridToWorld / worldToGrid / isValid / randomPos
│   │   ├── SnakeController.ts       # 蛇逻辑：移动/生长/碰撞/方向缓冲
│   │   ├── FoodSpawner.ts           # 食物生成：随机空位生成、吃食检测、补充
│   │   ├── UIManager.ts             # UI 面板：show/hide 四套面板、按钮事件转发
│   │   ├── GameManager.ts           # 主控制器：状态机、输入、分数、模块协调
│   │   └── AudioManager.ts          # 音频：BGM 播放/暂停、音效 OneShot
│   ├── prefabs/
│   │   ├── SnakeBody.prefab         # 蛇身节段预制体（Sprite + UITransform，28×28）
│   │   └── Food.prefab              # 食物预制体（Sprite + UITransform，26×26）
│   ├── audio/                       # bgm.wav / eat.wav / gameover.wav / button_click.wav
│   ├── textures/                    # 纹理资源
│   └── fonts/                       # 字体资源
├── settings/                        # 引擎项目设置
├── profiles/                        # 编辑器配置（已 gitignore）
├── library/ temp/ local/ build/     # 引擎生成目录（已 gitignore，勿手动改）
├── tools/                           # 辅助脚本（如 fix_scene.py）
├── package.json                     # Cocos 项目描述
├── tsconfig.json                    # TS 编译配置
└── .gitignore                       # 排除 library/temp/local/build/node_modules 等
```

## 代码架构

### 模块职责

| 脚本 | 职责 | 挂载节点 |
|------|------|----------|
| **GameManager** | 状态机中枢：监听输入（键盘+触屏）、监听 UI 事件、协调 Snake/Food/UI/Audio | 场景根下 GameManager 节点 |
| **GridSystem** | 纯坐标转换工具：逻辑格子 ↔ 局部坐标 | GameBoard 节点 |
| **SnakeController** | 蛇身逻辑数组 `_body[]`，定时移动，方向缓冲，碰撞检测 | GameManager 节点（与 GameManager 同节点） |
| **FoodSpawner** | 维护 `_foods[]` 食物逻辑坐标，随机生成避开蛇身 | 场景根下独立节点 |
| **UIManager** | 控制四套面板 active 切换，按钮点击通过 `node.emit` 事件转发给 GameManager | Canvas 节点 |
| **AudioManager** | 封装 AudioSource，BGM 循环播放、SFX OneShot | 场景根下独立节点 |

### 数据流

```
玩家输入(键盘/触屏) ─→ GameManager.onKeyDown/onTouchEnd
                              │
                              ▼
                    SnakeController.setDirection(dir)
                              │ (update 定时驱动)
                              ▼
                    SnakeController.move()
                       ├── 撞墙/撞身 → onDeath → GameManager.onSnakeDeath → GAME_OVER
                       └── 移动头部   → onEatFood → GameManager.onFoodEaten
                                                      ├── FoodSpawner.checkEat → 吃到则 grow()+加分+补食
                                                      └── 未吃到则 pop 尾部
                    updateBodyPositions() → gridToWorld → 节点 setPosition
```

UI 事件流：

```
按钮点击 → UIManager.onXxxClick() → this.node.emit('game-start'/'game-pause'/...)
                                        ↓
                          GameManager.setupUIEvents() 监听 → startGame/pauseGame/...
```

### 状态机

`GameState` 四态：`MENU → PLAYING ↔ PAUSED → GAME_OVER → MENU/PLAYING`

`GameManager.setState(state)` 是唯一入口，内部联动 UI 面板显示、蛇暂停、音频播放/停止。

### 坐标系

- **逻辑坐标**：`GridPos { x, y }`，范围 `0~19`，左下角为 (0,0)
- **gridToWorld** 返回以网格中心为原点的**局部坐标**（范围约 -285 ~ +285），因为 `_offsetX = -(gridWidth*cellSize)/2`
- 蛇/食物节点挂在 `SnakeContainer`/`FoodContainer`（GameBoard 子节点）下，GameBoard 挂在 Canvas 下，Canvas 在 (360, 640)
- 因此蛇身世界坐标 ≈ 360±285、640±285，落在 720×1280 屏幕中央

## 开发流程

### 运行游戏

1. 用 Cocos Creator 3.8.8 打开项目（`CocosDashboard → 打开 → 选择 SnakeBattle 目录`）
2. 双击 `assets/scenes/MainScene.scene` 打开场景
3. 点击编辑器顶部 **▶ 预览** 按钮，浏览器中运行
4. 键盘：方向键 / WASD 移动，Space / P 暂停，Enter 开始/重开
5. 触屏：滑动改变方向

### 修改代码后生效

- 修改 `.ts` 脚本 → 编辑器自动编译 → 预览窗口会自动热重载场景
- 修改 `.scene` / `.prefab` 文件 → 需在编辑器中**重新打开场景**或点 Reimport
- 修改 `GameConfig.ts` 常量（速度/颜色/网格大小）→ 全局生效，无需改其他文件

### 调试

- 运行日志：`temp/logs/project.log`，搜索 `[PreviewInEditor]` 查看预览期错误
- 编译产物：`library/{uuid前2位}/{uuid}.json`
- 浏览器控制台（预览时）可直接看 `console.log` 输出

## 场景文件编辑（重要约束）

`MainScene.scene` 是 JSON 数组格式，首元素为 `cc.SceneAsset`，后续每个对象通过 `__id__`（数组下标）互相引用。**外部直接编辑此文件时需极其谨慎。**

### Cocos uuid 压缩算法

场景中脚本/资源引用用**压缩 uuid**（23 字符）：
- 前 5 个 hex 字符保留原文
- 剩余 27 个 hex 字符做**标准 base64**（18 字符）
- 例：`1ccfc7ed-9aa3-4016-8cf4-61035ff7fde7` → `1ccfcftmqNAFoz0YQNf9/3n`

外部修改脚本组件引用时必须正确计算压缩 uuid，否则编辑器无法识别。

### 场景层级（当前正确结构）

```
Scene
  └── Canvas (pos: 360, 640)              ← UI 渲染根节点
      ├── GameBoard (pos: 0, 0)           ← 必须在 Canvas 下！
      │   ├── GridBackground              ← 必须排第一（先渲染，作底层背景）
      │   ├── SnakeContainer              ← 排第二（蛇在背景之上）
      │   └── FoodContainer               ← 排第三（食物在最上层）
      ├── HUD                             ← 游戏中信息栏
      ├── MenuPanel                       ← 主菜单
      ├── GameOverPanel                   ← 结束面板
      └── PausePanel                      ← 暂停面板
  ├── Camera                              ← 逻辑节点，不在 Canvas 下
  ├── GameManager (挂 GameManager + SnakeController)
  ├── FoodSpawner
  └── AudioManager
```

## 关键技术陷阱（踩坑记录）

### 1. UI 组件必须在 Canvas 子树中

Cocos 3.x 的 UI 渲染管线从 **Canvas 节点**向下遍历收集可渲染 UI 组件（Sprite/Label 等）。节点不在 Canvas 后代中 → 即使 `active=true`、`layer=UI_2D`、坐标在屏幕内、Camera visibility 包含 UI_2D，**也不会被渲染**。这是"日志一切正常但看不到东西"的典型原因。

### 2. 子节点渲染顺序 = 数组顺序

同一父节点下，子节点按 `_children` 数组顺序渲染，**后渲染的覆盖先渲染的**。背景节点必须排在数组前面（先渲染），否则会盖住蛇和食物。

### 3. 3.x API，禁用 2.x API

| 2.x（禁用） | 3.x（正确） |
|-------------|-------------|
| `node.setActive(bool)` | `node.active = bool` |
| `cc.find('path')` | `find('path')`（从 `'cc'` 导入） |
| `node.runAction(action)` | `tween(node).to(...).start()` |
| `setPosition(Vec3)` | 仍可用（有重载），也可用 `node.position` |

用 `setActive` 会导致 `TypeError: xxx.setActive is not a function`，且异常在 `onLoad` 中抛出会中断后续所有逻辑。

### 4. @property 必须显式类型

```typescript
// 正确：数字类型必须显式声明
@property({ type: CCInteger })
gridWidth: number = 20;

// 错误：某些版本下不会在属性检查器中暴露
@property
gridWidth: number = 20;
```

### 5. layer 常量

- `UI_2D = 33554432`（`1 << 25`）
- `DEFAULT = 1073741824`（`1 << 30`）
- UI 节点（蛇/食物/面板）必须用 `UI_2D`，Camera 的 `visibility` 必须包含 `UI_2D`

### 6. 场景重载与 onDestroy

脚本修改触发热重载 → `Director.runSceneImmediate` → 旧组件 `onDestroy` 时，其他组件的 `node` 可能已被置空。`onDestroy` 中解绑事件前必须判空：

```typescript
if (this.uiManager && this.uiManager.node) {
    this.uiManager.node.off('game-start', this.startGame, this);
}
```

### 7. Sprite 需要 SpriteFrame 才能渲染颜色

`Sprite.color` 只是 tint 颜色，前提是 Sprite 已绑定 `SpriteFrame`（本项目用 `default_sprite_splash`，白色全图，tint 后显示纯色方块）。

## 常见开发任务

### 调整游戏速度

改 `GameConfig.ts`：
```typescript
export const INITIAL_SPEED = 0.18;   // 初始移动间隔（秒），越小越快
export const MIN_SPEED = 0.08;       // 最快限制
export const SPEED_INCREMENT = 0.005; // 每吃一个食物加速量
```

### 改变蛇/食物颜色

改 `GameConfig.ts`：
```typescript
export const SNAKE_HEAD_COLOR = '#4CAF50';  // 蛇头深绿
export const SNAKE_BODY_COLOR = '#81C784';  // 蛇身浅绿
export const FOOD_COLOR = '#FF5252';        // 食物红
export const GRID_BG_COLOR = '#1A1A2E';     // 棋盘深蓝
```

### 增加食物数量

改 `GameConfig.ts`：`export const FOOD_COUNT = 1;` → 改为 3 等。

### 修改网格大小

改 `GameConfig.ts` 的 `GRID_WIDTH` / `GRID_HEIGHT` / `CELL_SIZE`，同时需在编辑器中调整 `GridBackground` 的尺寸。

## Git

- 远程仓库：`git@github.com:malinghan/snake-battle.git`
- 分支：`main`
- `.gitignore` 已排除 `library/`、`temp/`、`local/`、`build/`、`node_modules/`、`profiles/` 等生成目录
- 首次推送：
  ```bash
  git add .
  git commit -m "init: SnakeBattle project"
  git branch -M main
  git push -u origin main
  ```
