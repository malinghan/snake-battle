#!/usr/bin/env python3
"""
generate_scene.py
生成一个完整的 MainScene.scene，包含贪吃蛇大作战的所有节点、
组件和属性绑定。直接覆盖到 assets/scenes/MainScene.scene 即可。
"""
import json, os, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCENE_PATH = PROJECT_ROOT / 'assets/scenes/MainScene.scene'

# 资源 UUID（从 .meta 文件读取）
UUIDS = {
    'GameBoard.prefab':      '5fa2b800-db9b-4abe-a689-a322f2e1967e',
    'SnakeBody.prefab':      '6efce8aa-aa3f-488b-9a2d-3c25e907bf5f',
    'Food.prefab':           'e47b70e3-718e-420a-ba57-f487bfc414d4',
    'GameManager.ts':        '1ccfc7ed-9aa3-4016-8cf4-61035ff7fde7',
    'SnakeController.ts':    '23fd39e6-54b5-4d70-8021-ed9aa1982f14',
    'FoodSpawner.ts':        'ca8e46e0-f18d-43ad-b307-35ea4fb45eb3',
    'GridSystem.ts':         '9efdafc8-663d-4aa0-b0fa-860cb655ac58',
    'UIManager.ts':          '55dca6df-d847-46eb-a03e-0e1d4fd816bd',
    'AudioManager.ts':       '90ed09e6-9aac-4c8c-9a9f-f86196ac0408',
    'bgm.wav':               '67a2df86-94cf-484e-98c8-32fddfc7a8fa',
    'eat.wav':               '7d93feb7-3c8d-4ff7-8001-cbc303649dc0',
    'gameover.wav':          '113737b3-bae9-4f1f-8aff-cfebd60668ec',
    'button_click.wav':      '6436e7a9-a11e-49cc-8ca0-1094ba97ae41',
    'default_sprite':        '7d8f9b89-4fd1-4c9f-a3ab-38ec7cded7ca@f9941',
}

class SceneBuilder:
    def __init__(self):
        self.objects = []

    def add(self, obj):
        obj['__id__'] = len(self.objects)
        self.objects.append(obj)
        return obj['__id__']

    def ref(self, idx):
        return {'__id__': idx}

    def to_json(self):
        return json.dumps(self.objects, indent=2, ensure_ascii=False)


