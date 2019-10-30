import xlwt

from common.utils.general import SysUtils


class XlsUtils:
    @staticmethod
    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式

        font = xlwt.Font()  # 为样式创建字体
        # 字体类型：比如宋体、仿宋也可以是汉仪瘦金书繁
        font.name = name
        font.bold = bold
        # 设置字体颜色
        font.colour_index = 17
        # 字体大小
        font.height = height
        # 定义格式
        style.font = font

        border_color = 1
        # borders.left = xlwt.Borders.THIN
        # NO_LINE： 官方代码中NO_LINE所表示的值为0，没有边框
        # THIN： 官方代码中THIN所表示的值为1，边框为实线
        borders = xlwt.Borders()
        borders.left = border_color
        borders.left = xlwt.Borders.THIN
        borders.right = border_color
        borders.top = border_color
        borders.bottom = border_color

        # 定义格式
        style.borders = borders
        return style

    @staticmethod
    def init_cols(sheet, col_params):
        style_header = XlsUtils.set_style('Times New Roman', 320, True)
        tall_style = xlwt.easyxf('font:height 600;')
        sheet.row(0).set_style(tall_style)
        index = 0
        for col_param in col_params:
            sheet.write(0, index, col_param[0], style_header)
            col = sheet.col(index)
            col.width = col_param[1] * 256
            index += 1
        return

    @staticmethod
    def write_sheet_old(file_name, data):
        # 创建工作簿
        book = xlwt.Workbook()
        # 创建工作表单
        sheet = book.add_sheet('漏洞特征库', cell_overwrite_ok=True)
        # 初始化表头
        col_params = [['漏洞编号', 14], ['描述', 80], ['贡献者', 30], ['贡献者编号', 18], ['类型', 20], ['类型编号', 14],
                      ['平台', 20], ['平台编号', 14], ['发布时间', 26], ]
        XlsUtils.init_cols(sheet, col_params)
        # 数据为空时，保存无数据的空表文件，返回
        if not isinstance(data, list) or len(data) == 0:
            book.save(file_name)
            return

        row = 1
        cell_style = XlsUtils.set_style('Times New Roman', 280, False)
        for item in data:
            sheet.write(row, 0, item['edb_id'], cell_style)
            sheet.write(row, 1, item['description'][1], cell_style)
            sheet.write(row, 2, item['author']['name'], cell_style)
            sheet.write(row, 3, item['author']['id'], cell_style)
            sheet.write(row, 4, item['type']['name'], cell_style)
            sheet.write(row, 5, item['type']['id'], cell_style)
            sheet.write(row, 6, item['platform']['platform'], cell_style)
            sheet.write(row, 7, item['platform']['id'], cell_style)
            sheet.write(row, 8, item['date_published'], cell_style)
            row += 1
        book.save(file_name)
        return

    @staticmethod
    def write_sheet(file_name, data, start_index):
        # 创建工作簿
        book = xlwt.Workbook()
        # 创建工作表单
        sheet = book.add_sheet('漏洞特征库', cell_overwrite_ok=True)
        # 初始化表头
        col_params = [['序号', 14], ['漏洞编号', 14], ['漏洞名称', 80], ['发布者', 30], ['漏洞类型', 20],
                      ['平台', 20], ['发布时间', 26], ]
        XlsUtils.init_cols(sheet, col_params)
        # 数据为空时，保存无数据的空表文件，返回
        if not isinstance(data, list) or len(data) == 0:
            book.save(file_name)
            return

        cell_style = XlsUtils.set_style('Times New Roman', 280, False)
        for index, item in enumerate(data):
            row = index + 1
            sheet.write(row, 0, start_index + index, cell_style)
            sheet.write(row, 1, item['edb_id'], cell_style)
            sheet.write(row, 2, item['description'][1], cell_style)
            sheet.write(row, 3, item['author']['name'], cell_style)
            sheet.write(row, 4, item['type']['name'], cell_style)
            sheet.write(row, 5, item['platform']['platform'], cell_style)
            sheet.write(row, 6, item['date_published'], cell_style)
            # row += 1
        book.save(file_name)
        return

    @staticmethod
    def write_excel(data, start_index):
        file_name = SysUtils.get_now_time().strftime('%Y%m%d %H%M%S') + '.xls'
        XlsUtils.write_sheet(file_name, data, start_index)
        return file_name
