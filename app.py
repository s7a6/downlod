from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
import os
import yt_dlp
import tempfile

app = Flask(__name__)
app.secret_key = 'secret-key'  # ضروري لعرض رسائل الفلاش

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format', 'video')  # 'video' or 'audio'
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best' if format_type == 'audio' else 'best',
            'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
    except Exception as e:
        print('Download error:', e)
        flash(f'حدث خطأ أثناء التحميل: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 