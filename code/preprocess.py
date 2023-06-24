#preprocessing
import pandas as pd

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
    

    new_datafram = new_datafram[['Site','Time','Latency','Forecast max','Forecast min','Confidence Level','Volatility', 'Packet loss', 'Application type']]    
    
    return new_datafram

def filter_date(df):
    pass

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
    new_df = pd.DataFrame(zipped, columns=['Application type', 'Average latency', 'Average packet loss', 'Frequency'])
    new_df = new_df[new_df['Frequency'] > 0]
    return new_df