import itertools
import re
import scipy.linalg as spla
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


dataFrame = pd.read_csv(r"C:\Users\matth\Documents\Atom\397A Homeworks\Homeworks\homework3\responses_clean.csv")

response_tally = {}

q1_responses = dataFrame.Q1
q2_responses = dataFrame.Q2
q3_responses = dataFrame.Q3
q4_responses = dataFrame.Q4
q4_text_responses = dataFrame.Q4_text

for response in q1_responses:
    if(response in response_tally):
        response_tally[response] += 1
    else:
        response_tally[response] = 1


decrease_reasons = {}
increase_reasons = {}


for (change, reason_decrease, reason_increase) in zip(q1_responses, q2_responses, q3_responses):

    if(change == 'Slightly higher') or (change == 'Much higher'):

        if(reason_increase != 'Both'):

            if(reason_increase in increase_reasons):
                increase_reasons[reason_increase] += 1
            else:
                increase_reasons[reason_increase] = 1

        else:

            increase_reasons['Income increase due to COVID-19 related stimulus payment'] += 1
            increase_reasons['Buying products out of boredom'] += 1

    if(change == 'Slightly lower') or (change == 'Much lower'):

        if(reason_decrease != 'Both'):

            if(reason_decrease in decrease_reasons):
                decrease_reasons[reason_decrease] += 1
            else:
                decrease_reasons[reason_decrease] = 1
        else:
            decrease_reasons['Financial Constraints (Unemployment, increased healthcare costs, etc.)'] += 1
            decrease_reasons['Lockdown Orders (Reduced access to retail outlets, restaurants, etc.)'] += 1


total_stims = {
                "Stimulus Check" : 0,
                "Pandemic Unemployment Assistance" : 0,
                "Paycheck Protection Program" : 0,
                "University Aid" : 0,
                "I have not received any COVID-19 related government financial assistance" : 0
                }

decrease_stims = {
                    "Stimulus Check" : 0,
                    "Pandemic Unemployment Assistance" : 0,
                    "Paycheck Protection Program" : 0,
                    "University Aid" : 0,
                    "I have not received any COVID-19 related government financial assistance" : 0
                }
increase_stims = {
                    "Stimulus Check" : 0,
                    "Pandemic Unemployment Assistance" : 0,
                    "Paycheck Protection Program" : 0,
                    "University Aid" : 0,
                    "I have not received any COVID-19 related government financial assistance" : 0
                }

combo_same_stims = {
                        "Stimulus Check" : 0, #"Stimulus Check (SC)" : 0,
                        "Pandemic Unemployment Assistance" : 0,
                        "Paycheck Protection Program" : 0,
                        "University Aid" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance" : 0,
                        "Stimulus Check,Paycheck Protection Program" : 0,
                        "Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "I have not received any COVID-19 related government financial assistance" : 0
                        }

combo_decrease_stims = {
                        "Stimulus Check" : 0, #"Stimulus Check (SC)" : 0,
                        "Pandemic Unemployment Assistance" : 0,
                        "Paycheck Protection Program" : 0,
                        "University Aid" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance" : 0,
                        "Stimulus Check,Paycheck Protection Program" : 0,
                        "Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "I have not received any COVID-19 related government financial assistance" : 0
                        }

combo_increase_stims = {
                        "Stimulus Check" : 0, #"Stimulus Check (SC)" : 0,
                        "Pandemic Unemployment Assistance" : 0,
                        "Paycheck Protection Program" : 0,
                        "University Aid" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance" : 0,
                        "Stimulus Check,Paycheck Protection Program" : 0,
                        "Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "I have not received any COVID-19 related government financial assistance" : 0
                        }

combo_total_stims = {
                        "Stimulus Check" : 0, #"Stimulus Check (SC)" : 0,
                        "Pandemic Unemployment Assistance" : 0,
                        "Paycheck Protection Program" : 0,
                        "University Aid" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance" : 0,
                        "Stimulus Check,Paycheck Protection Program" : 0,
                        "Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "Stimulus Check,Pandemic Unemployment Assistance,Paycheck Protection Program" : 0,
                        "I have not received any COVID-19 related government financial assistance" : 0
                        }
same_count = 0
incr_count = 0
decr_count = 0
incr_same_count = 0

""" These variables represent the number of respondents that said they
    changed their spending, given they receieved some form of government
    assistance"""
same_while_stimmed = 0
incr_while_stimmed = 0
decr_while_stimmed = 0
incr_same_while_stimmed = 0

