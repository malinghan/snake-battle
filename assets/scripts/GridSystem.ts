/**
 * GridSystem.ts
 * 网格坐标系 —— 将逻辑坐标 (gridX, gridY) 与屏幕像素坐标互相转换
 * 在 Cocos Creator 中作为组件挂载到场景节点上
 *
 * 注意：Cocos Creator 3.x 中数字类型属性必须用 @property(CCInteger) 或 @property(CCFloat)
 * 显式声明类型，单纯写 @property 在某些版本下不会在属性检查器中暴露
 */

import { _decorator, Component, Node, Vec3, CCInteger } from 'cc';
import { GRID_WIDTH, GRID_HEIGHT, CELL_SIZE } from './GameConfig';

const { ccclass, property } = _decorator;

// 网格坐标类型
export interface GridPos {
    x: number;
    y: number;
}

@ccclass('GridSystem')
export class GridSystem extends Component {
    @property({ type: CCInteger, tooltip: '横向格子数' })
    gridWidth: number = GRID_WIDTH;

    @property({ type: CCInteger, tooltip: '纵向格子数' })
    gridHeight: number = GRID_HEIGHT;

    @property({ type: CCInteger, tooltip: '每格像素大小' })
    cellSize: number = CELL_SIZE;

    // 原点偏移：将网格中心对齐到节点原点
    private _offsetX: number = 0;
    private _offsetY: number = 0;

    onLoad() {
        // 计算偏移量，使网格居中
        this._offsetX = -(this.gridWidth * this.cellSize) / 2;
        this._offsetY = -(this.gridHeight * this.cellSize) / 2;
    }

    /**
     * 网格坐标 → 世界坐标（用于放置蛇身节点）
     */
    gridToWorld(gridX: number, gridY: number): Vec3 {
        const worldX = this._offsetX + gridX * this.cellSize + this.cellSize / 2;
        const worldY = this._offsetY + gridY * this.cellSize + this.cellSize / 2;
        return new Vec3(worldX, worldY, 0);
    }

    /**
     * 世界坐标 → 网格坐标（用于触屏点击转换为格子）
     */
    worldToGrid(worldX: number, worldY: number): GridPos {
        const gridX = Math.floor((worldX - this._offsetX) / this.cellSize);
        const gridY = Math.floor((worldY - this._offsetY) / this.cellSize);
        return { x: gridX, y: gridY };
    }

    /**
     * 检查坐标是否在网格范围内
     */
    isValid(gridX: number, gridY: number): boolean {
        return gridX >= 0 && gridX < this.gridWidth &&
               gridY >= 0 && gridY < this.gridHeight;
    }

    /**
     * 随机生成一个网格内坐标
     */
    randomPos(): GridPos {
        return {
            x: Math.floor(Math.random() * this.gridWidth),
            y: Math.floor(Math.random() * this.gridHeight),
        };
    }

    get totalWidth(): number {
        return this.gridWidth * this.cellSize;
    }

    get totalHeight(): number {
        return this.gridHeight * this.cellSize;
    }
}
