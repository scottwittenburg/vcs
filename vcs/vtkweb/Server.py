# import vtk modules.
import vtk
from vtk.web import protocols
from vtk.web import wslink as vtk_wslink
from wslink import server


# import protocols
import vcs_server
from Visualizer import Visualizer
from FileLoader import FileLoader


class VCSApp(vtk_wslink.ServerProtocol):

    # Application configuration
    rootDir = "."
    authKey = "wslink-secret"

    def initialize(self):
        self.registerVtkWebProtocol(protocols.vtkWebMouseHandler())
        self.registerVtkWebProtocol(protocols.vtkWebViewPort())
        self.registerVtkWebProtocol(protocols.vtkWebViewPortImageDelivery())
        self.registerVtkWebProtocol(protocols.vtkWebFileBrowser(self.rootDir, 'Home'))
        self.registerVtkWebProtocol(FileLoader(self.rootDir))
        self.registerVtkWebProtocol(Visualizer())

        # Update authentication key to use
        self.updateSecret(VCSApp.authKey)