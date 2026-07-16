/**
 * UIManager.ts
 * UI 管理器：控制 HUD、主菜单、暂停界面、游戏结束界面的显示与隐藏
 */

import { _decorator, Component, Node, Label, Button } from 'cc';
import { GameState } from './GameConfig';

const { ccclass, property } = _decorator;

@ccclass('UIManager')
export class UIManager extends Component {
    @property(Node)
    menuPanel: Node | null = null;

    @property(Node)
    hudPanel: Node | null = null;

    @property(Node)
    pausePanel: Node | null = null;

    @property(Node)
    gameOverPanel: Node | null = null;

    @property(Label)
    scoreLabel: Label | null = null;

    @property(Label)
    highScoreLabel: Label | null = null;

    @property(Label)
    finalScoreLabel: Label | null = null;

    @property(Label)
    finalHighScoreLabel: Label | null = null;

    @property(Button)
    startButton: Button | null = null;

    @property(Button)
    resumeButton: Button | null = null;

    @property(Button)
    restartButton: Button | null = null;

    @property(Button)
    menuButton: Button | null = null;

    @property(Button)
    pauseMenuButton: Button | null = null;

    @property(Button)
    pauseButton: Button | null = null;

    onLoad() {
        this.resolveMissingRefs();
        // 立即隐藏所有面板，防止闪烁
        this.hideAll();
        this.showMenu();

        // 按钮事件
        if (this.startButton) {
            this.startButton.node.on(Button.EventType.CLICK, this.onStartClick, this);
        }
        if (this.resumeButton) {
            this.resumeButton.node.on(Button.EventType.CLICK, this.onResumeClick, this);
        }
        if (this.restartButton) {
            this.restartButton.node.on(Button.EventType.CLICK, this.onRestartClick, this);
        }
        if (this.menuButton) {
            this.menuButton.node.on(Button.EventType.CLICK, this.onMenuClick, this);
        }
        if (this.pauseMenuButton) {
            this.pauseMenuButton.node.on(Button.EventType.CLICK, this.onMenuClick, this);
        }
        if (this.pauseButton) {
            this.pauseButton.node.on(Button.EventType.CLICK, this.onPauseClick, this);
        }
    }

    start() {
        // 再次确保只有菜单显示（防止编辑器里面板都是激活状态）
        this.resolveMissingRefs();
        this.hideAll();
        this.showMenu();
    }

    private resolveMissingRefs() {
        // 如果属性未绑定，按名字兜底查找，避免面板同时显示
        if (!this.menuPanel) this.menuPanel = this.node.getChildByName('MenuPanel');
        if (!this.hudPanel) this.hudPanel = this.node.getChildByName('HUD');
        if (!this.pausePanel) this.pausePanel = this.node.getChildByName('PausePanel');
        if (!this.gameOverPanel) this.gameOverPanel = this.node.getChildByName('GameOverPanel');
    }

    private hideAll() {
        if (this.menuPanel) this.menuPanel.active = false;
        if (this.hudPanel) this.hudPanel.active = false;
        if (this.pausePanel) this.pausePanel.active = false;
        if (this.gameOverPanel) this.gameOverPanel.active = false;
    }

    showMenu() {
        this.hideAll();
        if (this.menuPanel) this.menuPanel.active = true;
    }

    showHUD() {
        this.hideAll();
        if (this.hudPanel) this.hudPanel.active = true;
    }

    showPause() {
        this.hideAll();
        if (this.pausePanel) this.pausePanel.active = true;
        if (this.hudPanel) this.hudPanel.active = true;
    }

    showGameOver(score: number, highScore: number) {
        this.hideAll();
        if (this.gameOverPanel) this.gameOverPanel.active = true;

        if (this.finalScoreLabel) {
            this.finalScoreLabel.string = `本次得分: ${score}`;
        }
        if (this.finalHighScoreLabel) {
            const isNew = score >= highScore && score > 0;
            this.finalHighScoreLabel.string = `最高纪录: ${highScore}${isNew ? ' (新纪录!)' : ''}`;
        }
    }

    updateScore(score: number) {
        if (this.scoreLabel) {
            this.scoreLabel.string = `得分: ${score}`;
        }
    }

    updateHighScore(highScore: number) {
        if (this.highScoreLabel) {
            this.highScoreLabel.string = `最高: ${highScore}`;
        }
    }

    // 按钮回调 —— 需要由外部（GameManager）注入实际逻辑
    onStartClick() {
        // 通过事件系统通知 GameManager
        this.node.emit('game-start');
    }

    onResumeClick() {
        this.node.emit('game-resume');
    }

    onRestartClick() {
        this.node.emit('game-restart');
    }

    onMenuClick() {
        this.node.emit('game-menu');
    }

    onPauseClick() {
        this.node.emit('game-pause');
    }
}
