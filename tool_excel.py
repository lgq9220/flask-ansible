import xlrd
import tool_db
def insertFromExcel( excelPath ):
    book = xlrd.open_workbook( excelPath )
    sheet = book.sheet_by_index(0)
    rowsnumber = sheet.nrows
    colsnumber = sheet.ncols
    for i in range(0, rowsnumber):
        value = []
        for j in range(0, colsnumber):
            value.append(sheet.cell(i, j).value)
        if i != 0:
            sql = 'replace into servers (name,ip, port, user) VALUES( %s, %s, %s, %s);'
            tool_db.updateByParameters( sql, (value[0],value[1], value[2], value[3] ) )

if __name__ == "__main__":
    insertFromExcel('/soft/flask/learn008/static/servers.xlsx')