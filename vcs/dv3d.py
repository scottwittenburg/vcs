"""
If in interact mode (see :func:`vcs.Canvas.Canvas.interact`), these attributes can be configured interactively, via the
method described in the **Interact Mode** section of the attribute description.
"""
# @author: tpmaxwel
from . import VCS_validation_functions
import multiprocessing
import vcs
import time
import warnings
try:
    from DV3D.ConfigurationFunctions import ConfigManager
    HAS_DV3D = True
except Exception:
    HAS_DV3D = False

from .xmldocs import toggle_surface, toggle_volume, xslider, yslider, zslider, verticalscaling, scalecolormap  # noqa
from .xmldocs import scaletransferfunction, toggleclipping, isosurfacevalue, scaleopacity, basemapopacity, camera, scriptdocs  # noqa


class Gfdv3d(object):
    __doc__ = """
    Gfdv3d is class from which Gf3Dvector, Gf3Dscalar, and Gf3DDualScalar
    inherit. It sets up properties and functions common to all of the 3d
    graphics method objects.

    Attributes
    ----------

    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s
    %s

    .. pragma: skip-doctest
    """ % (toggle_surface, toggle_volume, xslider, yslider, zslider, verticalscaling, scalecolormap,
           scaletransferfunction, toggleclipping, isosurfacevalue, scaleopacity, basemapopacity, camera)
    __slots__ = [
        'g_name',
        'ncores',
        'plot_attributes'
    ]

    def _getname(self):
        return self._name

    def _setname(self, value):
        value = VCS_validation_functions.checkname(self, 'name', value)
        if value is not None:
            self._name = value
    name = property(_getname, _setname)

    def _getaxes(self):
        return self._axes

    def _setaxes(self, value):
        #        value=VCS_validation_functions.checkOnOff(self,'axes',value)
        self._axes = value
    axes = property(_getaxes, _setaxes)

    def _getNumCores(self):
        return self.ncores

    def _setNumCores(self, nc):
        self.ncores = nc
    NumCores = property(_getNumCores, _setNumCores)

    def script(self, script_filename=None, mode=None):
        if (script_filename is None):
            raise ValueError(
                'Error - Must provide an output script file name.')

        if (mode is None):
            mode = 'a'
        elif (mode not in ('w', 'a')):
            raise ValueError(
                'Error - Mode can only be "w" for replace or "a" for append.')

        # By default, save file in json
        scr_type = script_filename.split(".")
        if len(scr_type) == 1 or len(scr_type[-1]) > 5:
            scr_type = "json"
            if script_filename != "initial.attributes":
                script_filename += ".json"
        else:
            scr_type = scr_type[-1]
        if scr_type == '.scr':
            raise vcs.VCSDeprecationWarning("scr script are no longer generated")
        elif scr_type == ".py":
            mode = mode + '+'
            py_type = script_filename[
                len(script_filename) -
                3:len(script_filename)]
            if (py_type != '.py'):
                script_filename = script_filename + '.py'

            # Write to file
            fp = open(script_filename, mode)

            if (fp.tell() == 0):  # Must be a new file, so include below
                fp.write("#####################################\n")
                fp.write("#                                 #\n")
                fp.write("# Import and Initialize VCS     #\n")
                fp.write("#                             #\n")
                fp.write("#############################\n")
                fp.write("import vcs\n")
                fp.write("v=vcs.init()\n\n")

            gtype = 'xyt' if (self._axes == "Hovmoller3D") else 'default'
            unique_name = 'gm3d_%s' % str(time.time() % 1)[2:]
            fp.write('%s = vcs.get%s("%s")\n' % (unique_name, self.g_name, gtype))
            for param_name in self.parameter_names:
                fp.write('%s.%s = %s\n' % (unique_name, param_name, self.cfgManager.getParameterValue(param_name)))
        else:
            # Json type
            mode += "+"
            f = open(script_filename, mode)
            vcs.utils.dumpToJson(self, f)
            f.close()
    # can we add a scriptdocs[g_name] here and have each derived class pick up the documentation correctly?

    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):
        if not HAS_DV3D:
            warnings.warn("Could not find DV3D module, you will not be able to use DV3D's graphic methods")
            return
        if not isinstance(Gfdv3d_name, str):
            raise ValueError("DV3D name must be a string")
        if Gfdv3d_name in list(vcs.elements[self.g_name].keys()):
            raise ValueError(
                "DV3D graphic method '%s' already exists" %
                Gfdv3d_name)
        self._name = Gfdv3d_name
        self.plot_attributes = {}
        self.projection = 'default'
        self.provenanceHandler = None

        vcs.elements[self.g_name][Gfdv3d_name] = self

        self._axes = "xyz"

        # Use parent config values if possible
        if isinstance(Gfdv3d_name_src, str):
            # Make sure we aren't inheriting from ourself
            if Gfdv3d_name_src != Gfdv3d_name:
                parent_cfg = vcs.elements[self.g_name][Gfdv3d_name_src].cfgManager
                self._axes = vcs.elements[self.g_name][Gfdv3d_name_src]._axes
            else:
                parent_cfg = None
        else:
            # Make sure we aren't inheriting from ourself
            if Gfdv3d_name_src.name != self.name:
                parent_cfg = Gfdv3d_name_src.cfgManager
                self._axes = Gfdv3d_name_src._axes
            else:
                parent_cfg = None

        self.cfgManager = ConfigManager(cm=parent_cfg)

        if Gfdv3d_name == "Hovmoller3D":
            self._axes = "xyt"

        self.ncores = multiprocessing.cpu_count()

        self.addParameters()

        self.plot_attributes['name'] = self.g_name
        self.plot_attributes['template'] = Gfdv3d_name

    def setProvenanceHandler(self, provenanceHandler):
        self.provenanceHandler = provenanceHandler

    def getStateData(self):
        return self.cfgManager.getStateData()

    def getConfigurationData(self, **args):
        return self.cfgManager.getConfigurationData(**args)

    def getConfigurationParms(self, **args):
        return self.cfgManager.getConfigurationParms(**args)

    def getConfigurationState(self, pname, **args):
        return self.cfgManager.getConfigurationState(pname, **args)

    def add_property(self, name):

        def fget(self):
            return self.getParameter(name)

        def fset(self, value):
            self.setParameter(name, value)

        setattr(self.__class__, name, property(fget, fset))
        if name not in Gfdv3d.__slots__:
            Gfdv3d.__slots__.append(name)

    def addPlotAttribute(self, name, value):
        self.plot_attributes[name] = value

    def getPlotAttribute(self, name):
        return self.plot_attributes.get(name, None)

    def getPlotAttributes(self):
        return self.plot_attributes

    @staticmethod
    def getParameterList():
        from DV3D.DV3DPlot import PlotButtonNames
        cfgManager = ConfigManager()
        parameterList = cfgManager.getParameterList(extras=PlotButtonNames)
        return parameterList

    def addParameters(self):
        self.parameter_names = []
        for pname in self.getParameterList():
            self.add_property(pname)
            self.parameter_names.append(pname)
