from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return "Main"

@app.route('/site')
def site():
    return render_template("site.html")

if __name__ == '__main__':
    app.run(debug=True)
