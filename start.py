import http.server
import socketserver
import webbrowser
import os
import sys

# 设置端口
PORT = 8000

# 自定义服务器，添加 ffmpeg.wasm 必须的安全头 (COOP/COEP)
class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许 SharedArrayBuffer (关键设置)
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        super().end_headers()

    # 禁用缓存，防止调试时看不到更新
    def send_response(self, code, message=None):
        super().send_response(code, message)
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')

# 切换到脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"start on http://localhost:{PORT}")
print("使用时请勿关闭此窗口")

# 自动打开浏览器
webbrowser.open(f'http://localhost:{PORT}/index.html')

# 启动服务
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass