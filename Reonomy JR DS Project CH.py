"""
Process:
I initially wanted to see what the data contained so I analyzed it in excel and I noticed some key inconsistencies. I noticed that the Manhattan was ÒManhattan, KSÓ. This was not what the assignment was looking for so I found that the dataset was using ÒNew York, NYÓ as Manhattan. I decided that was the best city to go with.
After importing my relevant packages into python, I needed to clean the data. I first viewed the unit of pay to understand if all the data was in the same unit. There were different units so I had to correct the data to all be yearly. Then I created a Manhattan and a San Francisco dataframe given the visa class H-1B.
I found the average of the wages in these dataframes.
I also found the max and standard deviation to help understand the data distribution.
I then plotted the data in a histogram and boxplot to help clearly show why the average was higher for one then the other. The only issue was that the data from NYC had some very large outliers that were skewing the data. I decided to look into the data without the outliers just so we can see the plots for Manhattan more clearly.
I can see from the boxplots that San Francisco has higher values for the quantiles and median which helps us to understand why the average value would be higher.
We can also see from the histograms that are displayed together that the SanFrancisco wages have higher counts (taller bars) in the higher wage values, showing that San Francisco have more higher wages than NYC which would help to pull its average up. The only thing that was pulling Manhattans average up was the fact that they had some outlier wages that were in the 100's of millions but it seems that without those outliers the data falls mostly around the $60,000 to $70,000 range.
I then preformed an anova test to determine if the means significantly differ from one another for the categories. Because the p-value was less than .05, the test returned a statistically significant result and therefore rejected the Null hypothesis that the means are equal.
"""


#%% Importing Libraries
# Basic Imports
import numpy as np
import pandas as pd
# Plotting
from matplotlib import pyplot
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Import data
df = pd.read_csv(r"C:\Users\tinah\Desktop\data_source.csv")

#determining the values that exist in the unit of pay column
df.pw_unit_of_pay.unique()

# Cleaning data because the units of prevailing wage are different
df.loc[df.pw_unit_of_pay == "Hour", 'prevailing_wage'] = (df.prevailing_wage * 40 * 52)
df.loc[df.pw_unit_of_pay == "Hour", 'pw_unit_of_pay'] = "Year"
df.loc[df.pw_unit_of_pay == "Week", 'prevailing_wage'] = (df.prevailing_wage * 52)
df.loc[df.pw_unit_of_pay == "Week", 'pw_unit_of_pay'] = "Year"
df.loc[df.pw_unit_of_pay == "Bi-Weekly", 'prevailing_wage'] = (df.prevailing_wage * 26)
df.loc[df.pw_unit_of_pay == "Bi-Weekly", 'pw_unit_of_pay'] = "Year"
df.loc[df.pw_unit_of_pay == "Montly", 'prevailing_wage'] = (df.prevailing_wage * 12)
df.loc[df.pw_unit_of_pay == "Monthly", 'pw_unit_of_pay'] = "Year"

#Viewing updated data
df[['prevailing_wage', 'pw_unit_of_pay']]

#validating
df.pw_unit_of_pay.unique()

# Understanding if the data has any important null values
print(df.isnull().sum())

# Creating a dataframe for Manhattan people and also having a visa class of H-1B
dfMan= df[(df['employer_city']=="NEW YORK") & (df['visa_class']=="H-1B")]
#creating a dataframe for san fran people and also having a visa class of H-1B
dfSan= df[(df['employer_city']=="SAN FRANCISCO") & (df['visa_class']=="H-1B")]

#finding the max value in prevailing wage
print("the max value for H-1B salaries in NYC is" , dfMan["prevailing_wage"].max())

#finding the mean value in prevailing wage
print("the mean value for H-1B salaries in NYC is" , dfMan["prevailing_wage"].mean())

#finding the SD in prevailing wage
print("the Standard Deviation for H-1B salaries in NYC is" ,dfMan["prevailing_wage"].std())

#finding the max value in prevailing wage
print("the max value for H-1B salaries in San Fran is" ,dfSan["prevailing_wage"].max())

#finding the mean value in prevailing wage
print("the mean value for H-1B salaries in San Fran is" ,dfSan["prevailing_wage"].mean())

#finding the SD in prevailing wage
print("the Standard Deviation for H-1B salaries in San Fran is" ,dfSan["prevailing_wage"].std())


#creating a new dataframe with both NYC and San Fran
df1= dfMan.append(dfSan)

#finding the mean value of the combined San Fran and NYC data
print("the mean value for H-1B salaries across both is" ,df1["prevailing_wage"].mean())

#Validating
df1.employer_city.unique()

# %% [markdown]
# Using a box plot to understand how the wage data varies for NYC
# We can see that Manhattan has a huge variation in its data because of these very large outliers


fig = px.box(dfMan, y="prevailing_wage", title= "Box Plot for NYC wages")
fig.show()



# The below histogram barely can show our data because it has become so right skewed because these outliers have given it a very long tailed look
fig = px.histogram(dfMan, x="prevailing_wage", title= "Histogram of Prevailing Wages for NYC")
fig.show()


# Boxplot of San Francisco
# This distribution of values looks much better than that of NYC

fig = px.box(dfSan, y="prevailing_wage", title= "San Francisco Box Plot of Wages")
fig.show()

# Below is a histogram of San Fran wages. The X axis is the wage and the Y axis is the count.
fig = px.histogram(dfSan, x="prevailing_wage", title= "Histogram of Prevailing Wages for San Francisco")
fig.show()

# The below scatterplot seems useless, we need to remove the outliers to get a clearer picture of the majority of our data
fig1 = px.scatter(df1, x="prevailing_wage", y="prevailing_wage", color= "employer_city")
fig1.show()

# I believe it is important to also analyze the data without the NYC outliers because it is clearly skewing our data. I created a dataframe without the outliers to

#Creating a dataframe with no outliers
Df_wo_outliers = df1[df1['prevailing_wage'] < 500000]



# Below is a histogram of both cities, we can clearly see that there are many more higher salaries for San Fran than for NYC. This can be seen looking at the prevelance of the red lines past 100,000 dollars. We can see that many of the values fall around the 60,000 dollar range for NYC, but because we have so many outliers in the NYC dataset, the salary get inflated and as we saw the mean salary increases. NYC still has a lower mean salary than San Fran because San Fran is consistent in its higher wage values with much less skew.

fig = px.histogram(Df_wo_outliers, x="prevailing_wage", color= "employer_city" )
fig.show()


# Below is a boxplot wih the outliers removed, we can clearly see that Q1, Median and Q3 are all much higher for San Fran than for NYC
fig = px.box(Df_wo_outliers, x="employer_city", y="prevailing_wage")
fig.show()


# Creating a dataframe to use for the anova test
df_anova= Df_wo_outliers[["employer_city", "prevailing_wage"]]

# Using an anova model to test difference among groups and difference between groups
# An anova model is used to test the differences in means of groups
# H0: ?1 = ?2
# H1: Means are not all equal

model = ols("prevailing_wage ~ C(employer_city)", df_anova).fit()
res = sm.stats.anova_lm(model, typ=1)
print(res)
# We can clearly see from the results that the difference in means is statistically significant, we will be rejecting the Null hypothesis






