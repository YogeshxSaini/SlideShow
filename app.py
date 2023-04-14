from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)

def get_random_image_url(category_name, shown_images):
  file_path = os.path.join('links', f'{category_name}_urls.txt')
  with open(file_path, 'r') as f:
    urls = [url.strip() for url in f.readlines()]
  urls = [url for url in urls if url not in shown_images]
  if not urls:
    urls = [url for url in urls if url not in shown_images]
  if not urls:
    return None
  url = random.choice(urls)
  shown_images.add(url)
  return url

UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', '2500'))

@app.route('/')
def category_selection():
  return render_template('category_selection.html')


@app.route('/category/<category_name>')
def show_images(category_name):
  shown_images = set()
  return render_template('image_display.html',category_name=category_name,shown_images=shown_images)


@app.route('/get_random_image/<category_name>')
def get_random_image(category_name):
  shown_images = set(request.args.getlist('shown_images[]'))
  url = get_random_image_url(category_name, shown_images)
  return jsonify({'url': url})


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000, debug=True)