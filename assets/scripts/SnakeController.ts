/**
 * SnakeController.ts
 * 蛇的核心逻辑：移动、生长、碰撞检测
 * 使用逻辑坐标数组管理蛇身，通过定时器驱动移动
 */

import { _decorator, Component, Node, Vec3, instantiate, Prefab, Sprite, UITransform, Color } from 'cc';
import { GridSystem, GridPos } from './GridSystem';
import { Direction, DirectionVector, OppositeDirection, INITIAL_LENGTH, INITIAL_SPEED, MIN_SPEED, SPEED_INCREMENT, SNAKE_HEAD_COLOR, SNAKE_BODY_COLOR, CELL_SIZE } from './GameConfig';

const { ccclass, property } = _decorator;

@ccclass('SnakeController')
export class SnakeController extends Component {
    @property(GridSystem)
    gridSystem: GridSystem | null = null;

    @property(Prefab)
    bodySegmentPrefab: Prefab | null = null;

    @property(Node)
    snakeContainer: Node | null = null;

    // 蛇身逻辑坐标数组，第 0 个是蛇头
    private _body: GridPos[] = [];
    // 当前方向
    private _currentDir: Direction = Direction.RIGHT;
    // 下一步方向（缓冲输入，防止一帧内多次转向）
    private _nextDir: Direction = Direction.RIGHT;
    // 移动计时器
    private _moveTimer: number = 0;
    // 当前移动间隔
    private _moveInterval: number = INITIAL_SPEED;
    // 蛇身节点引用
    private _bodyNodes: Node[] = [];
    // 是否暂停
    private _isPaused: boolean = false;

    // 回调
    public onEatFood: (() => void) | null = null;
    public onDeath: (() => void) | null = null;

    onLoad() {
        // 不在这里调用 initSnake，等 GridSystem.onLoad 先执行完毕
    }

    start() {
        this.initSnake();
    }

    /**
     * 初始化蛇：放置在网格中央，初始长度 3
     */
    initSnake() {
        this._body = [];
        this._bodyNodes.forEach(node => node.destroy());
        this._bodyNodes = [];

        this._currentDir = Direction.RIGHT;
        this._nextDir = Direction.RIGHT;
        this._moveInterval = INITIAL_SPEED;
        this._moveTimer = 0;

        const centerX = Math.floor((this.gridSystem?.gridWidth ?? 20) / 2);
        const centerY = Math.floor((this.gridSystem?.gridHeight ?? 20) / 2);

        for (let i = 0; i < INITIAL_LENGTH; i++) {
            this._body.push({ x: centerX - i, y: centerY });
            this.createBodyNode(i === 0);
        }

        this.updateBodyPositions();
    }

    /**
     * 创建蛇身节点（头/身用不同颜色区分）
     */
    private createBodyNode(isHead: boolean) {
        if (!this.bodySegmentPrefab || !this.snakeContainer) return;

        const node = instantiate(this.bodySegmentPrefab);
        node.setParent(this.snakeContainer);

        const sprite = node.getComponent(Sprite);
        if (sprite) {
            const color = isHead ? new Color().fromHEX(SNAKE_HEAD_COLOR)
                                  : new Color().fromHEX(SNAKE_BODY_COLOR);
            sprite.color = color;
        }

        const transform = node.getComponent(UITransform);
        if (transform) {
            transform.setContentSize(CELL_SIZE - 2, CELL_SIZE - 2);
        }

        this._bodyNodes.push(node);
    }

    update(deltaTime: number) {
        if (this._isPaused) return;

        this._moveTimer += deltaTime;
        if (this._moveTimer >= this._moveInterval) {
            this._moveTimer = 0;
            this.move();
        }
    }

    /**
     * 蛇移动一步的核心逻辑
     */
    private move() {
        // 应用缓冲方向
        this._currentDir = this._nextDir;

        const vector = DirectionVector[this._currentDir];
        const head = this._body[0];
        const newHead: GridPos = {
            x: head.x + vector.x,
            y: head.y + vector.y,
        };

        // 碰撞检测：撞墙
        if (!this.gridSystem?.isValid(newHead.x, newHead.y)) {
            this.onDeath?.();
            return;
        }

        // 碰撞检测：撞自身（排除尾巴，因为尾巴会移走）
        for (let i = 0; i < this._body.length - 1; i++) {
            if (this._body[i].x === newHead.x && this._body[i].y === newHead.y) {
                this.onDeath?.();
                return;
            }
        }

        // 移动：在头部添加新格子
        this._body.unshift(newHead);

        // 通知外部检查是否吃到食物
        // GameManager.onFoodEaten 会调用 foodSpawner.checkEat，
        // 如果吃到则调用 grow() 设置 _shouldGrow = true
        this.onEatFood?.();

        // 根据是否吃到食物决定是否移除尾部
        if (!this._shouldGrow) {
            this._body.pop();
        } else {
            this._shouldGrow = false;
            this.createBodyNode(false);
        }

        this.updateBodyPositions();
    }

    private _shouldGrow: boolean = false;

    /**
     * 外部调用：蛇吃到食物，下次移动时生长
     */
    grow() {
        this._shouldGrow = true;
        // 加速
        this._moveInterval = Math.max(MIN_SPEED, this._moveInterval - SPEED_INCREMENT);
    }

    /**
     * 更新所有蛇身节点的屏幕位置
     */
    private updateBodyPositions() {
        for (let i = 0; i < this._body.length; i++) {
            const pos = this.gridSystem!.gridToWorld(this._body[i].x, this._body[i].y);
            if (this._bodyNodes[i]) {
                this._bodyNodes[i].setPosition(pos);
            }
        }
    }

    /**
     * 设置方向（带防掉头检查）
     */
    setDirection(dir: Direction) {
        if (dir === OppositeDirection[this._currentDir]) return;
        this._nextDir = dir;
    }

    /**
     * 获取蛇头位置
     */
    getHeadPos(): GridPos {
        return this._body[0];
    }

    /**
     * 检查某个格子是否被蛇身占据
     */
    occupies(gridX: number, gridY: number): boolean {
        return this._body.some(seg => seg.x === gridX && seg.y === gridY);
    }

    setPaused(paused: boolean) {
        this._isPaused = paused;
    }

    getCurrentLength(): number {
        return this._body.length;
    }
}
