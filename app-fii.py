from flask import Flask, redirect, url_for, render_template,request


app = Flask(__name__)

@app.route("/funds")
@app.route("/", methods=['GET', 'POST'])   # criando rota principal
def bemvindo():
    if request.method == 'POST':
        FII_desejado  = request.form.get('FII_desejado')
        #framework = request.form.get('framework')
        return redirect(f'https://www.fundsexplorer.com.br/funds/{FII_desejado}')
    return render_template('index.html')

       
if __name__  == "__main__":
    app.run(debug= True,host= '20.124.43.86', port=6379)  