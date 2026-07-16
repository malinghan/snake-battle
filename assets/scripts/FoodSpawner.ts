/**
 * FoodSpawner.ts
 * 食物生成器：在网格空位随机生成食物
 */

import { _decorator, Component, Node, Vec3, instantiate, Prefab, Sprite, UITransform, Color } from 'cc';
import { GridSystem, GridPos } from './GridSystem';
import { SnakeController } from './SnakeController';
import { FOOD_COUNT, FOOD_COLOR, CELL_SIZE } from './GameConfig';

const { ccclass, property } = _decorator;

@ccclass('FoodSpawner')
export class FoodSpawner extends Component {
    @property(GridSystem)
    gridSystem: GridSystem | null = null;

    @property(SnakeController)
    snakeController: SnakeController | null = null;

    @property(Prefab)
    foodPrefab: Prefab | null = null;

    @property(Node)
    foodContainer: Node | null = null;

    // 当前所有食物的逻辑坐标
    private _foods: GridPos[] = [];
    // 食物节点引用
    private _foodNodes: Node[] = [];

    /**
     * 生成指定数量的食物
     */
    spawnAll() {
        this.clearAll();
        for (let i = 0; i < FOOD_COUNT; i++) {
            this.spawnOne();
        }
    }

    /**
     * 生成一个食物（避开蛇身和已有食物）
     */
    spawnOne() {
        if (!this.gridSystem || !this.snakeController) return;

        let pos: GridPos;
        let attempts = 0;
        const maxAttempts = 200;

        do {
            pos = this.gridSystem.randomPos();
            attempts++;
            // 检查是否与蛇身或已有食物重叠
            const onSnake = this.snakeController.occupies(pos.x, pos.y);
            const onFood = this._foods.some(f => f.x === pos.x && f.y === pos.y);
            if (!onSnake && !onFood) break;
        } while (attempts < maxAttempts);

        this._foods.push(pos);

        // 创建食物节点
        if (this.foodPrefab && this.foodContainer) {
            const node = instantiate(this.foodPrefab);
            node.setParent(this.foodContainer);

            const sprite = node.getComponent(Sprite);
            if (sprite) {
                sprite.color = new Color().fromHEX(FOOD_COLOR);
            }

            const transform = node.getComponent(UITransform);
            if (transform) {
                transform.setContentSize(CELL_SIZE - 4, CELL_SIZE - 4);
            }

            const worldPos = this.gridSystem.gridToWorld(pos.x, pos.y);
            node.setPosition(worldPos);
            this._foodNodes.push(node);
        }
    }

    /**
     * 检查蛇头是否吃到食物，如果吃到则移除该食物并返回 true
     */
    checkEat(headX: number, headY: number): boolean {
        for (let i = 0; i < this._foods.length; i++) {
            if (this._foods[i].x === headX && this._foods[i].y === headY) {
                // 移除被吃的食物
                this._foods.splice(i, 1);
                const node = this._foodNodes.splice(i, 1)[0];
                if (node) node.destroy();
                // 补充新食物
                this.spawnOne();
                return true;
            }
        }
        return false;
    }

    /**
     * 清除所有食物
     */
    clearAll() {
        this._foodNodes.forEach(node => node.destroy());
        this._foodNodes = [];
        this._foods = [];
    }
}
