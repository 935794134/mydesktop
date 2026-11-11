# My Desktop

把便签卡片贴在桌面上的小工具。Python + PySide6，仅 Windows。

## 功能

- 卡片可以拖到桌面任意位置，坐标存进 `data.json`，下次启动位置不变
- 窗口常驻**最底层**，不挡其他窗口；点关闭只是隐藏，仍在托盘运行
- 托盘菜单退出
- 调整移动步长（1 / 5 / 10 / 20 / 50 像素），选中某张卡后用按钮微调位置
- 一键隐藏 / 显示所有卡片的标题

## 运行

```bash
pip install PySide6
python main.py
```

窗口置底用的是 Win32 `SetWindowPos`（`to_buttom()`），**只能在 Windows 上跑**。

## 文件

| 文件 | 说明 |
|---|---|
| `main.py` | 主程序 |
| `data.json` | 卡片内容与设置，改这个文件就能换字 |
| `icon.ico` | 托盘图标 |

## 配置

`data.json` 分两块：

```json
{
  "sittings": { "title_visible": false, "background_rgb": "0, 0, 0", "background_opacity": "0.6" },
  "cards": [ { "index": 1, "title": "...", "info": "...", "width": 340, "height": 150, "x": 600, "y": 344 } ]
}
```

`info` 里的 `\n` 会原样换行。

## 已知限制

- 只支持 Windows
- 卡片内容靠手改 `data.json`，程序里没有编辑界面
