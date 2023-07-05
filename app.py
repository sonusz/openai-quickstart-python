import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]        
        resource_name = 'gpcs-nw-west-europe'
        openai.api_base = f'https://{resource_name}.openai.azure.com/'
        openai.api_type = 'azure'
        openai.api_version = '2023-05-15'
        deployment_id = 'gpcs-nw-west-europe-poc'

        response = openai.ChatCompletion.create(
                deployment_id=deployment_id,
                stream=False,
                messages=[{'role':'system', 'content': generate_prompt(animal)}],
                temperature=0.6
            )
        return redirect(url_for("index", result=response['choices'][0]['message'].get('content', 'No response from OpenAI')))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