for (change, stims_recieved, other_stims) in zip(q1_responses, q4_responses, q4_text_responses):
    combo_total_stims[stims_recieved] += 1

    if(change == "About the same"):
        combo_same_stims[stims_recieved] += 1
        same_count += 1
        incr_same_count += 1
        if(stims_recieved != "I have not received any COVID-19 related government financial assistance"):
            same_while_stimmed += 1
            incr_same_while_stimmed += 1


    if(change == 'Slightly higher') or (change == 'Much higher'):
        incr_count += 1
        incr_same_count += 1
        combo_increase_stims[stims_recieved] += 1

        stims = stims_recieved
        if("I have not received any COVID-19 related government financial assistance" in stims_recieved):

            decrease_stims['I have not received any COVID-19 related government financial assistance'] += 1
            total_stims['I have not received any COVID-19 related government financial assistance'] += 1

        else:
            incr_while_stimmed += 1
            incr_same_while_stimmed += 1
            if("Stimulus Check" in stims_recieved):

                decrease_stims['Stimulus Check'] += 1
                total_stims['Stimulus Check'] += 1


            if("Pandemic Unemployment Assistance" in stims_recieved):

                decrease_stims['Pandemic Unemployment Assistance'] += 1
                total_stims['Pandemic Unemployment Assistance'] += 1

            if("Paycheck Protection Program" in stims_recieved):

                decrease_stims['Paycheck Protection Program'] += 1
                total_stims['Paycheck Protection Program'] += 1

            if("University Aid" in stims_recieved):

                decrease_stims['University Aid'] += 1
                total_stims['University Aid'] += 1

    if(change == 'Slightly lower') or (change == 'Much lower'):
        decr_count += 1
        combo_decrease_stims[stims_recieved] += 1
        stims = stims_recieved

        if("I have not received any COVID-19 related government financial assistance" in stims_recieved):

            increase_stims['I have not received any COVID-19 related government financial assistance'] += 1
            total_stims['I have not received any COVID-19 related government financial assistance'] += 1

        else:
            decr_while_stimmed += 1
            if("Stimulus Check" in stims_recieved):

                increase_stims['Stimulus Check'] += 1
                total_stims['Stimulus Check'] += 1

            if("Pandemic Unemployment Assistance" in stims_recieved):

                increase_stims['Pandemic Unemployment Assistance'] += 1
                total_stims['Pandemic Unemployment Assistance'] += 1

            if("Paycheck Protection Program" in stims_recieved):

                increase_stims['Paycheck Protection Program'] += 1
                total_stims['Paycheck Protection Program'] += 1

            if("University Aid" in stims_recieved):

                decrease_stims['University Aid'] += 1
                total_stims['University Aid'] += 1


""" Convert Qualitative Answers to Quanitative """

q1_responses_as_int = []
q1_counts = {}

for response in q1_responses:
    value = 0
    if(response == 'Much higher'):
        value = 2
        if('Much Higher' in q1_counts):
            q1_counts['Much Higher'] += 1
        else:
            q1_counts['Much Higher'] = 1
    if(response == 'Slightly higher'):
        value = 2
        if('Slightly higher' in q1_counts):
            q1_counts['Slightly higher'] += 1
        else:
            q1_counts['Slightly higher'] = 1
    if(response == 'About the same'):
        value = 1
        if('About the same' in q1_counts):
            q1_counts['About the same'] += 1
        else:
            q1_counts['About the same'] = 1
    if(response == 'Slightly lower'):
        value = 0
        if('Slightly lower' in q1_counts):
            q1_counts['Slightly lower'] += 1
        else:
            q1_counts['Slightly lower'] = 1
    if(response == 'Much lower'):
        value = 0
        if('Much lower' in q1_counts):
            q1_counts['Much lower'] += 1
        else:
            q1_counts['Much lower'] = 1
    q1_responses_as_int.append(value)


to_be_coded = pd.DataFrame()
print(q1_counts)
to_be_coded["q2"] = q2_responses
to_be_coded["q3"] = q3_responses













q3_responses_as_ints = []

q4_responses_as_ints = []



for response in q4_responses:
    value = 0
    if("," in response):
        value = 2

    if(response == 'Paycheck Protection Program') or (response == 'Pandemic Unemployment Assistance'):
        value = 2

    if(response == 'Stimulus Check'):
        value = 1

    if(response == 'I have not received any COVID-19 related government financial assistance'):
        value = 0

    q4_responses_as_ints.append(value)




first_test = pd.DataFrame()
first_test["q1"] = q1_responses_as_int
first_test["q4"] = q4_responses_as_ints

kmean = KMeans(n_clusters=4)
kmean.fit(first_test)
labels = kmean.predict(first_test)



cluster_tally = {}

for element in labels:
    if(element in cluster_tally):
        cluster_tally[element] += 1
    else:
        cluster_tally[element] = 1

stats_in_clusters = {}

q4_counts = {}

for cluster in cluster_tally.keys():
    stats_in_clusters[cluster] = {}
    #stats_in_clusters[cluster]["Changes"] = {}
    #stats_in_clusters[cluster]["Stims"] = {}

stim_list = []

