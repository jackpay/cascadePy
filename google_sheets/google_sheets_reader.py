import pygsheets

class GoogleSheetsReaderWriter():
    """A class to allow google sheets to be read from and written to"""

    def __init__(self, auth_path):
        self.user = pygsheets.authorize(service_file=auth_path)

    def read_sheet(self, sheet_name, working_sheet=0):
        """Get a Google Sheet from the auth users GDrive - needs sheet_name and index of working sheet (i.e. if the GSheet contains multiple internal sheets)"""
        sh = self.user.open(sheet_name)
        return sh[working_sheet]

    def write_sheet(self,output_sheet_name, dataframe, coords=None):
        """Write the sheet starting from the specified coordinates - e.g. (2,2) would start at C2"""
        if coords:
            output_sheet_name.set_dataframe(dataframe, coords)
        else:
            output_sheet_name.set_dataframe(dataframe,(0,0))
