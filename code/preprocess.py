#preprocessing
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go

def filter_groupby_time_city(df):
    '''
        Add forecasting value to data

        Args:
            dataframe: The dataframe to process
        Returns:
            only one total latency for each city per time
    '''
    # TODO : filter data by time and city and return filtered data
 
    # Group by 'city' and calculate average of 'age'
    new_datafram = df.groupby(['Site', 'Time']).mean().reset_index()
    
    new_datafram = new_datafram[['Site','Time','Latency','Forecast max','Forecast min','Confidence Level','Volatility']]    
    
    return new_datafram


#vis2
def filter_date(df, start_date, end_date):
    df['Time'] = pd.to_datetime(df['Time'])
    s = datetime(year=start_date.year, month=start_date.month, day=start_date.day, hour=0,minute=0,second=0)
    e = datetime(year=end_date.year, month=end_date.month, day=end_date.day, hour=22,minute=0,second=0)
    date_df = df.loc[(df['Time'] >= s) & (df['Time'] <= e)]
    return date_df

def filter_protocol(df, protocol):
    protocol_df = df.loc[df['Protocol'] == protocol]
    return protocol_df


def bubble_chart_df(df):
    df = df.reset_index()  # make sure indexes pair with number of rows

    application_type = ['Communication', 'Voice and File Transfer', 'Multimedia Streaming', 'Social Commerce', 'Network Management']
    frequency = [0]*len(application_type) # frequency of each application type
    sum_packet_loss = [0]*len(application_type)
    sum_latency = [0]*len(application_type)

    for index, row in df.iterrows():
        idx = application_type.index(row['Application type'])
        frequency[idx] = frequency[idx] + 1
        sum_packet_loss[idx] = sum_packet_loss[idx] + row['Packet loss']
        sum_latency[idx] = sum_latency[idx] + row['Latency']


    mean_packet_loss = []
    mean_latency = []
    for i in range(len(frequency)):
        if frequency[i] != 0:
            mean_packet_loss.append(round(sum_packet_loss[i] / frequency[i], 4)) # calculate the average packet loss for each application type
            mean_latency.append(round(sum_latency[i] / frequency[i], 2)) # calculate the average latency for each application type
        else:
            mean_packet_loss.append(0) 
            mean_latency.append(0) 

    zipped = list(zip(application_type, mean_latency, mean_packet_loss, frequency))
    bubble_df = pd.DataFrame(zipped, columns=['Application type', 'Average latency', 'Average packet loss', 'Frequency'])
    bubble_df = bubble_df[bubble_df['Frequency'] > 0]
    return bubble_df

def line_chart_df(df, application_type, s_date, e_date):
    date_df = filter_date(df, s_date, e_date)
    line_df = date_df.loc[date_df['Application type'] == application_type]
    return line_df

def bubble_select(df, start_date, end_date, protocol, clickedData): # understand which application type is selected
    application_type = ['Communication', 'Voice and File Transfer', 'Multimedia Streaming', 'Social Commerce', 'Network Management']

    if protocol == 'All':
        application_type_idx = clickedData['points'][0]['curveNumber']
        return application_type[application_type_idx]
    elif protocol != 'All':
        date_df = filter_date(df, start_date, end_date)
        protocol_df = filter_protocol(date_df, protocol)
        bubble_df = bubble_chart_df(protocol_df)
        for index, row in bubble_df.iterrows():
            if row['Frequency'] == clickedData['points'][0]['x'] and row['Average latency'] == clickedData['points'][0]['y'] and row['Average packet loss'] == clickedData['points'][0]['marker.size']:
                return row['Application type']
#viz_3
def to_df(data):
    # Convert JSON formatted data to dataframe
    return pd.json_normalize(data['features'])
def get_neighborhoods(data):
    return to_df(data)['properties.prov_name_en'].unique()





# Visual 1
###################################
def filter_by_Site(df):
    '''
        Retrieves all the data by protocol

        Args:
            dataframe: The dataframe to process
        Returns:
            Dictionnary of dataframe containing latency of each Site
    '''
  
    # TODO : Select the attributes we're interested in
    selected_attributes = ['Site', 'Time', 'Type','Protocol','Latency']
    df = df[selected_attributes]

    # Group by 'Site'
    unique_site = df['Site'].unique()
    data_per_city = dict()
    for city in unique_site:
      data_per_city[city] = df[df['Site'] == city]

    return(data_per_city)
    

