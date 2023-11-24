from flask import Flask, render_template

app = Flask(__name__)

@app.route('/result1/<user>')
def result1(user):
    my_dict = {'phy': 50, 'che': 60, 'maths': 70, 'Geo': 45}
    return render_template('result1.html', name=user, result1=my_dict)

if __name__ == '__main__':
    app.run(debug=True)