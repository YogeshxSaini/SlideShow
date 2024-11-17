from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)

def get_random_image_url(category_name, shown_images):
    # Assuming you are using a static file like 'links/category_name_urls.txt'
    file_path = os.path.join('links', f'{category_name}_urls.txt')

    # Vercel uses a serverless environment so you should ideally use cloud storage, 
    # but for the purpose of this example, we will keep this simple and assume file access works.
    try:
        with open(file_path, 'r') as f:
            urls = [url.strip() for url in f.readlines()]
    except Exception as e:
        return None

    # Filter out shown images
    urls = [url for url in urls if url not in shown_images]

    if not urls:
        # If no more new images are available, restart the list or return None
        urls = [url for url in urls if url not in shown_images]
        if not urls:
            return None

    url = random.choice(urls)
    shown_images.add(url)  # Track shown images to avoid showing the same one again
    return url

UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', '2500'))

@app.route('/')
def category_selection():
    # Renders the category selection template.
    return render_template('category_selection.html')

@app.route('/category/<category_name>')
def show_images(category_name):
    shown_images = set()
    return render_template('image_display.html', category_name=category_name, shown_images=shown_images)

@app.route('/get_random_image/<category_name>')
def get_random_image(category_name):
    # Get the list of shown images from the URL query params
    shown_images = set(request.args.getlist('shown_images[]'))
    url = get_random_image_url(category_name, shown_images)
    return jsonify({'url': url})

# Since Vercel runs the function as a serverless endpoint, we don't need to call app.run() 
# Here we are explicitly defining the entry point as a serverless function

if __name__ == '__main__':
    # The app won't run on a traditional server; Vercel will invoke it as a function
    pass