#            print "  ------------->> Adding parameter: ", pname

    def getParameter(self, param_name, **args):
        return self.cfgManager.getParameterValue(param_name, **args)

    def setParameter(self, param_name, data, **args):
        self.cfgManager.setParameter(param_name, data, **args)

    def restoreState(self):
        self.cfgManager.restoreState()

    def initDefaultState(self):
        self.cfgManager.initDefaultState()

    def list(self):
        print('---------- DV3D (Gfdv3d) member (attribute) listings ----------')
        print('name =', self.name)
        print('axes =', self.axes)
        for pname in self.parameter_names:
            pval = self.getParameter(pname)
            print(pname, '=', repr(pval))


class Gf3Dvector(Gfdv3d):
    """
    Gf3Dvector
    """
    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):
        self.g_name = '3d_vector'
        Gfdv3d.__init__(self, Gfdv3d_name, Gfdv3d_name_src=Gfdv3d_name_src)


class Gf3Dscalar(Gfdv3d):
    """
    Gf3Dscalar
    """
    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):
        self.g_name = '3d_scalar'
        Gfdv3d.__init__(self, Gfdv3d_name, Gfdv3d_name_src=Gfdv3d_name_src)
        self.VectorDisplay = Gfdv3d_name


class Gf3DDualScalar(Gfdv3d):
    """
    Gf3DDualScalar
    """
    def __init__(self, Gfdv3d_name, Gfdv3d_name_src='default'):
        self.g_name = '3d_dual_scalar'
        Gfdv3d.__init__(self, Gfdv3d_name, Gfdv3d_name_src=Gfdv3d_name_src)
