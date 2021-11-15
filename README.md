# literate-sniffle
INTENTION:
a personal bot hosted on discord that does the following;\n
scrapes my school's website for my grades :\n
predicts the next grade for an assessment and/or a course final score\n
sends a plot of the assessment(s) of a course\n
tracks assessments days for reminder with ideal studying time\n
generates a progress report of semester/course:\n
. Course that needs improvements\n
. Scores needed to get desired grade\n
. average scores per assessment per course\n
. % lost/gained so far in a course\n
. projected grade letter\n
. and so on....\n
\n
The predictions are done with the sklearn library specifically the linear regression model. My independent variables were:\n
. Assessment number(my reasoning was because assessments tend to get harder deeper into the semester regardless of effort put)\n
. and confidence level(i give the bot an honest confidence level(1-10) before i write an assessment). It is then put in a csv file as another independent variable.\n
the model is actively trained with my previous grades\n



