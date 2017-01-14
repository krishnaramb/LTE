#This script takes the xls file as input, it copies the same file and perform some regular expression replacement in the particular row and saves with the other file name
#in the xls format. Useful when dealing with mass changes of a particular items


from xlrd import open_workbook
#import xlrd
#from xlwt import Workbook
from xlutils.copy import copy
import re

#Find and replace using re.sub(): find MeasReport-5-L-1 and replace it with MeasReport-8-L-1

class ExlGen (object):
	def __init__(self,file_name):
		self.file_name = file_name
		

	def ExlCopy(self):
		self.rb = open_workbook(self.file_name)
		self.wb = copy(self.rb)
		return self.rb, self.wb





def MatchStrList(FileName,wb,rb_sheet,wb_sheet,row_start,row_end,column_req):
	matched_str = []
	for row_no in range(row_start,row_end+1):
		string = rb_sheet.cell(row_no, column_req ).value
		#print(string)
		#string = sheet.cell_value(row_no,column_req)
		match = re.sub("@sub_loop_count\s*=\s*\(.*?\)","@sub_loop_count=(\"None\",8)",string)
		#print(match)
		wb_sheet.write(row_no,column_req,match)

	wb.save("output.xls")

	
def WriteToWorkBook(scenario):
	wb = openpyxl.Workbook()
	ws2 = wb.create_sheet(title="L_G_2DLCA")
	for index, value  in enumerate (scenario):
		ws2.cell(column = 2, row = index+1, value = value)
	wb.save(filename = "Lorezno_feb8_MODIFIED_11.xlsx")


if __name__ == '__main__':
	WorkBookName = 'L0_L4_DuallSIM_DSDS_L_G_3GPP_Combined_new.xls'
	scenario = ExlGen(WorkBookName) 
	rb,wb = scenario.ExlCopy()
	wb_sheet = wb.get_sheet(1)
	rb_sheet = rb.sheet_by_name("Job Details")
	print(rb_sheet)
	#print(wb_sheet)
	#sheet.cell_value(0,0)
	#num_rows = sheet.ncols
	MatchStrList(WorkBookName,wb,rb_sheet,wb_sheet,9,134,8)
	
	


