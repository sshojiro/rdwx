import wx
from pandas import read_csv, DataFrame
import os
import sys
import pprint
from app.library import yarn
from rdkit.Chem.Descriptors import descList
from rdkit.Chem import MolFromSmiles
from numpy import matrix as np_matrix


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Pandas & Pyinstaller", size=(200,150))
        self.InitializeComponents()

    def InitializeComponents(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("LIGHT BLUE")
        self.button = wx.Button(panel, -1, 'Open File')
        self.button.Bind(wx.EVT_BUTTON, self.open_file)
        yarn()
    def open_file(self, event):
        #
        with wx.FileDialog(self, "Open CSV file", wildcard="CSV files (*.csv)|*.csv",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
        df = read_csv(pathname)
        df[['smiles']].to_csv(pathname.replace('.csv','.smi'))
        df['mol'] = df['smiles'].apply(MolFromSmiles)
        X = np_matrix([list(map(lambda f:f(m), dict(descList).values()))
                for m in df['mol']])
        names = list(dict(descList).keys())
        DataFrame(X, index=df.index, columns=names).to_csv(pathname.replace('.csv', '.desc'))

def main():
    app = wx.App(redirect=True)
    top = MyFrame()
    top.Show()
    app.MainLoop()

if __name__=='__main__':
    main()
