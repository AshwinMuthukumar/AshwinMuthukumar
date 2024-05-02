from flask import Flask, request, render_template

import pandas as pd

import concurrent.futures

from AJIO import ajio

from BWF import bwf

from FLIPKART import flipkart

from MYNTRA import myntra


app = Flask(__name__,static_url_path="",static_folder="static")


@app.route('/')

def default():

 return render_template("homepage.html")

@app.route('/Homepage',methods = ['GET','POST'])

def home():

 return render_template("homepage.html")

@app.route('/Guide',methods = ['GET','POST'])

def guide():

 return render_template("guide.html")

@app.route('/About',methods = ['GET','POST'])

def about():

 return render_template("about.html")

@app.route('/result',methods = ['GET','POST'])

def api():
    query1 = request.form["search"]

    if query1=="":
        return render_template("homepage.html")
    
    query = query1.replace(" ","%20")

    with concurrent.futures.ThreadPoolExecutor() as executor:

        future1 = executor.submit(ajio,query)
        future2 = executor.submit(bwf,query)
        # future3 = executor.submit(flipkart,query)
        future4 = executor.submit(myntra,query)

        df1 = future1.result()
        df2 = future2.result()
        # df3 = future3.result()
        df4 = future4.result()

    # frames = [df1,df2,df3,df4]
    frames = [df1,df2,df4]

    res1 = pd.concat(frames)

    main_df = res1.sort_values(by=['Discount'],ascending=False)

    data = main_df.values

    size = len(data)
    
    return render_template("products.html", data=data, size = size, query=query1)


if __name__ == '__main__':

 app.run(debug=True)
