/**
 * AudioManager.ts
 * 音频管理器：BGM 播放/暂停/停止，音效播放
 */

import { _decorator, Component, AudioSource, AudioClip } from 'cc';

const { ccclass, property } = _decorator;

@ccclass('AudioManager')
export class AudioManager extends Component {
    @property(AudioSource)
    bgmSource: AudioSource | null = null;

    @property(AudioSource)
    sfxSource: AudioSource | null = null;

    @property(AudioClip)
    eatClip: AudioClip | null = null;

    @property(AudioClip)
    gameOverClip: AudioClip | null = null;

    @property(AudioClip)
    buttonClickClip: AudioClip | null = null;

    private _bgmVolume: number = 0.5;
    private _sfxVolume: number = 0.8;

    playBGM() {
        if (this.bgmSource && !this.bgmSource.playing) {
            this.bgmSource.volume = this._bgmVolume;
            this.bgmSource.loop = true;
            this.bgmSource.play();
        }
    }

    pauseBGM() {
        this.bgmSource?.pause();
    }

    stopBGM() {
        this.bgmSource?.stop();
    }

    resumeBGM() {
        if (this.bgmSource && !this.bgmSource.playing) {
            this.bgmSource.play();
        }
    }

    playEat() {
        if (this.sfxSource && this.eatClip) {
            this.sfxSource.playOneShot(this.eatClip, this._sfxVolume);
        }
    }

    playGameOver() {
        if (this.sfxSource && this.gameOverClip) {
            this.sfxSource.playOneShot(this.gameOverClip, this._sfxVolume);
        }
    }

    playButtonClick() {
        if (this.sfxSource && this.buttonClickClip) {
            this.sfxSource.playOneShot(this.buttonClickClip, this._sfxVolume);
        }
    }

    setBGMVolume(volume: number) {
        this._bgmVolume = Math.max(0, Math.min(1, volume));
        if (this.bgmSource) {
            this.bgmSource.volume = this._bgmVolume;
        }
    }

    setSFXVolume(volume: number) {
        this._sfxVolume = Math.max(0, Math.min(1, volume));
    }
}
