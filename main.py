import random
import string
import json
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

shortened_urls = {}
   

def generate_short_url(length=6):
    
    # collection of characters containing all letters in the alphabet and digits 
    chars = string.ascii_letters + string.digits
    
    # a short url that is a string combined with a random choice of characters from the
    # chars collection in the set length of the function: 
    short_url = "".join(random.choice(chars) for _ in range(length))

    return short_url


# make an endpoint for both GET and POST methods: 
@app.route("/", methods=['GET','POST'])
def index():

    # if request is POST, take the long url from the parameter, and the short_url function
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate_short_url() 

        while short_url in shortened_urls:
            short_url = generate_short_url()

        # set the shortened URL to the long URL in the dictionary to identify it in the future
        shortened_urls[short_url] = long_url
        with open("urls.json", "w") as file_to_write:
            json.dump(shortened_urls, file_to_write)

        return f'Shortened URL: {request.url_root}{short_url}'
    return render_template("index.html")  


@app.route("/<short_url>")
def redirect_url(short_url):
    # When getting the URL, return the value from the dictionary then redirect it to the long URL
    # effectively, completing the URL shortener. 
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        
        # if key, is not identified to be assigned to any value or it doesn't exist: return 404
        return "URL not found", 404        


if __name__ == "__main__":
    app.jinja_env.auto_reload = True 
    # load the saved URLs from previous sessions from the JSON into the dictionary: 
    with open("urls.json", "r") as f:
        shortened_urls = json.load(f)
    app.run(debug=True)
