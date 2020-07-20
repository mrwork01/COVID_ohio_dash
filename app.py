import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import sqlite3
import datetime as dt

app = dash.Dash()

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Global site tag (gtag.js) - Google Analytics -->
		<script async src="https://www.googletagmanager.com/gtag/js?id=UA-163136461-2"></script>
		<script>
  			window.dataLayer = window.dataLayer || [];
  			function gtag(){dataLayer.push(arguments);}
  			gtag('js', new Date());

  			gtag('config', 'UA-163136461-2');
		</script>
	</head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div>*Powered by J&O Financial</div>
    </body>
</html>
'''

server = app.server

app.layout = html.Div([
				html.Div(children='Ohio Covid-19 Dashboard',
					style=dict(textAlign='center',
							    fontSize=30)),
				html.Div(children='A Simple Look at Covid-19 in Ohio',
					style=dict(textAlign='center',
							    fontSize=20)),
				html.Br(),
				html.Br(),
				html.Div([
					html.Label('''Disclaimer:  Data is not in real time.  Due to the nature of the situation and manner of
								collection, data may lag several days.'''),
					html.Br(),
					html.Label('''*Last Updated: 7/20/20 6:10 AM EST''')]),

				html.Br(),
				html.Div([
					html.Div([
						dcc.Graph(id='daily_new_cases_graph')],
					style=dict(border='none',
                                   borderRadius='5px',
                                   margin='5px',
                                   width='73%',
                                   height='450px',
                                   display='inline-block',
                                   boxShadow='3px 3px 3px lightgrey',
                                   float='left')),
					html.Div([
						html.Br(),
						html.Br(),
						html.Br(),
						html.Br(),
						html.Label(['Total Ohio Case Count'],
							style=dict(fontSize=30,
									   textDecoration='underline')),
						html.Br(),
						html.Br(),
						html.Br(),
						html.Label(id='total_cases',
							style=dict(fontSize=30))],
						style=dict(border='none',
                                   margin='5px',
                                   boxShadow='3px 3px 3px lightgrey',
                                   width='23%',
                                   height='450px',
                                   display='inline-block',
                                   textAlign='center',
                                   verticalAlign='middle',
                                   backgroundColor='#ffffff'))]),
				html.Br(),
				html.Div([
					html.Div([
                        dcc.Graph(id='daily_new_deaths_graph')],
                     style=dict(border='none',
                                   borderRadius='5px',
                                   margin='5px',
                                   width='73%',
                                   height='450px',
                                   display='inline-block',
                                   boxShadow='3px 3px 3px lightgrey',
                                   float='left')),
					html.Div([
						html.Br(),
						html.Br(),
						html.Br(),
						html.Br(),
						html.Label(['Total Ohio Death Count'],
							style=dict(fontSize=30,
								       textDecoration='underline')),
						html.Br(),
						html.Br(),
						html.Br(),
						html.Label(id='total_deaths',
							style=dict(fontSize=30))],
						style=dict(border='none',
                                   margin='5px',
                                   boxShadow='3px 3px 3px lightgrey',
                                   width='23%',
                                   height='450px',
                                   display='inline-block',
                                   textAlign='center',
                                   backgroundColor='#ffffff'))]),


				dcc.Interval(id='interval_call',
                    interval=6000*1000,
                    n_intervals=0)

			 ],
			 style=dict(backgroundColor='#f2f2f2',
                               height='none'))


#------------------------------------------------------------------
# piv_by_date() takes in a dataframe and pivots it into certain
# date group
#------------------------------------------------------------------
@app.callback([Output('daily_new_cases_graph','figure'),
			   Output('daily_new_deaths_graph','figure'),
			   Output('total_cases','children'),
			   Output('total_deaths','children')],
             [Input('interval_call','n_intervals')])

def update_new_cases(n_intervals):

	start_date = pd.to_datetime('2020-02-12')
	end_date = dt.datetime.today()

	#US Data
	df_us = pd.read_csv('us_data.csv')
	df_us['date'] = pd.to_datetime(df_us['date'])
	df_us['deaths'] = df_us['deaths'].astype(int)
	df_us['deaths'] = df_us['deaths'] * .035
	df_us['oh_deaths'] =  df_us['oh_deaths'].astype(int)


	#Forecast Data
	df_forecast = pd.read_csv('COVID forecast.csv')
	df_forecast['date'] = pd.to_datetime(df_forecast['date'])
	mask = (df_forecast['date'] > start_date) & (df_forecast['date'] <= end_date)
	df_forecast = df_forecast.loc[mask]

	#Ohio Data
	df = pd.read_csv('COVIDSummaryData.csv')
	df = df[:-1]
	df['Case Count'] =  df['Case Count'].astype(int)
	df['Death Count'] =  df['Death Count'].astype(int)

	df['Onset Date'] = pd.to_datetime(df['Onset Date'])
	case_sum = df['Case Count'].groupby(df['Onset Date']).sum()
	death_sum = df['Death Count'].groupby(df['Onset Date']).sum()

	total_cases = case_sum.sum()
	total_cases = '{:,}'.format(total_cases)
	total_deaths = death_sum.sum()
	total_deaths = '{:,}'.format(total_deaths)

	trace1 = []


	trace1.append(go.Scatter(x=case_sum.index,
  							 y=case_sum,
  							 mode='lines',
  							 name='New Cases',
  							 line=dict(color='blue')))

	trace1.append(go.Bar(x=df_forecast['date'],
						 y=df_forecast['forecast_2'],
						 name='Case Forecast',
						 opacity=0.5,
						 marker=dict(color='red')))


	layout_1 = go.Layout(title='New Daily Cases',
						 barmode='stack',
						 annotations=[dict(x='2020-3-23',
						 				  y=268,
						 				  xref='x',
						 				  yref='y',
						 				  ax=50,
						 				  ay=-50,
						 				  text='Ohio Stay in Place',
						 				  showarrow=True,
						 				  arrowhead=1),
						 			  dict(x='2020-3-16',
						 				  y=190,
						 				  xref='x',
						 				  yref='y',
						 				  text='Ohio Closes Schools',
						 				  showarrow=True,
						 				  arrowhead=1)])

	output_1 = dict(data=trace1, layout=layout_1)

	trace2 = []


	trace2.append(go.Scatter(x=df_us['date'],
  							 y=df_us['oh_deaths'],
  							 mode='lines',
  							 name='Ohio Deaths per Day',
  							 line=dict(color='blue')))

	trace2.append(go.Scatter(x=df_us['date'],
  							 y=df_us['deaths'],
  							 mode='lines',
  							 name='US Adj Deaths per Day ',
  							 line=dict(color='red')))

	layout_2 = go.Layout(title='Ohio vs US Daily Deaths<br><sub>(US Deaths Adjusted by Population)</sub>')

	output_2 = dict(data=trace2, layout=layout_2)


	return output_1, output_2, total_cases, total_deaths


#------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
