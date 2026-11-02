# gyro-orbit

手機陀螺儀控制的「子彈時間」環繞效果: 轉動手機, 畫面就繞著主體轉一圈。

Demo: https://zbryikt.github.io/gyro-orbit/

## 做法

1. 用 OpenAI `gpt-image-2` 生成一張場景圖 ( 中間有主體 )。
2. 用 fal 上的 MiniMax H3 ( `minimax/h3-max-turbo/image-to-video` ) 做首尾幀 ( FLF ) 生成: 首幀與尾幀都是同一張圖, prompt 要求時間凍結、鏡頭等速環繞一圈。prompt 見 `scripts/prompt-orbit-v2.txt`。
3. 影片抽成逐幀 JPEG ( 去掉結尾回到原圖後的靜止段 ), 網頁用 canvas 依角度畫出對應幀, 相鄰幀交叉淡入。

## 網頁操作

- 轉動 ( 預設 ): 積分繞手機 y 軸的角速度。iOS Safari 的 `rotationRate` 軸向與規格不同 ( alpha/beta/gamma = x/y/z ), 所以 iOS 讀 `beta`, 其他讀 `gamma`。
- 傾斜: 用 `deviceorientation` 的 gamma, 以開始時的姿勢為原點。
- 桌機可拖曳。`?set=v2a|v2b` 切換影片, `?debug=1` 顯示角速度數值。
- 陀螺儀需要 HTTPS。

## 腳本

金鑰從 `~/.ssh/ai/envs` 讀取 ( `OPENAI_API_KEY`, `FALAI_API_KEY` )。

    python3 scripts/gen_image.py "<prompt>" out.png gpt-image-2
    python3 scripts/gen_video.py in.jpg out.mp4 4 1080P "$(cat scripts/prompt-orbit-v2.txt)"
    ffmpeg -i out.mp4 -frames:v <N> -vf scale=720:-2 -q:v 4 web/sets/<name>/%03d.jpg
    python3 scripts/serve.py 8790 web
