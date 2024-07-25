import os
import random

import requests
import json
import re
import html
from flask import Flask, send_file, render_template, request, redirect, url_for, jsonify
import db
from db import logger
import google.generativeai as genai
from urllib.parse import urlparse
import cloudscraper

app = Flask(__name__)


def extract_cafe_via_gemini(gemini_api_key, html_source):
    """return ai assisted cafe information"""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    escaped_html_source = html.escape(html_source)
    prompt = f"""
        Fill in this json ({{"name":"", "address":"", "phone":""}}) 
        with cafe name, address and phone 
        from this escaped html source: {escaped_html_source}"""
    response = model.generate_content(prompt)
    logger.info(response.text)
    json_pattern = r'\{[\s\S]*\}'
    match = re.search(json_pattern, response.text)
    if match:
        try:
            json_text = match.group()
            json_data = json.loads(json_text)
            cafe = {
                'name': json_data["name"],
                'address': json_data["address"],
                'phone': json_data["phone"],
                'url': 'cafe_url'
            }
            return cafe
        except json.JSONDecodeError:
            raise Exception("Found text is not valid JSON")
    else:
        raise Exception("No JSON found in the string")


@app.route("/", methods=['GET', 'POST'])
def index():
    error_message = ""
    info_message = ""
    cafe_url = ""
    gemini_api_key = ""
    cafes = []
    try:
        if 'cafe-url' in request.form:
            cafe_url = request.form["cafe-url"]
            gemini_api_key = request.form["gemini-api-key"]

            # response = requests.get(cafe_url) # sometimes gets blocked by cloudflare
            scraper = cloudscraper.create_scraper()  # see https://github.com/VeNoMouS/cloudscraper
            response = scraper.get(cafe_url)
            response.encoding = "utf-8"  # TODO review encoding
            html_source = response.text
            cafe = extract_cafe_via_gemini(gemini_api_key, html_source)
            domain = urlparse(cafe_url).netloc
            db.insert_cafe(domain, cafe_url, cafe["name"], cafe["address"], cafe["phone"])
            info_message = "Scraped successfully"
        try:
            cafes = db.get_cafes()
        except Exception as ex:
            logger.exception(f"error: {ex}")
            error_message = f'Error: {ex}'
    except Exception as ex:
        logger.exception(f"error: {ex}")
        error_message = f'Error: {ex}'

    return render_template('index.html',
                           timestamp=random.randint(1, 1000),
                           error_message=error_message,
                           info_message=info_message,
                           cafe_url=cafe_url,
                           gemini_api_key=gemini_api_key,
                           cafes=cafes)


def main():
    db.init()
    app.run(port=int(os.environ.get('PORT', 8081)), debug=True)


if __name__ == "__main__":
    main()