for change, stim, cluster in zip(q1_responses, q4_responses, labels):

        key = change + "; " + stim

        if("," in stim):

            key = change + "; " + "Combo Payments"
            stim_list.append("Combo Payment")
            if('Combo Payment' in q4_counts):
                q4_counts['Combo Payment'] += 1
            else:
                q4_counts['Combo Payment'] = 1
        else:
            if("I have not received any COVID-19 related government financial assistance" in stim):

                key = change + "; " + "No Aid"
                stim_list.append("No Aid")
                if('No Aid' in q4_counts):
                    q4_counts['No Aid'] += 1
                else:
                    q4_counts['No Aid'] = 1
            else:

                if("Stimulus Check" in stim):

                    key = change + "; " + "One Time Payment"
                    stim_list.append("One Time Payment")
                    if('One-Time Payment' in q4_counts):
                        q4_counts['One-Time Payment'] += 1
                    else:
                        q4_counts['One-Time Payment'] = 1
                else:

                    if("Pandemic Unemployment Assistance" in key) or ("Paycheck Protection Program" in key) or ("University Aid" in key):

                        key = change + "; " + "Recurring Payments"
                        stim_list.append("Recurring Payment")
                        if('Recurring Payments' in q4_counts):
                            q4_counts['Recurring Payments'] += 1
                        else:
                            q4_counts['Recurring Payments'] = 1







        if(key in stats_in_clusters[cluster]):
            stats_in_clusters[cluster][key] = stats_in_clusters[cluster][key] + 1
        else:
            stats_in_clusters[cluster][key] = 1

        if(key in stats_in_clusters[cluster]):
            stats_in_clusters[cluster][key] = stats_in_clusters[cluster][key] + 1
        else:
            stats_in_clusters[cluster][key] = 1



print(q4_counts)

distri_counts = {}

for change in q1_responses:
    distri_counts[change] = {}

reason_to_int_dict = {}
index = 0



change_list = []
reason_list = []

for change, reasonDecr, reasonIncr in zip(q1_responses, q2_responses, q3_responses):




    if(change != "About the same"):
        if(change == "Much higher") or (change == "Slightly higher"):
            if(reasonIncr in reason_to_int_dict):
                print("working")
            else:
                reason_to_int_dict[reasonIncr] = index
                index += 1
            change_list.append("Increase")
            reason_list.append(reason_to_int_dict[reasonIncr])

            if(reasonIncr in distri_counts[change]):
                distri_counts[change][reasonIncr] += 1
            else:
                distri_counts[change][reasonIncr] = 1
        else:
            if(reasonDecr in reason_to_int_dict):
                print("working")
            else:
                reason_to_int_dict[reasonDecr] = index
                index += 1
            change_list.append("Decrease")
            reason_list.append(reason_to_int_dict[reasonDecr])
            if(reasonDecr in distri_counts[change]):
                distri_counts[change][reasonDecr] += 1
            else:
                distri_counts[change][reasonDecr] = 1
    else:
        if("Same" in reason_to_int_dict):
            print("working")
        else:
            reason_to_int_dict['Same'] = index
            index += 1
        change_list.append("Same")
        reason_list.append(reason_to_int_dict['Same'])
        if("same" in distri_counts[change]):
            distri_counts[change]["same"] += 1
        else:
            distri_counts[change]["same"] = 1

print("distri",distri_counts)
print("change_list", change_list)
print("     ", q1_responses_as_int)
print("reason_list", reason_list)

print("target_list", q4_responses_as_ints)

change_list_float = q1_responses_as_int

stim_list_float = q4_responses_as_ints

age_list = []
age_int_dict = {}
age_index = 0

for response in dataFrame.Q37:
    if(response in age_int_dict):
        print("working")
    else:
        age_int_dict[response] = age_index
        age_index += 1
    age_list.append(age_int_dict[response])

income_list = []
income_int_dict = {}
income_index = 0

for response in dataFrame.Q38:
    if(response in income_int_dict):
        print("working")
    else:
        income_int_dict[response] = income_index
        income_index += 1
    income_list.append(income_int_dict[response])


education_list = []
education_int_dict = {}
education_index = 0

for response in dataFrame.Q38:
    if(response in education_int_dict):
        print("working")
    else:
        education_int_dict[response] = education_index
        education_index += 1
    education_list.append(education_int_dict[response])

le = preprocessing.LabelEncoder()

to_be_coded = pd.DataFrame()
to_be_coded["reason"] = reason_list

coded = to_be_coded.apply(le.fit_transform)
#coded["q1"] = pd.DataFrame(q1_responses_as_int)


enc = preprocessing.OneHotEncoder()
enc.fit(coded)

onehotlabels = enc.transform(coded).toarray()
onehotlabels.shape

one_coded = pd.DataFrame(onehotlabels)
print(one_coded)

data = one_coded
data["stim"] = q1_responses_as_int
data["age"] = age_list
#   data["income"] = income_list
data["education"] = education_list
print(age_list)

targets = q4_responses_as_ints
print("data",data)
print("target",targets)

data_train,data_test,target_train,target_test = train_test_split(data,targets,test_size=0.2,random_state=9)

classifier = GaussianNB()
classifier.fit(data_train, target_train)

target_prediction = classifier.predict(data_test) # store the prediction data
score = accuracy_score(target_test,target_prediction)
print(score)
