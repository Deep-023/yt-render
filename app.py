from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/get_video_url')
def get_video_url():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({'error': 'Missing video ID'}), 400

    try:
        url = f'https://www.youtube.com/watch?v={video_id}'
        ydl_opts = {
            'quiet': True,
            'format': 'best[ext=mp4][protocol=https]',
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'title': info.get('title'), 'stream_url': info['url']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)