def filter_by_type(df):
    '''
        Retrieves all the data by source type (whether from app or network )

        Args:
            dataframe: The dataframe to process
        Returns:
            Dictionnary of dataframe containing latency of each Type
    '''
  
    # TODO : Select the attributes we're interested in
    selected_attributes = [ 'Time','Type','Protocol','Latency']
    df = df[selected_attributes]

    # Group by 'Type'
    unique_type = df['Type'].unique()
    latency_per_type = dict()
    for Lat_Type in unique_type:
      latency_per_type[Lat_Type] = df[df['Type'] == Lat_Type]

    return(latency_per_type)


def filter_by_protocol(df):
    '''
        Retrieves all the data by protocol

        Args:
            dataframe: The dataframe to process
        Returns:
            Dictionnary of dataframe containing the list of latency for each protocol
    '''
  
    # TODO : Select the attributes we're interested in
    selected_attributes = ['Time','Protocol','Latency']
    df = df[selected_attributes]

    # Group by 'Type'
    unique_protocol = df['Type'].unique()
    latency_per_prot = dict()
    for Lat_protocol in unique_protocol:
      latency_per_prot[Lat_protocol] = df[df['Type'] == Lat_protocol]

    return(latency_per_prot)

def Protocol_to_df (dataframe):
  variables = dataframe['Protocol'].unique()
  Df_protocol = pd.DataFrame(columns=variables)
  for temps in dataframe['Time'].unique():
    df_values = dataframe[dataframe['Time']
                              == temps ]
    list_values = df_values['Latency'].tolist()
    # Add a new row using df.append
    new_row = pd.DataFrame([list_values], columns=Df_protocol.columns)
    Df_protocol = pd.concat([Df_protocol, new_row], ignore_index=True)
  return Df_protocol


# Fonction pour générer la figure d'une jauge
def generate_gauge_figure(value, variable,ref=0):
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={'text': variable},
            delta={'reference': ref,'increasing': {'color': 'red'}, 'decreasing': {'color': 'green'}},
            gauge={
                'axis': {'range': [None, 100]},
                    'bar': {'color': 'rgb(0, 128, 255)'},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': 'gray',
                    'steps': [
                        {'range': [0, value], 'color': 'rgb(0, 70, 140)'},
                        {'range': [value, 100], 'color': 'rgb(0, 128, 255)'}
                    ]
                
            }
        ),
        layout=go.Layout(
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            width=200,
            height=200
        ),
    )
#######################################################

#vis4

########################################################################################################
# A new table with proper rows and attributes was created to show the average latency in each site 
# per type in an animated line chart. Since we did not need the protocols in this visualization, 
# We removed these values from the dataset, 
# but each row of the table needed to be the average latency per site and by type, 
# so we created new rows with the required information, removed the extra attribute, 
# and combined these two datasets into a new data set that could be used for visualization 4.
# Args: dataframe: The dataframe to process
# Returns: new table for average latency per type in each site
# ######################################################################################################

def city_average_latency_type(df_viz4):
    pd.set_option('display.max_columns', None)
    print("df_viz4" , df_viz4)
    #df_viz4.drop(['Protocol', 'Latency'], axis=1, inplace=True)
    df_viz4 = df_viz4.groupby(['Site', 'Time', 'Type'], as_index=False)['Average Latency'].mean()


    app_df_viz4 = df_viz4[df_viz4['Type'] == 'app'].rename(columns={'Average Latency': 'app_Average_Latency'})
    network_df_viz4 = df_viz4[df_viz4['Type'] == 'network'].rename(columns={'Average Latency': 'network_Average_Latency'})
    df_viz4 = pd.merge(app_df_viz4, network_df_viz4, on=['Site', 'Time'], suffixes=('_app', '_network'))
    df_viz4.drop(['Type_network', 'Type_app'], axis=1, inplace=True)
    #df_viz4 = pd.DataFrame(df_viz4)
    return(df_viz4) 
