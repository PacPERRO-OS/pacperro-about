import os, subprocess
import gi
import locale
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk
from locale import gettext as tr

# Translation Constants:
APPNAME = "pacperro-about"
TRANSLATIONS_PATH = "/usr/share/locale"
SYSTEM_LANGUAGE = os.environ.get("LANG")

# Translation functions:
locale.bindtextdomain(APPNAME, TRANSLATIONS_PATH)
locale.textdomain(APPNAME)
locale.setlocale(locale.LC_ALL, SYSTEM_LANGUAGE)

class MainWindow:
    def __init__(self, application):
        # Gtk Builder
        self.builder = Gtk.Builder()

        # Translate things on glade:
        self.builder.set_translation_domain(APPNAME)

        # Import UI file:
        self.builder.add_from_file(os.path.dirname(os.path.abspath(__file__)) + "/pacperro-about.glade")
        self.builder.connect_signals(self)

        # Window
        self.window = self.builder.get_object("pəncərə")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_application(application)
        self.window.connect("destroy", self.onDestroy)
        self.defineComponents()

        self.readSystemInfo()
        
        # Set application:
        self.application = application

        # Show Screen:
        self.window.show_all()
    
    # Window methods:
    def onDestroy(self, action):
        self.window.get_application().quit()
    
    def defineComponents(self):
        self.dialog_report_exported = self.builder.get_object("dialog_report_exported")
        self.dialog_report_failed = self.builder.get_object("dialog_report_failed")

        self.lbl_distro = self.builder.get_object("lbl_distro")
        self.lbl_distro_version = self.builder.get_object("lbl_distro_version")
        self.lbl_distro_codename = self.builder.get_object("lbl_distro_codename")

        self.lbl_user_host = self.builder.get_object("lbl_user_host")
        self.lbl_kernel = self.builder.get_object("lbl_kernel")
        self.lbl_desktop = self.builder.get_object("lbl_desktop")
        self.lbl_cpu = self.builder.get_object("lbl_cpu")
        self.lbl_gpu = self.builder.get_object("lbl_gpu")
        self.lbl_ram = self.builder.get_object("lbl_ram")
        self.lbl_azp_support = self.builder.get_object("lbl_azp_support")

    def readSystemInfo(self):
        output = subprocess.check_output([os.path.dirname(os.path.abspath(__file__)) + "/sistem-info.sh"]).decode("utf-8")
        lines = output.splitlines()
        
        self.lbl_distro.set_label(lines[0])
        self.lbl_distro_version.set_label(lines[1])
        self.lbl_distro_codename.set_label(lines[2])

        self.lbl_user_host.set_label(lines[3])
        self.lbl_kernel.set_label(lines[4])
        self.lbl_desktop.set_label(lines[5])
        if lines[7] == "0":
            self.lbl_cpu.set_label(lines[6])
        else:
            ghz = "{:.2f}".format(float(lines[7])/1000000)
            self.lbl_cpu.set_label(lines[6] + " (" + ghz  + "GHz)")
        self.lbl_gpu.set_label(lines[8])
        self.lbl_ram.set_label(lines[9] + "GB")
        self.lbl_azp_support.set_label(lines[10])
