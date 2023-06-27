#preprocessing
import pandas as pd
from datetime import datetime

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

    application_type = ['Communication', 'Voice and File Transfe', 'Multimedia Streaming', 'Social Commerce', 'Network Management']
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
            mean_packet_loss.append(sum_packet_loss[i] / frequency[i]) # calculate the average packet loss for each application type
            mean_latency.append(sum_latency[i] / frequency[i]) # calculate the average latency for each application type
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
    application_type = ['Communication', 'Voice and File Transfe', 'Multimedia Streaming', 'Social Commerce', 'Network Management']

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



# Preprocess for Visual 1
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

#######################################################

#vis4
'''
        Retrieves all the data by protocol

        Args:
            dataframe: The dataframe to process
        Returns:
            Dictionnary of dataframe containing latency of each Site
    '''
def city_average_latency_type(df_viz4):
    print("df_viz4" , df_viz4)
    df_viz4.drop(['Protocol', 'Latency'], axis=1, inplace=True)
    df_viz4 = df_viz4.groupby(['Site', 'Time', 'Type'], as_index=False)['Average Latency'].mean()


    app_df_viz4 = df_viz4[df_viz4['Type'] == 'app'].rename(columns={'Average Latency': 'app_Average_Latency'})
    network_df_viz4 = df_viz4[df_viz4['Type'] == 'network'].rename(columns={'Average Latency': 'network_Average_Latency'})
    df_viz4 = pd.merge(app_df_viz4, network_df_viz4, on=['Site', 'Time'], suffixes=('_app', '_network'))
    df_viz4.drop(['Type_network', 'Type_app'], axis=1, inplace=True)
    #df_viz4 = pd.DataFrame(df_viz4)
    return(df_viz4) 