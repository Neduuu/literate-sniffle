# literate-sniffle
INTENTION:
a personal bot hosted on discord that does the following;
scrapes my school's website for my grades :
predicts the next grade for an assessment and/or a course final score
sends a plot of the assessment(s) of a course
tracks assessments days for reminder with ideal studying time
generates a progress report of semester/course:
. Course that needs improvements
. Scores needed to get desired grade
. average scores per assessment per course
. % lost/gained so far in a course
. projected grade letter
. and so on....

The predictions are done with the sklearn library specifically the linear regression model. My independent variables were:
. Assessment number(my reasoning was because assessments tend to get harder deeper into the semester regardless of effort put)
. and confidence level(i give the bot an honest confidence level(1-10) before i write an assessment). It is then put in a csv file as another independent variable.
the model is actively trained with my previous grades



