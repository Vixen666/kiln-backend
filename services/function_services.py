# function_services.py
class FunctionServices:
    def TemplateCurveService_SplitCurveData(self, data):
        return data
        interpolated_data = []
        
        for i in range(len(data) - 1):
            start_point = data[i]
            end_point = data[i + 1]
            
            start_time = start_point['time']
            end_time = end_point['time']
            start_temp = start_point['temperature']
            end_temp = end_point['temperature']
            
            time_interval = end_time
            temp_interval = end_temp - start_temp
            
            # Interpolate points between start and end
            interpolated_data.append(start_point)  # Add the start point
            for t in range(1, time_interval):
                interpolated_time = start_time + t
                interpolated_temp = start_temp + (temp_interval * (t / time_interval))
                interpolated_data.append({
                    'sequence': i*10+t,  # Interpolated points don't have a sequence number
                    'time': interpolated_time,
                    'temperature': interpolated_temp,
                    'burn_id': start_point['burn_id']
                })
            
        interpolated_data.append(data[-1])  # Add the last point
        #print(interpolated_data)
        return interpolated_data