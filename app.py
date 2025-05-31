from flask import Flask, request, render_template_string
import yaml
import html

app = Flask(__name__)

@app.route("/")
def index():
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Configuration Portal - Upload Config</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h2>📁 Import Project Config</h2>
            <p>Paste your YAML configuration below:</p>
            <form method="POST" action="/import">
                <textarea name="yaml_data" rows="18" style="width:100%;">name: MyProject\nscripts:\n  - echo 'Hello!'</textarea><br><br>
                <button type="submit">🚀 Import Config</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(template)

def render_yaml(data):
    """Recursively render YAML data into nested HTML lists with HTML escaping."""
    if isinstance(data, dict):
        html_output = "<ul>"
        for key, value in data.items():
            escaped_key = html.escape(str(key))
            html_output += f"<li><b>{escaped_key}:</b> {render_yaml(value)}</li>"
        html_output += "</ul>"
        return html_output
    elif isinstance(data, list):
        html_output = "<ul>"
        for item in data:
            html_output += f"<li>{render_yaml(item)}</li>"
        html_output += "</ul>"
        return html_output
    elif isinstance(data, bytes):
        return f"<pre>{html.escape(data.decode(errors='ignore'))}</pre>"
    else:
        return html.escape(str(data))


@app.route("/import", methods=["POST"])
def import_config():
    yaml_data = request.form['yaml_data']
    try:
        config = yaml.load(yaml_data, Loader=yaml.Loader)
        html_content = render_yaml(config)

        template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>ConfigPort - Parsed YAML</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <h2>📄 Parsed YAML:</h2>
                {html_content}
            </div>
        </body>
        </html>
        """

        return render_template_string(template)


    except Exception as e:
        return f"<pre>Error loading config:\n{e}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
