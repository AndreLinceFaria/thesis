import xlsxwriter as xs
import os
import mining.algorithms.mlearning.persist as p

dir = os.path.dirname(__file__)
base_dir = os.path.join(dir,"report-files/")


class XlsxReport():
    def __init__(self, base_name = "execution_report"):
        self.base_name = base_name
        self.report_name = os.path.join(base_dir,self.base_name) + "-" \
                           + str(len(p.get_files_from_dir(os.path.join(base_dir, self.base_name))[0])) + ".xlsx"
        self.wb = xs.Workbook(self.report_name)
        self.current_ws = None

    def add_sheet(self, name=None):
        self.current_ws = self.wb.add_worksheet(name)

    def write_data(self, list_data):
        if all(isinstance(elem, list) for elem in list_data):
            for lst in list_data:
                row = 0
                col = 0
                for entry in lst:
                    self.current_ws.write(row,col, str(entry))
                    col += 1
                row+=1
        else:
            raise Warning("No content written to xlsx file. Incorrect data format.")

    def save(self):
        self.wb.close()



if __name__ == "__main__":
    print("DIR: " + dir)
    print("BASE_DIR: " + base_dir)

    data1 = [['ola','hello','salut']]
    data2 = [['ola','hello','salut'],['adeus','goodbye','au revoir']]
    data3 = ['ola','hello','salut'] #must rase warning

    xs = XlsxReport()
    print("FNAME: " + xs.report_name)

    xs.add_sheet()
    xs.write_data(data1)
    xs.add_sheet()
    xs.write_data(data2)
    xs.add_sheet()
    try:
        xs.write_data(data3)
    except Warning as e:
        print e

    xs.save()
