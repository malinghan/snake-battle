/**
 * GameManager.ts
 * 游戏主控制器：协调各模块，管理游戏状态和分数
 */

import { _decorator, Component, Node, input, Input, EventKeyboard, KeyCode, EventTouch, Vec2 } from 'cc';
import { GridSystem } from './GridSystem';
import { SnakeController } from './SnakeController';
import { FoodSpawner } from './FoodSpawner';
import { UIManager } from './UIManager';
import { AudioManager } from './AudioManager';
import { GameState, Direction, FOOD_SCORE } from './GameConfig';

const { ccclass, property } = _decorator;

@ccclass('GameManager')
export class GameManager extends Component {
    @property(GridSystem)
    gridSystem: GridSystem | null = null;

    @property(SnakeController)
    snakeController: SnakeController | null = null;

    @property(FoodSpawner)
    foodSpawner: FoodSpawner | null = null;

    @property(UIManager)
    uiManager: UIManager | null = null;

    @property(AudioManager)
    audioManager: AudioManager | null = null;

    private _state: GameState = GameState.MENU;
    private _score: number = 0;
    private _highScore: number = 0;

    onLoad() {
        // 从本地存储读取最高分
        const saved = localStorage.getItem('snake_high_score');
        this._highScore = saved ? parseInt(saved) : 0;

        // 注册事件
        this.setupInput();
        this.setupCallbacks();
        this.setupUIEvents();

        // 初始状态
        this.setState(GameState.MENU);
    }

    /**
     * 设置输入监听：键盘 + 触屏滑动
     */
    private setupInput() {
        input.on(Input.EventType.KEY_DOWN, this.onKeyDown, this);
        input.on(Input.EventType.TOUCH_START, this.onTouchStart, this);
        input.on(Input.EventType.TOUCH_END, this.onTouchEnd, this);
    }

    private _touchStartPos: Vec2 = new Vec2();

    private onTouchStart(event: EventTouch) {
        this._touchStartPos.set(event.getLocation());
    }

    private onTouchEnd(event: EventTouch) {
        if (this._state !== GameState.PLAYING) return;

        const endPos = event.getLocation();
        const dx = endPos.x - this._touchStartPos.x;
        const dy = endPos.y - this._touchStartPos.y;

        // 滑动距离阈值
        const threshold = 30;
        if (Math.abs(dx) < threshold && Math.abs(dy) < threshold) return;

        // 判断滑动方向
        if (Math.abs(dx) > Math.abs(dy)) {
            this.snakeController?.setDirection(dx > 0 ? Direction.RIGHT : Direction.LEFT);
        } else {
            this.snakeController?.setDirection(dy > 0 ? Direction.UP : Direction.DOWN);
        }
    }

    private onKeyDown(event: EventKeyboard) {
        switch (event.keyCode) {
            case KeyCode.ARROW_UP:
            case KeyCode.KEY_W:
                if (this._state === GameState.PLAYING) {
                    this.snakeController?.setDirection(Direction.UP);
                }
                break;
            case KeyCode.ARROW_DOWN:
            case KeyCode.KEY_S:
                if (this._state === GameState.PLAYING) {
                    this.snakeController?.setDirection(Direction.DOWN);
                }
                break;
            case KeyCode.ARROW_LEFT:
            case KeyCode.KEY_A:
                if (this._state === GameState.PLAYING) {
                    this.snakeController?.setDirection(Direction.LEFT);
                }
                break;
            case KeyCode.ARROW_RIGHT:
            case KeyCode.KEY_D:
                if (this._state === GameState.PLAYING) {
                    this.snakeController?.setDirection(Direction.RIGHT);
                }
                break;
            case KeyCode.SPACE:
            case KeyCode.KEY_P:
                if (this._state === GameState.PLAYING) {
                    this.pauseGame();
                } else if (this._state === GameState.PAUSED) {
                    this.resumeGame();
                }
                break;
            case KeyCode.ENTER:
                if (this._state === GameState.MENU || this._state === GameState.GAME_OVER) {
                    this.startGame();
                }
                break;
        }
    }

