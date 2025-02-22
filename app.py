import gradio as gr
from knowledge_generate import extract_and_summarize
from video_generate import cut_video, video_process_concatnate

# Gradio界面
with gr.Blocks() as demo:

    # 变量
    cut_video_path = gr.State()
    output_video_path = gr.State('output')
    pic1_path = gr.State('utils/pic/pic1.png')
    pic2_path = gr.State('utils/pic/pic2.png')

    with open('prompt.txt', 'r', encoding='utf-8') as file:
        initial_prompt = file.read()
    
    # Add custom CSS to style the video background and other components
    gr.HTML("""
    <style>
    /* 全局样式，设置基本字体和背景颜色 */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #f4f4f4;
    }

    /* 为视频输出区域添加样式 */
    #video_output {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* 为视频参数输入列添加样式 */
    #video_param {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        margin-right: 20px;
    }

    /* 为视频播放列添加样式 */
    #video_play {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }

    /* 为提示词设置列添加样式 */
    #prompt_set {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        margin-right: 20px;
    }

    /* 为知识展示列添加样式 */
    #knowledge_play {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }

    /* 为小文本框样式添加样式 */
    .small-textbox {
        width: 100%;
        height: 35px;
        font-size: 14px;
        margin: 5px 0;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 0 10px;
        transition: border-color 0.3s ease;
    }

    .small-textbox:focus {
        border-color: #007BFF;
        outline: none;
    }

    /* 为按钮添加样式 */
    button {
        background-color: #007BFF;
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        font-size: 14px;
        margin-top: 10px;
    }

    button:hover {
        background-color: #0056b3;
    }

    /* 为 Markdown 标题添加样式 */
    h3 {
        color: #333;
        margin-bottom: 15px;
    }

    /* 为文本框标签添加样式 */
    label {
        display: block;
        margin-bottom: 5px;
        font-size: 14px;
        font-weight: 600;
        color: #555;
    }

    /* 调整行布局的间距 */
    .gr-row {
        margin-bottom: 20px;
    }
</style>
    """)

    with gr.Row():

        with gr.Column(scale=0.3):
            with gr.Row():
                gr.Markdown("""
                <div style='text-align: center; font-family: "Comic Sans MS", cursive, sans-serif;'>
                    <strong style='font-size: 50px;'>🎥 LuLu 🎥 Helper</strong><br>
                    <em style='font-size: 16px;'>Produced by Yuanyuan</em>
                </div>
                """)
            with gr.Row(elem_id="video_param"):
                with gr.Column():
                    video_input = gr.Video(label="上传视频", height=200, width=400)
                
                with gr.Column():
                    start_time_input = gr.Textbox(label="开始时间 (格式为 HH:MM:SS)", value="00:05:20",
                                                elem_classes="small-textbox")
                    end_time_input = gr.Textbox(label="结束时间 (格式为 HH:MM:SS)", value="00:05:21",
                                                elem_classes="small-textbox")
                    cover_height_input = gr.Slider(0.0, 1.0, step=0.01, label="遮盖高度比例", value=0.15,
                                                elem_classes="small-textbox")
                    cover_width_input = gr.Slider(0.0, 1.0, step=0.01, label="遮盖宽度比例", value=0.95,
                                                elem_classes="small-textbox")
                    
                    cut_button = gr.Button("截取视频")
                    cut_video_message = gr.Textbox(label="截取结果", interactive=False)

        with gr.Column(scale=0.4):
            with gr.Row(scale=1, elem_id="video_play"):
                # gr.Markdown("<div style='background-color: #f0f0f0; padding: 10px;'>### Magic video dealer</div>")
                with gr.Column():
                    process_button = gr.Button("剪辑视频")
                with gr.Column():
                    video_output = gr.Video(label="成片", elem_id="video_output")
                    

            with gr.Row(scale=2, elem_id="prompt_set"):
                with gr.Column():
                    extract_button = gr.Button("提取文字")
                with gr.Column():
                    system_prompt = gr.Textbox(label='人设提示词', value=initial_prompt, lines=7, interactive=True)
                    save_prompt_button = gr.Button("保存提示词")
                


        with gr.Column(scale=0.3, elem_id="knowledge_play"):
            text_output = gr.Textbox(label="文案自动生成", lines=27)
    


    def update_video_input(cut_video_path):
        return cut_video_path

    def save_prompt(prompt_text):
        with open('prompt.txt', 'w', encoding='utf-8') as file:
            file.write(prompt_text)
        return "提示词已保存！"

    cut_button.click(
        fn=lambda *args: (cut_video(*args), "视频截取成功！")[0],
        inputs=[video_input, output_video_path, start_time_input, end_time_input],
        outputs=[cut_video_path, cut_video_message]
    )
    
    cut_video_path.change(
        fn=update_video_input,
        inputs=[cut_video_path],
        outputs=[video_input]
    )
    
    process_button.click(
        fn=video_process_concatnate,
        inputs=[cut_video_path, cover_height_input, cover_width_input, pic1_path, pic2_path],
        outputs=video_output
    )
        
    extract_button.click(
        fn=extract_and_summarize,
        inputs=[cut_video_path, system_prompt],
        outputs=text_output
    )

    save_prompt_button.click(
        fn=save_prompt,
        inputs=[system_prompt],
        outputs=[]
    )

if __name__ == "__main__":
    demo.launch(share=True)