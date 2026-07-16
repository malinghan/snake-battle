/**
 * GameConfig.ts
 * 全局游戏配置常量，集中管理所有可调参数
 */

// 网格配置
export const GRID_WIDTH = 20;       // 横向格子数
export const GRID_HEIGHT = 20;      // 纵向格子数
export const CELL_SIZE = 30;        // 每格像素大小（场景中节点的实际尺寸）

// 蛇的配置
export const INITIAL_SPEED = 0.18;  // 初始移动间隔（秒），越小越快
export const MIN_SPEED = 0.08;      // 最快速度限制
export const SPEED_INCREMENT = 0.005; // 每吃一个食物加速量
export const INITIAL_LENGTH = 3;    // 蛇的初始长度

// 方向枚举
export enum Direction {
    UP = 'up',
    DOWN = 'down',
    LEFT = 'left',
    RIGHT = 'right',
}

// 方向向量
export const DirectionVector: Record<Direction, { x: number; y: number }> = {
    [Direction.UP]:    { x: 0,  y: 1  },
    [Direction.DOWN]:  { x: 0,  y: -1 },
    [Direction.LEFT]:  { x: -1, y: 0  },
    [Direction.RIGHT]: { x: 1,  y: 0  },
};

// 相反方向（防止蛇直接掉头）
export const OppositeDirection: Record<Direction, Direction> = {
    [Direction.UP]:    Direction.DOWN,
    [Direction.DOWN]:  Direction.UP,
    [Direction.LEFT]:  Direction.RIGHT,
    [Direction.RIGHT]: Direction.LEFT,
};

// 食物配置
export const FOOD_COUNT = 1;        // 同时存在的食物数量
export const FOOD_SCORE = 10;       // 每个食物的分数

// 颜色配置
export const SNAKE_HEAD_COLOR = '#4CAF50';
export const SNAKE_BODY_COLOR = '#81C784';
export const FOOD_COLOR = '#FF5252';
export const GRID_BG_COLOR = '#1A1A2E';
export const GRID_LINE_COLOR = '#16213E';

// 游戏状态枚举
export enum GameState {
    MENU = 'menu',
    PLAYING = 'playing',
    PAUSED = 'paused',
    GAME_OVER = 'game_over',
}