    /**
     * 监听 UIManager 的 UI 事件
     */
    private setupUIEvents() {
        if (!this.uiManager) return;

        this.uiManager.node.on('game-start', this.startGame, this);
        this.uiManager.node.on('game-resume', this.resumeGame, this);
        this.uiManager.node.on('game-restart', this.startGame, this);
        this.uiManager.node.on('game-pause', this.pauseGame, this);
        this.uiManager.node.on('game-menu', this.backToMenu, this);
    }

    /**
     * 设置蛇和食物的回调
     */
    private setupCallbacks() {
        if (this.snakeController) {
            this.snakeController.onEatFood = () => {
                this.onFoodEaten();
            };
            this.snakeController.onDeath = () => {
                this.onSnakeDeath();
            };
        }
    }

    /**
     * 切换游戏状态
     */
    setState(state: GameState) {
        this._state = state;

        switch (state) {
            case GameState.MENU:
                this.uiManager?.showMenu();
                this.snakeController?.setPaused(true);
                break;
            case GameState.PLAYING:
                this.uiManager?.showHUD();
                this.snakeController?.setPaused(false);
                this.audioManager?.playBGM();
                break;
            case GameState.PAUSED:
                this.uiManager?.showPause();
                this.snakeController?.setPaused(true);
                this.audioManager?.pauseBGM();
                break;
            case GameState.GAME_OVER:
                this.uiManager?.showGameOver(this._score, this._highScore);
                this.snakeController?.setPaused(true);
                this.audioManager?.stopBGM();
                this.audioManager?.playGameOver();
                break;
        }
    }

    /**
     * 开始游戏
     */
    startGame() {
        this._score = 0;
        this.snakeController?.initSnake();
        this.foodSpawner?.spawnAll();
        this.uiManager?.updateScore(this._score);
        this.uiManager?.updateHighScore(this._highScore);
        this.setState(GameState.PLAYING);
    }

    /**
     * 暂停游戏
     */
    pauseGame() {
        if (this._state === GameState.PAUSED) return;
        this.setState(GameState.PAUSED);
    }

    /**
     * 恢复游戏
     */
    resumeGame() {
        if (this._state === GameState.PLAYING) return;
        this.setState(GameState.PLAYING);
    }

    /**
     * 回到主菜单
     */
    backToMenu() {
        this.setState(GameState.MENU);
    }

    /**
     * 蛇吃到食物
     */
    private onFoodEaten() {
        // 在 SnakeController.move() 之后检查
        const head = this.snakeController?.getHeadPos();
        if (head && this.foodSpawner?.checkEat(head.x, head.y)) {
            this._score += FOOD_SCORE;
            this.snakeController?.grow();
            this.uiManager?.updateScore(this._score);
            this.audioManager?.playEat();
        }
    }

    /**
     * 蛇死亡
     */
    private onSnakeDeath() {
        // 更新最高分
        if (this._score > this._highScore) {
            this._highScore = this._score;
            localStorage.setItem('snake_high_score', this._highScore.toString());
        }
        this.setState(GameState.GAME_OVER);
    }

    /**
     * 获取当前分数
     */
    getScore(): number {
        return this._score;
    }

    /**
     * 获取最高分
     */
    getHighScore(): number {
        return this._highScore;
    }

    onDestroy() {
        input.off(Input.EventType.KEY_DOWN, this.onKeyDown, this);
        input.off(Input.EventType.TOUCH_START, this.onTouchStart, this);
        input.off(Input.EventType.TOUCH_END, this.onTouchEnd, this);

        // 场景重载时 UIManager 可能已被销毁，node 变 null，需判空
        if (this.uiManager && this.uiManager.node) {
            this.uiManager.node.off('game-start', this.startGame, this);
            this.uiManager.node.off('game-resume', this.resumeGame, this);
            this.uiManager.node.off('game-restart', this.startGame, this);
            this.uiManager.node.off('game-pause', this.pauseGame, this);
            this.uiManager.node.off('game-menu', this.backToMenu, this);
        }
    }
}
