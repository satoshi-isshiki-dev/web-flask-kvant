from flask import render_template
from news import app

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/modules')
def module():
    return render_template('modules.html')

@app.route('/foto')
def foto():
    return render_template('foto.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/modules/junior')
def junior_module():
    return render_template('junior_module.html')

@app.route('/modules/middle')
def middle_module():
    return render_template('middle_module.html')

@app.route('/modules/senior')
def senior_module():
    return render_template('senior_module.html')

if __name__ == '__main__':
    app.run(debug=True)