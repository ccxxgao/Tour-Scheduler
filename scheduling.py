import csv
import pandas as pd
import numpy as np

def getAvailabilities(string):
    s = string.split(', ')
    avail = [0,0,0,0,0]
    for day in s:
        if day == 'Monday': avail[0] = 1
        elif day == 'Tuesday': avail[1] = 1
        elif day == 'Wednesday': avail[2] = 1
        elif day == 'Thursday': avail[3] = 1
        elif day == 'Friday': avail[4] = 1 
    return avail 

if __name__ == "__main__":
    A = pd.read_csv('availabilities.csv')
    A['days_available'] = A["When are you available for tours?"].apply(lambda x: getAvailabilities(x))
    A = A.drop(A.columns[[0,1,3,4,6,7]], axis=1)
    A['num_of_tours'] = 0
    A['Name'] = A['Name'].str.split(" ", n = 1, expand = True)
    A['gave_tour_this_week'] = 0
    # A['gave_tour_last_week'] = 0
    temp = A['days_available'].apply(pd.Series)
    weekdays = ['M', 'T', 'W', 'Th', 'F']
    temp.columns = weekdays
    A = A.join(temp, how='outer')
    A = A.join(pd.DataFrame(np.zeros((len(A), len(A)), dtype=int)), how='outer')
    A = A.drop(A.columns[2], axis=1)

    # assign head guides four tours each
    head_guides = [2, 5]
    # dict stores semester assignments 
    # week : [(g1, g2), (g1, g2)...]
    semester_assignments = {}

    for week in range(0, 11):
        A['gave_tour_this_week'] = 0
        semester_assignments[week] = []
        for day in weekdays:
            # get list of all indices of available guides on a given day
            available_guides = A[A[day]==1]

            # Remove guides unavailable that day
            date_val = '('+str(week)+','+str(weekdays.index(day))+')'
            for index, row in available_guides.iterrows():
                if date_val in str(row['Days_off']):
                    available_guides = available_guides.drop(index)

            # Remove head guides if they have given 3 tours
            for h in head_guides:
                if h in list(available_guides.index):
                    if A.iloc[h, A.columns.get_loc('num_of_tours')] == 4:
                        available_guides = available_guides.drop(h)
            assigned_guides = []
            curr_guide = -1

            # Select Guide 1
            while True:
                curr_guide = available_guides[available_guides.num_of_tours==available_guides.num_of_tours.min()]
                curr_guide = curr_guide[curr_guide.gave_tour_this_week==curr_guide.gave_tour_this_week.min()].sample(n=1)
                A.iloc[curr_guide.index[0], A.columns.get_loc('num_of_tours')] += 1
                A.iloc[curr_guide.index[0], A.columns.get_loc('gave_tour_this_week')] = 1
                assigned_guides.append(curr_guide.index[0])
                available_guides = available_guides.drop(curr_guide.index[0])
                break

            # Select guide 2
            while True:
                # get the remaining available guides in a list
                available_guides = available_guides[available_guides.num_of_tours==available_guides.num_of_tours.min()]
                available_guides = available_guides[available_guides.gave_tour_this_week==available_guides.gave_tour_this_week.min()]
                past_pairings = {}
                for option in list(available_guides.index):
                    past_pairings[option] = A.iloc[assigned_guides[0], A.columns.get_loc(option)]
                attempt = min(past_pairings, key=past_pairings.get)
                A.iloc[attempt, A.columns.get_loc('num_of_tours')] += 1
                A.iloc[attempt, A.columns.get_loc('gave_tour_this_week')] = 1
                assigned_guides.append(attempt)
                break
                
            # add 1 to both guides' paired w/
            A.iloc[assigned_guides[0], A.columns.get_loc(assigned_guides[1])] += 1
            A.iloc[assigned_guides[1], A.columns.get_loc(assigned_guides[0])] += 1
            guides = []
            for g in assigned_guides:
                guides.append(A.iloc[g, A.columns.get_loc('Name')])
            semester_assignments[week].append(guides)             
    

    for key, val in semester_assignments.items():
        print("Week ", key, ": ", val)
    print(A)