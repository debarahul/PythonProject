import pandas

dataframe_1 = pandas.read_csv('result.csv', delimiter='@')
dataframe_2 = pandas.read_csv('summary.csv', delimiter='@')
x="report"
y=".xlsx"
a="-"
#File=x+a+testplans+build+y
File=x+y
excel_writer = pandas.ExcelWriter(File, engine='xlsxwriter')
dataframe_2.to_excel(excel_writer,'Summary')
dataframe_1.to_excel(excel_writer,'TestCase Status')
excel_writer.save()

