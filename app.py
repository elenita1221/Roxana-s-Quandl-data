from flask import Flask, render_template, request, redirect
import Quandl
import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
#from bokeh.resources import CDN

app = Flask(__name__)
app.vars={}
app.vars['color'] = {
    'Close': 'blue',
    'Adj. Close': 'green',
    'Open': 'yellow',
    'Adj. Open': 'red'
}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
     return render_template('index.html')
  else:  
     app.vars['ticker'] = request.form['ticker'].upper() 
     app.vars['features'] = request.form.getlist('features')
     return redirect('/graph')

@app.route('/graph', methods=['GET','POST'])
def graph():
  stock_ticker= app.vars['ticker']
  df = Quandl.get("WIKI/"+stock_ticker, returns="pandas", authtoken="jxC1mNzsEpVGzojfQWUW")
  ticker_dates = np.array(df[df.index >= '2014-01-01'].index, dtype=np.datetime64)
  p = figure(width=900, height=500, x_axis_type="datetime", title="Data from Quandl WIKI set")
  for category in app.vars['features']:
        p.line(ticker_dates, df[category], color=app.vars['color'][category], line_width=2, legend=stock_ticker + ": " + category)

  p.xaxis.axis_label = 'Date'
  p.yaxis.axis_label = 'Price'
  script, div = components(p)
  return render_template('graph.html', ticker=stock_ticker, script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)