#preprocessing

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

