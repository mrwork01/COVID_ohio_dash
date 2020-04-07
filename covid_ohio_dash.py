import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import sqlite3
import datetime as dt

app = dash.Dash()

app.layout = html.Div([
				html.Div(children='Ohio Covid-19 Dashboard',
					style=dict(textAlign='center',
							    fontSize=30)),
				html.Br(),
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
						html.Label(['Total Case Count'],
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
						html.Label(['Total Death Count'],
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

	start_date = '2020-03-20'
	end_date = dt.datetime.today()

	df_forecast = pd.read_csv('COVID forecast.csv')
	df_forecast['date'] = pd.to_datetime(df_forecast['date'])
	mask = (df_forecast['date'] > start_date) & (df_forecast['date'] <= end_date)
	df_forecast = df_forecast.loc[mask]

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
						 y=df_forecast['forecast'],
						 name='Forecast',
						 opacity=0.5,
						 marker=dict(color='orange')))


	layout_1 = go.Layout(title='New Daily Cases')

	output_1 = dict(data=trace1, layout=layout_1)

	trace2 = []


	trace2.append(go.Scatter(x=death_sum.index,
  							 y=death_sum,
  							 mode='lines',
  							 name='New Cases',
  							 line=dict(color='blue')))

	layout_2 = go.Layout(title='New Daily Deaths')

	output_2 = dict(data=trace2, layout=layout_2)


	return output_1, output_2, total_cases, total_deaths


#------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
