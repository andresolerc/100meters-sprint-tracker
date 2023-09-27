import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import requests


# Title of the app
st.title('Sprint Performance Analyzer')

# Sidebar for User Input
st.sidebar.title('User Input')

# User Input for the number of sets in the sidebar
num_sets = st.sidebar.number_input('How many sets of sprints did you do?', min_value=1, max_value=50, value=10)

# User Input for each set time in the sidebar
st.sidebar.write('Please enter the time taken for each 100-meter sprint:')
sprint_times = []
for i in range(num_sets):
    time = st.sidebar.number_input(f'Set {i+1} time (seconds):', min_value=0.1, max_value=600.0)
    sprint_times.append(time)

# Calculate Speed (Speed = Distance/Time; Distance = 100 meters)
if len(sprint_times) > 0:
    speeds_ms = [100.0 / time if time != 0 else 0 for time in sprint_times]  # Speed in m/s
    speeds_kmh = [speed * 3.6 for speed in speeds_ms]  # Speed in km/h

    # Estimate VO2 Max (example estimation; for demonstration purposes)
    vo2_max = np.mean([speed * 3.1 for speed in speeds_ms])
    
    # Calculate Pacing Strategy
    pacing_std_dev = np.std(speeds_ms)
    
    # Fatigue Index (Speed drop from first to last set)
    if speeds_ms[0] != 0:
        fatigue_index = ((speeds_ms[0] - speeds_ms[-1]) / speeds_ms[0]) * 100
    

    # Create a DataFrame to Display Data
    df = pd.DataFrame({
        'Set': np.arange(1, len(sprint_times) + 1),
        'Time (s)': sprint_times,
        'Speed (m/s)': speeds_ms,
        'Speed (km/h)': speeds_kmh
    })
    st.dataframe(df)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Set'], df['Speed (m/s)'], marker='o', label='Speed (m/s)')
    ax.plot(df['Set'], df['Speed (km/h)'], marker='x', label='Speed (km/h)')
    ax.set_xlabel('Set')
    ax.set_ylabel('Speed')
    ax.set_title('Speed Across Sets')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Average Speed
    avg_speed_ms = np.mean([speed for speed in speeds_ms if speed != 0])
    avg_speed_kmh = avg_speed_ms * 3.6
    st.write(f'Your average speed is: {avg_speed_ms:.2f} m/s or {avg_speed_kmh:.2f} km/h')
    st.subheader('Interesting Speed Observation')
    st.write(f"Your average speed was **{avg_speed_kmh:.2f} km/h**. To put that in perspective, the fastest land animal, the cheetah, reaches speeds up to 100 km/h. Fastest 100m Sprint (Men): Usain Bolt holds the record with a time of 9.58 seconds, achieved in 2009. His top speed was approximately 44.72 km/h. Fastest 100m Sprint (Women): Florence Griffith-Joyner set the record with a time of 10.49 seconds in 1988. You're on your way to breaking your own records! Keep pushing!")
 
    # Show Advanced Metrics
    st.subheader('Advanced Metrics')
    
    st.write(f'**Estimated VO2 Max: {vo2_max:.2f} ml/kg/min**')
    st.write("VO2 Max represents your body's ability to utilize oxygen during intense exercise. A higher value indicates better cardiovascular fitness and endurance. This is an estimation and can serve as a baseline to monitor your aerobic improvements.")
    
    st.write(f'**Pacing Consistency (Std Dev): {pacing_std_dev:.2f} m/s**')
    st.write("The standard deviation in your speed across sets indicates your pacing consistency. A lower number suggests you're maintaining a consistent pace, key for optimal performance. A high number means you may benefit from a more even pace.")
    
    st.write(f'**Fatigue Index: {fatigue_index:.2f}%**')
    st.write("The Fatigue Index calculates the drop in your speed from your first to your last set, as a percentage. A lower percentage indicates better endurance and less fatigue. A high number means you may need to focus on stamina and recovery.")

    # Calculate Acceleration Phase
    if len(speeds_kmh) >= 2:
        acceleration_phase = speeds_kmh[1] - speeds_kmh[0]
        st.write(f'**Acceleration Phase: {acceleration_phase:.2f} km/h difference between first and second sets**')
        st.write("The acceleration phase is crucial in any sprint. It's where you generate the momentum you'll carry through the rest of the race. Your change in speed between the first and second sets gives an insight into your acceleration abilities.")

    # Calculate estimated Reaction Time
    reaction_time = sprint_times[0] - min(sprint_times)
    st.write(f'**Estimated Reaction Time: {reaction_time:.2f} seconds**')
    st.write('Knowing how quickly you reach your top speed can give you an idea of your reaction time.')
    # Display elite sprinter's reaction time
    elite_reaction_time = 0.18  # average reaction time of an elite sprinter in seconds
    st.write(f"**Elite Sprinter's Reaction Time: {elite_reaction_time:.2f} seconds**")
    st.write("The reaction time of elite sprinters is typically around 0.15 to 0.20 seconds.")


    # Calculate Cadence (estimated)
    cadence = 60 / 1.2  # 1.2 seconds per stride is a made-up constant for this example
    st.write(f'**Estimated Cadence: {cadence:.2f} steps/minute**')
    st.write('Cadence measures how many steps you take per minute. A higher cadence often correlates with better performance.')
    # Display elite sprinter's cadence
    elite_cadence = 270  # average cadence of an elite sprinter in steps/minute
    st.write(f"**Elite Sprinter's Cadence: {elite_cadence} steps/minute**")
    st.write("Cadence measures how many steps you take per minute. Elite sprinters usually have a cadence of around 260-280 steps/minute.")

    # Estimated Optimal Stride Length
    stride_length = 100 / (sprint_times[0] / 1.2)  # 100 meters and 1.2 seconds per stride
    st.write(f'**Estimated Optimal Stride Length: {stride_length:.2f} meters**')
    st.write('Your stride length, combined with your cadence, determines your speed.')
    # Stride Length based on leg length (for this example, let's assume a leg length of 1 meter)
    leg_length = 1.0  # in meters
    optimal_stride_length = leg_length * 1.1  # A research-based multiplier
    st.write(f"**Optimal Stride Length: {optimal_stride_length:.2f} meters**")
    st.write("Optimal stride length is often around 1.1 times your leg length.")

    # Calculate estimated Energy Expenditure
    energy_expenditure = np.mean(speeds_kmh) * 3.6  # An arbitrary constant for demonstration
    st.write(f'**Estimated Energy Expenditure: {energy_expenditure:.2f} kcal**')
    st.write("Knowing how much energy you're expending can help you manage your efforts better.")
    # Calculate estimated Energy Expenditure
    total_distance = 100 * len(sprint_times)  # 100 meters per set
    energy_expenditure = total_distance * 0.2  # 0.2 calories burned per meter
    st.write(f"**Estimated Energy Expenditure: {energy_expenditure:.2f} kcal**")
    st.write("An average adult may burn approximately 0.2 calories per meter during a sprint.")

    # Estimated Wind Resistance
    drag_coefficient = 0.9  # A made-up constant
    wind_resistance = drag_coefficient * np.mean(speeds_kmh)  # A simplistic formula
    st.write(f'**Estimated Wind Resistance: {wind_resistance:.2f} N (Newtons)**')
    st.write('Understanding the effects of wind resistance can offer insights into why you might be slower or faster on particular days.')

    # Create a DataFrame for Advanced Metrics Comparison
    advanced_metrics_df = pd.DataFrame({
        'Metric': ['VO2 Max (ml/kg/min)', 'Pacing Consistency (Std Dev, m/s)', 'Fatigue Index (%)', 'Reaction Time (s)', 'Cadence (steps/min)', 'Optimal Stride Length (m)', 'Energy Expenditure (kcal)', 'Wind Resistance (N)'],
        'Your Value': [vo2_max, pacing_std_dev, fatigue_index, reaction_time, cadence, stride_length, energy_expenditure, wind_resistance],
        'Olympian Benchmark': [' Male 85, Female 77 ', '< 0.2', '< 5%', '0.15-0.20', '260-280', 'Depends on leg length', 'Varies', 'Minimal']
    })

    # Display the DataFrame as a table in Streamlit
    st.table(advanced_metrics_df)