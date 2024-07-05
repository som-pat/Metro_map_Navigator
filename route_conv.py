import pandas as pd
routes = pd.read_csv('Dataset/routes.txt')


def seperator(route_long_name):
    # print(route_long_name)
    parts = route_long_name.split('_')
    if 'RAPID' in parts:
        parts[0] ='PURPLE'
    if 'ORANGE/AIRPORT' in parts:
        parts[0] ='ORANGE'
    if 'GRAY' in parts:
        parts[0] ='#0C0C0C'
    if 'YELLOW' in parts:
        parts[0] = '#750E21'
    if 'MAGENTA' in parts:
        parts[0] = '#720455'

    color = parts[0] if len(parts)>1 else None
    if 'to' in parts[-1]:
        rt = parts[-1].split(' to ')
        start_point = rt[0]
        end_point = rt[1]
    else:
        start_point=end_point=None
    
    return pd.Series([color,start_point,end_point])


routes[['route_color','start_point','end_point']] = routes['route_long_name'].apply(seperator)
routes = routes.sort_values(by=['route_color'])
print(routes['route_color'])
# path = r'Dataset/routes2.txt'
# with open(path, 'a') as f:
#     route_str = routes.to_string(index=False)
#     f.write(route_str)

routes.to_csv('Dataset/routes4.txt', header=True, index=None, sep=',', mode='a') # type: ignore