def build_scene():
    b = SceneBuilder()

    # SceneAsset
    scene_asset = b.add({
        '__type__': 'cc.SceneAsset',
        '_name': 'MainScene',
        '_objFlags': 0,
        '_native': '',
        'scene': b.ref(1)
    })

    # Scene
    scene = b.add({
        '__type__': 'cc.Scene',
        '_name': 'scene-2d',
        '_objFlags': 0,
        '_parent': None,
        '_children': [],
        '_active': True,
        '_components': [],
        '_prefab': None,
        'autoReleaseAssets': False,
        '_globals': b.ref(2),
        '_id': '81406645-c85e-4185-a547-03a8077f1307'
    })
    scene_idx = scene

    # SceneGlobals
    globals_idx = b.add({
        '__type__': 'cc.SceneGlobals',
        'ambient': b.ref(3),
        'shadows': b.ref(4),
        '_skybox': b.ref(5),
        'fog': b.ref(6),
        'octree': b.ref(7),
        'skin': b.ref(8),
    })

    # AmbientInfo
    b.add({
        '__type__': 'cc.AmbientInfo',
        '_skyColorHDR': {'__type__': 'cc.Vec4', 'x': 0, 'y': 0, 'z': 0, 'w': 0.520833125},
        '_skyColor': {'__type__': 'cc.Vec4', 'x': 0, 'y': 0, 'z': 0, 'w': 0.520833125},
        '_skyIllumHDR': 20000,
        '_skyIllum': 20000,
        '_groundAlbedoHDR': {'__type__': 'cc.Vec4', 'x': 0, 'y': 0, 'z': 0, 'w': 0},
        '_groundAlbedo': {'__type__': 'cc.Vec4', 'x': 0, 'y': 0, 'z': 0, 'w': 0},
        '_skyColorLDR': {'__type__': 'cc.Vec4', 'x': 0.2, 'y': 0.5, 'z': 0.8, 'w': 1},
        '_skyIllumLDR': 20000,
        '_groundAlbedoLDR': {'__type__': 'cc.Vec4', 'x': 0.2, 'y': 0.2, 'z': 0.2, 'w': 1},
    })

    # ShadowsInfo
    b.add({
        '__type__': 'cc.ShadowsInfo',
        '_enabled': False,
        '_type': 0,
        '_normal': {'__type__': 'cc.Vec3', 'x': 0, 'y': 1, 'z': 0},
        '_distance': 0,
        '_shadowColor': {'__type__': 'cc.Color', 'r': 76, 'g': 76, 'b': 76, 'a': 255},
        '_maxReceived': 4,
        '_size': {'__type__': 'cc.Vec2', 'x': 512, 'y': 512},
    })

    # SkyboxInfo
    b.add({
        '__type__': 'cc.SkyboxInfo',
        '_envLightingType': 0,
        '_envmapHDR': None,
        '_envmap': None,
        '_envmapLDR': None,
        '_diffuseMapHDR': None,
        '_diffuseMapLDR': None,
        '_enabled': False,
        '_useHDR': True,
    })

    # FogInfo
    b.add({
        '__type__': 'cc.FogInfo',
        '_type': 0,
        '_fogColor': {'__type__': 'cc.Color', 'r': 200, 'g': 200, 'b': 200, 'a': 255},
        '_enabled': False,
        '_fogDensity': 0.3,
        '_fogStart': 0.5,
        '_fogEnd': 300,
        '_fogAtten': 5,
        '_fogTop': 1.5,
        '_fogRange': 1.2,
        '_accurate': False,
    })

    # OctreeInfo
    b.add({
        '__type__': 'cc.OctreeInfo',
        '_enabled': False,
        '_minPos': {'__type__': 'cc.Vec3', 'x': -1024, 'y': -1024, 'z': -1024},
        '_maxPos': {'__type__': 'cc.Vec3', 'x': 1024, 'y': 1024, 'z': 1024},
        '_depth': 8,
    })

    # SkinInfo
    b.add({
        '__type__': 'cc.SkinInfo',
        '_enabled': False,
        '_scale': 5,
    })

    def make_node(name, parent_idx=None, children=None, components=None, pos=None, size=None, anchor=None, layer=33554432):
        node = {
            '__type__': 'cc.Node',
            '_name': name,
            '_objFlags': 0,
            '__editorExtras__': {},
            '_parent': b.ref(parent_idx) if parent_idx is not None else None,
            '_children': [b.ref(c) for c in (children or [])],
            '_active': True,
            '_components': [b.ref(c) for c in (components or [])],
            '_prefab': None,
            '_lpos': pos or {'__type__': 'cc.Vec3', 'x': 0, 'y': 0, 'z': 0},
            '_lrot': {'__type__': 'cc.Quat', 'x': 0, 'y': 0, 'z': 0, 'w': 1},
            '_lscale': {'__type__': 'cc.Vec3', 'x': 1, 'y': 1, 'z': 1},
            '_layer': layer,
            '_euler': {'__type__': 'cc.Vec3', 'x': 0, 'y': 0, 'z': 0},
            '_id': ''
        }
        return b.add(node)

    def make_ui_transform(node_idx, width=100, height=100, anchor_x=0.5, anchor_y=0.5):
        return b.add({
            '__type__': 'cc.UITransform',
            '_name': '',
            '_objFlags': 0,
            '__editorExtras__': {},
            'node': b.ref(node_idx),
            '_enabled': True,
            '__prefab': None,
            '_contentSize': {'__type__': 'cc.Size', 'width': width, 'height': height},
            '_anchorPoint': {'__type__': 'cc.Vec2', 'x': anchor_x, 'y': anchor_y},
            '_id': ''
        })

    def make_sprite(node_idx, color=None, sprite_frame=None, size_mode=1):
        return b.add({
            '__type__': 'cc.Sprite',
            '_name': '',
            '_objFlags': 0,
            '__editorExtras__': {},
            'node': b.ref(node_idx),
            '_enabled': True,
            '__prefab': None,
            '_customMaterial': None,
            '_srcBlendFactor': 2,
            '_dstBlendFactor': 4,
            '_color': color or {'__type__': 'cc.Color', 'r': 255, 'g': 255, 'b': 255, 'a': 255},
            '_spriteFrame': {'__uuid__': sprite_frame, '__expectedType__': 'cc.SpriteFrame'} if sprite_frame else None,
            '_type': 0,
            '_fillType': 0,
            '_sizeMode': size_mode,
            '_fillCenter': {'__type__': 'cc.Vec2', 'x': 0, 'y': 0},
            '_fillStart': 0,
            '_fillRange': 0,
            '_isTrimmedMode': True,
            '_useGrayscale': False,
            '_atlas': None,
            '_id': ''
        })

    def make_label(node_idx, string='', font_size=24, color=None, h_align=1, v_align=1):
        return b.add({
            '__type__': 'cc.Label',
            '_name': '',
            '_objFlags': 0,
            '__editorExtras__': {},
            'node': b.ref(node_idx),
            '_enabled': True,
            '__prefab': None,
            '_customMaterial': None,
            '_srcBlendFactor': 2,
            '_dstBlendFactor': 4,
            '_color': color or {'__type__': 'cc.Color', 'r': 255, 'g': 255, 'b': 255, 'a': 255},
            '_string': string,
            '_horizontalAlign': h_align,
            '_verticalAlign': v_align,
            '_actualFontSize': font_size,
            '_fontSize': font_size,
            '_fontFamily': 'Arial',
            '_isSystemFontUsed': True,
            '_spacingX': 0,
            '_isBatchModeUsed': False,
            '_style': 0,
            '_font': None,
            '_sharedFont': None,
            '_cacheMode': 0,
            '_enableOutline': False,
            '_outlineColor': {'__type__': 'cc.Color', 'r': 0, 'g': 0, 'b': 0, 'a': 255},
            '_outlineWidth': 2,
            '_enableShadow': False,
            '_shadowColor': {'__type__': 'cc.Color', 'r': 0, 'g': 0, 'b': 0, 'a': 255},
            '_shadowOffset': {'__type__': 'cc.Vec2', 'x': 2, 'y': 2},
            '_shadowBlur': 2,
            '_enableItalic': False,
            '_enableBold': False,
            '_underlineHeight': 0,
            '_id': ''
        })

    def make_button(node_idx, target_idx=None, transition=1, color=None):
        return b.add({
            '__type__': 'cc.Button',
            '_name': '',
            '_objFlags': 0,
            '__editorExtras__': {},
            'node': b.ref(node_idx),
            '_enabled': True,
            '__prefab': None,
            'clickEvents': [],
            '_interactable': True,
            '_transition': transition,
            '_normalColor': color or {'__type__': 'cc.Color', 'r': 255, 'g': 255, 'b': 255, 'a': 255},
            '_hoverColor': {'__type__': 'cc.Color', 'r': 255, 'g': 255, 'b': 255, 'a': 255},
            '_pressedColor': {'__type__': 'cc.Color', 'r': 200, 'g': 200, 'b': 200, 'a': 255},
            '_disabledColor': {'__type__': 'cc.Color', 'r': 200, 'g': 200, 'b': 200, 'a': 255},
            '_normalSprite': None,
            '_hoverSprite': None,
            '_pressedSprite': None,
            '_disabledSprite': None,
            '_duration': 0.1,
            '_zoomScale': 1.1,
            '_target': b.ref(target_idx) if target_idx is not None else None,
            '_id': ''
        })

    def make_widget(node_idx, align_flags=45, top=0, bottom=0, left=0, right=0, hcenter=0, vcenter=0):
        return b.add({
            '__type__': 'cc.Widget',
            '_name': '',
            '_objFlags': 0,
            '__editorExtras__': {},
            'node': b.ref(node_idx),
            '_enabled': True,
            '__prefab': None,
            '_alignFlags': align_flags,
            '_target': None,
            '_left': left,
            '_right': right,
            '_top': top,
            '_bottom': bottom,
            '_horizontalCenter': hcenter,
            '_verticalCenter': vcenter,
            '_isAbsLeft': True,
            '_isAbsRight': True,
            '_isAbsTop': True,
            '_isAbsBottom': True,
            '_isAbsHorizontalCenter': True,
            '_isAbsVerticalCenter': True,
            '_originalWidth': 0,
            '_originalHeight': 0,
            '_alignMode': 2,
            '_lockFlags': 0,
            '_id': ''
        })

    def make_camera_node(parent_idx):
        cam_node = make_node('Camera', parent_idx, layer=1073741824)
        cam_comp = b.add({
            '__type__': 'cc.Camera',
            '_name': '',
            '_objFlags': 0,
            'node': b.ref(cam_node),
            '_enabled': True,
            '__prefab': None,
            '_projection': 0,
            '_priority': 0,
            '_fov': 45,
            '_fovAxis': 0,
            '_orthoHeight': 10,
            '_near': 0,
            '_far': 2000,
            '_color': {'__type__': 'cc.Color', 'r': 0, 'g': 0, 'b': 0, 'a': 255},
            '_depth': 1,
            '_stencil': 0,
            '_clearFlags': 7,
            '_rect': {'__type__': 'cc.Rect', 'x': 0, 'y': 0, 'width': 1, 'height': 1},
            '_aperture': 19,
            '_shutter': 7,
            '_iso': 0,
            '_screenScale': 1,
            '_visibility': 1108344832,
            '_targetTexture': None,
            '_id': '63WIch3o5BEYRlXzTT0oWc'
        })
        return cam_node, cam_comp

    def make_panel(name, parent_idx, width=400, height=300, color=(26, 26, 46, 200)):
        panel_node = make_node(name, parent_idx)
        ui_t = make_ui_transform(panel_node, width=width, height=height)
        sprite = make_sprite(panel_node, color={'__type__': 'cc.Color', 'r': color[0], 'g': color[1], 'b': color[2], 'a': color[3]},
                             sprite_frame=UUIDS['default_sprite'], size_mode=0)
        return panel_node, ui_t, sprite

    def make_button_with_label(name, parent_idx, width=150, height=50, label_text='Button',
                               bg_color=(70, 130, 180, 255), label_color=(255,255,255,255)):
        btn_node = make_node(name, parent_idx)
        btn_ui = make_ui_transform(btn_node, width=width, height=height)
        btn_sprite = make_sprite(btn_node, color={'__type__': 'cc.Color', 'r': bg_color[0], 'g': bg_color[1], 'b': bg_color[2], 'a': bg_color[3]},
                                 sprite_frame=UUIDS['default_sprite'], size_mode=0)
        btn_comp = make_button(btn_node, target_idx=btn_node)

        label_node = make_node('Label', btn_node)
        label_ui = make_ui_transform(label_node, width=width, height=height)
        label_comp = make_label(label_node, string=label_text, font_size=24,
                                color={'__type__': 'cc.Color', 'r': label_color[0], 'g': label_color[1], 'b': label_color[2], 'a': label_color[3]})
        return btn_node, btn_comp, label_comp

    # ========== Canvas ==========
    canvas_node = make_node('Canvas', scene_idx, layer=33554432)
    canvas_transform = make_ui_transform(canvas_node, width=960, height=640)
    canvas_comp = b.add({
        '__type__': 'cc.Canvas',
        '_name': '',
        '_objFlags': 0,
        'node': b.ref(canvas_node),
        '_enabled': True,
        '__prefab': None,
        '_cameraComponent': None,  # 稍后设置
        '_alignCanvasWithScreen': True,
        '_id': ''
    })
    canvas_widget = make_widget(canvas_node, align_flags=45, top=0, bottom=0, left=0, right=0)

    # Camera 必须放在 Canvas 下，且 cameraComponent 引用它
    cam_node, cam_comp = make_camera_node(canvas_node)
    b.objects[canvas_comp]['_cameraComponent'] = b.ref(cam_comp)

    # ========== HUD ==========
    hud_node = make_node('HUD', canvas_node)
    hud_ui = make_ui_transform(hud_node, width=960, height=640)

    score_label_node = make_node('ScoreLabel', hud_node)
    score_label_ui = make_ui_transform(score_label_node, width=200, height=40, anchor_x=0, anchor_y=0.5)
    score_label_comp = make_label(score_label_node, string='得分: 0', font_size=28)
    score_label_widget = make_widget(score_label_node, align_flags=9, top=20, left=20)

    high_score_label_node = make_node('HighScoreLabel', hud_node)
    high_score_label_ui = make_ui_transform(high_score_label_node, width=200, height=40, anchor_x=1, anchor_y=0.5)
    high_score_label_comp = make_label(high_score_label_node, string='最高: 0', font_size=28,
                                       h_align=2, v_align=1)
    high_score_label_widget = make_widget(high_score_label_node, align_flags=10, top=20, right=120)

    pause_btn_node, pause_btn_comp, pause_btn_label = make_button_with_label(
        'PauseButton', hud_node, width=60, height=60, label_text='||',
        bg_color=(60, 60, 80, 200), label_color=(255, 255, 255, 255))
    pause_btn_widget = make_widget(pause_btn_node, align_flags=10, top=20, right=20)

    # ========== MenuPanel ==========
    menu_panel, _, _ = make_panel('MenuPanel', canvas_node, width=400, height=300, color=(20, 20, 35, 230))
    menu_title_node = make_node('Title', menu_panel)
    menu_title_ui = make_ui_transform(menu_title_node, width=400, height=80)
    menu_title_label = make_label(menu_title_node, string='贪吃蛇大作战', font_size=48, h_align=1, v_align=1)
    menu_title_widget = make_widget(menu_title_node, align_flags=17, top=60)

    start_btn_node, start_btn_comp, start_btn_label = make_button_with_label(
        'StartButton', menu_panel, width=180, height=60, label_text='开始游戏',
        bg_color=(46, 204, 113, 255), label_color=(255, 255, 255, 255))
    start_btn_widget = make_widget(start_btn_node, align_flags=4, bottom=60)

    # ========== PausePanel ==========
    pause_panel, _, _ = make_panel('PausePanel', canvas_node, width=400, height=300, color=(20, 20, 35, 230))
    pause_title_node = make_node('Title', pause_panel)
    pause_title_ui = make_ui_transform(pause_title_node, width=400, height=80)
    pause_title_label = make_label(pause_title_node, string='游戏暂停', font_size=48, h_align=1, v_align=1)
    pause_title_widget = make_widget(pause_title_node, align_flags=17, top=60)

    resume_btn_node, resume_btn_comp, resume_btn_label = make_button_with_label(
        'ResumeButton', pause_panel, width=180, height=60, label_text='继续游戏',
        bg_color=(46, 204, 113, 255), label_color=(255, 255, 255, 255))
    resume_btn_widget = make_widget(resume_btn_node, align_flags=9, bottom=60, left=30)

    back_menu_btn_node, back_menu_btn_comp, back_menu_btn_label = make_button_with_label(
        'BackMenuButton', pause_panel, width=180, height=60, label_text='返回菜单',
        bg_color=(231, 76, 60, 255), label_color=(255, 255, 255, 255))
    back_menu_btn_widget = make_widget(back_menu_btn_node, align_flags=10, bottom=60, right=30)

    # ========== GameOverPanel ==========
    gameover_panel, _, _ = make_panel('GameOverPanel', canvas_node, width=400, height=360, color=(20, 20, 35, 230))
    gameover_title_node = make_node('Title', gameover_panel)
    gameover_title_ui = make_ui_transform(gameover_title_node, width=400, height=80)
    gameover_title_label = make_label(gameover_title_node, string='游戏结束', font_size=48, h_align=1, v_align=1)
    gameover_title_widget = make_widget(gameover_title_node, align_flags=17, top=60)

    final_score_node = make_node('FinalScoreLabel', gameover_panel)
    final_score_ui = make_ui_transform(final_score_node, width=400, height=40)
    final_score_label = make_label(final_score_node, string='得分: 0', font_size=28, h_align=1, v_align=1)
    final_score_widget = make_widget(final_score_node, align_flags=17, top=140)

    final_high_score_node = make_node('FinalHighScoreLabel', gameover_panel)
    final_high_score_ui = make_ui_transform(final_high_score_node, width=400, height=40)
    final_high_score_label = make_label(final_high_score_node, string='最高: 0', font_size=28, h_align=1, v_align=1)
    final_high_score_widget = make_widget(final_high_score_node, align_flags=17, top=190)

    restart_btn_node, restart_btn_comp, restart_btn_label = make_button_with_label(
        'RestartButton', gameover_panel, width=180, height=60, label_text='重新开始',
        bg_color=(46, 204, 113, 255), label_color=(255, 255, 255, 255))
    restart_btn_widget = make_widget(restart_btn_node, align_flags=9, bottom=60, left=30)

    go_menu_btn_node, go_menu_btn_comp, go_menu_btn_label = make_button_with_label(
        'MenuButton', gameover_panel, width=180, height=60, label_text='返回菜单',
        bg_color=(231, 76, 60, 255), label_color=(255, 255, 255, 255))
    go_menu_btn_widget = make_widget(go_menu_btn_node, align_flags=10, bottom=60, right=30)

    # ========== UIManager Component on Canvas ==========
    ui_manager_comp = b.add({
        '__type__': 'UIManager',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(canvas_node),
        '_enabled': True,
        '__prefab': None,
        'menuPanel': b.ref(menu_panel),
        'hudPanel': b.ref(hud_node),
        'pausePanel': b.ref(pause_panel),
        'gameOverPanel': b.ref(gameover_panel),
        'scoreLabel': b.ref(score_label_comp),
        'highScoreLabel': b.ref(high_score_label_comp),
        'finalScoreLabel': b.ref(final_score_label),
        'finalHighScoreLabel': b.ref(final_high_score_label),
        'startButton': b.ref(start_btn_comp),
        'resumeButton': b.ref(resume_btn_comp),
        'restartButton': b.ref(restart_btn_comp),
        'menuButton': b.ref(go_menu_btn_comp),
        '_id': ''
    })

    # ========== GameBoard ==========
    gameboard_node = make_node('GameBoard', canvas_node, layer=33554432)
    gameboard_ui = make_ui_transform(gameboard_node, width=600, height=600)
    grid_system_comp = b.add({
        '__type__': 'GridSystem',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(gameboard_node),
        '_enabled': True,
        '__prefab': None,
        'gridWidth': 20,
        'gridHeight': 20,
        'cellSize': 30,
        '_id': ''
    })

    grid_bg_node = make_node('GridBackground', gameboard_node)
    grid_bg_ui = make_ui_transform(grid_bg_node, width=600, height=600)
    grid_bg_sprite = make_sprite(grid_bg_node, color={'__type__': 'cc.Color', 'r': 26, 'g': 26, 'b': 46, 'a': 255},
                                 sprite_frame=UUIDS['default_sprite'], size_mode=0)

    snake_container_node = make_node('SnakeContainer', gameboard_node)
    snake_container_ui = make_ui_transform(snake_container_node, width=2, height=2)

    food_container_node = make_node('FoodContainer', gameboard_node)
    food_container_ui = make_ui_transform(food_container_node, width=2, height=2)

    # 设置 GameBoard 的子节点和组件
    b.objects[gameboard_node]['_children'] = [
        b.ref(grid_bg_node),
        b.ref(snake_container_node),
        b.ref(food_container_node),
    ]
    b.objects[gameboard_node]['_components'] = [
        b.ref(gameboard_ui),
        b.ref(grid_system_comp),
    ]

    # ========== GameManager Node ==========
    game_manager_node = make_node('GameManager', scene_idx)
    game_manager_comp = b.add({
        '__type__': 'GameManager',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(game_manager_node),
        '_enabled': True,
        '__prefab': None,
        'gridSystem': b.ref(grid_system_comp),
        'snakeController': None,  # 稍后设置
        'foodSpawner': None,
        'uiManager': b.ref(ui_manager_comp),
        'audioManager': None,
        '_id': ''
    })

    # ========== SnakeController Node ==========
    snake_controller_node = make_node('SnakeController', scene_idx)
    snake_controller_comp = b.add({
        '__type__': 'SnakeController',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(snake_controller_node),
        '_enabled': True,
        '__prefab': None,
        'gridSystem': b.ref(grid_system_comp),
        'bodySegmentPrefab': {'__uuid__': UUIDS['SnakeBody.prefab'], '__expectedType__': 'cc.Prefab'},
        'snakeContainer': b.ref(snake_container_node),
        '_id': ''
    })

    # ========== FoodSpawner Node ==========
    food_spawner_node = make_node('FoodSpawner', scene_idx)
    food_spawner_comp = b.add({
        '__type__': 'FoodSpawner',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(food_spawner_node),
        '_enabled': True,
        '__prefab': None,
        'gridSystem': b.ref(grid_system_comp),
        'foodContainer': b.ref(food_container_node),
        'foodPrefab': {'__uuid__': UUIDS['Food.prefab'], '__expectedType__': 'cc.Prefab'},
        'maxFoodCount': 3,
        '_id': ''
    })

    # 修正 GameManager 引用
    b.objects[game_manager_comp]['snakeController'] = b.ref(snake_controller_comp)
    b.objects[game_manager_comp]['foodSpawner'] = b.ref(food_spawner_comp)

    # ========== AudioManager Node ==========
    audio_manager_node = make_node('AudioManager', scene_idx)
    audio_source_bgm = b.add({
        '__type__': 'cc.AudioSource',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(audio_manager_node),
        '_enabled': True,
        '__prefab': None,
        '_clip': {'__uuid__': UUIDS['bgm.wav'], '__expectedType__': 'cc.AudioClip'},
        '_volume': 1.0,
        '_loop': True,
        '_playOnAwake': False,
        '_id': ''
    })
    audio_source_sfx = b.add({
        '__type__': 'cc.AudioSource',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(audio_manager_node),
        '_enabled': True,
        '__prefab': None,
        '_clip': None,
        '_volume': 1.0,
        '_loop': False,
        '_playOnAwake': False,
        '_id': ''
    })
    audio_manager_comp = b.add({
        '__type__': 'AudioManager',
        '_name': '',
        '_objFlags': 0,
        '__editorExtras__': {},
        'node': b.ref(audio_manager_node),
        '_enabled': True,
        '__prefab': None,
        'bgmSource': b.ref(audio_source_bgm),
        'sfxSource': b.ref(audio_source_sfx),
        'eatClip': {'__uuid__': UUIDS['eat.wav'], '__expectedType__': 'cc.AudioClip'},
        'gameOverClip': {'__uuid__': UUIDS['gameover.wav'], '__expectedType__': 'cc.AudioClip'},
        'buttonClickClip': {'__uuid__': UUIDS['button_click.wav'], '__expectedType__': 'cc.AudioClip'},
        '_id': ''
    })

    # 修正 GameManager 的 audioManager 引用
    b.objects[game_manager_comp]['audioManager'] = b.ref(audio_manager_comp)

    # 设置逻辑节点的组件
    b.objects[game_manager_node]['_components'] = [b.ref(game_manager_comp)]
    b.objects[snake_controller_node]['_components'] = [b.ref(snake_controller_comp)]
    b.objects[food_spawner_node]['_components'] = [b.ref(food_spawner_comp)]
    b.objects[audio_manager_node]['_components'] = [
        b.ref(audio_source_bgm),
        b.ref(audio_source_sfx),
        b.ref(audio_manager_comp),
    ]

    # 设置场景子节点（GameBoard 作为 Canvas 子节点，不在此处）
    b.objects[scene]['_children'] = [
        b.ref(canvas_node),
        b.ref(game_manager_node),
        b.ref(snake_controller_node),
        b.ref(food_spawner_node),
        b.ref(audio_manager_node),
    ]

    # 设置 Canvas 子节点
    b.objects[canvas_node]['_children'] = [
        b.ref(cam_node),
        b.ref(hud_node),
        b.ref(menu_panel),
        b.ref(pause_panel),
        b.ref(gameover_panel),
        b.ref(gameboard_node),
    ]
    b.objects[canvas_node]['_components'] = [
        b.ref(canvas_transform),
        b.ref(canvas_comp),
        b.ref(canvas_widget),
        b.ref(ui_manager_comp),
    ]

    return b.to_json()


if __name__ == '__main__':
    json_str = build_scene()
    SCENE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCENE_PATH.write_text(json_str, encoding='utf-8')
    print(f'MainScene.scene generated: {SCENE_PATH}')
