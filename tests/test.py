result = []
with open('D:\Projects\stocker\logs\startup.log') as f:
    lines = f.readlines()
    for line in lines:
        r = line.split('||')
        result.append({'timestamp': r[0], 'level': r[1], 'filename': r[2],
                       'funcName': r[3], 'lineno': r[4], 'message': r[5]})

print(result)
