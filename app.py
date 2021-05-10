import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# read the usage data file and verify data
user_usage = pd.read_csv("data/user_usage.csv")
# usage.head()

user_device = pd.read_csv("data/user_device.csv")
# user_device.head()

# do a inner join for usage and users device to get the usage per device
result = pd.merge(user_usage,
                  user_device[['use_id', 'platform', 'device']],
                  on='use_id')

# pd.set_option('display.max_rows', None)
# result

# inner join returned less number of rows since some users do not have the device information
# we should do a left join to include the null device rows
result = pd.merge(user_usage,
                  user_device[['use_id', 'platform', 'device']],
                  on='use_id',
                  how='left')
# result
# this has all the rows

# we have the model information for devices, lets bring those in
devices = pd.read_csv("data/android_devices.csv")
# devices.head()

# left join with earlier merged data
# the device column is called Model here, we cant rename since there is another Device column
result = pd.merge(result,
                  devices[['Retail Branding', 'Model']],
                  left_on='device',
                  right_on='Model',
                  how='left')

# result.head()

# create a scatter plot after replacing the null values with Unknown
result1 = result.replace(np.nan, "Unknown")
fig1 = go.Figure(go.Scatter(x=result1['Model'], y=result1['outgoing_mins_per_month'], mode='markers'))
fig1.update_layout(
    title='Minutes of usage per device type (includes unknown devices)',
    showlegend=True)


# create a bar chart after removing the null values and grouping by brand name
result2 = result.dropna().groupby('Retail Branding',  as_index=False).mean()
fig2 = go.Figure([go.Bar(x=result2['Retail Branding'], y=result2['outgoing_mins_per_month'])])
fig2.update_layout(
    title='Minutes of usage per brand name (after removing unknown devices)',
    showlegend=True)

# create a pie chart to show data usage by brand name
fig3 = go.Figure([go.Pie(labels=result2['Retail Branding'], values=result2['monthly_mb'])])
fig3.update_layout(
    title='Monthly data usage per brand name (after removing unknown devices)',
    showlegend=True)

# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Joins and plotting"

# Set up the layout
app.layout = html.Div(children=[
    html.H1("Assignment 6 - Sage DS "),
    dcc.Graph(
        id='assignment6.1',
        figure=fig1
    ),
    dcc.Graph(
        id='assignment6.2',
        figure=fig2
    ),
    dcc.Graph(
        id='assignment6.3',
        figure=fig3
    ),
    html.A('Code on Github', href="https://github.com/pinaki-das-sage/assignment6"),
]
)

if __name__ == '__main__':
    app.run_server()
