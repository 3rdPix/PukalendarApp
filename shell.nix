with import <nixpkgs> {};

let
  pythonEnv = pkgs.python3.withPackages (p: with p; [
      pyqt6
      babel
      beautifulsoup4
      certifi
      charset-normalizer
      colorthief
      darkdetect
      idna
      jinja2
      numpy
      pdoc
      pillow
      pygments
      scipy
      soupsieve
      urllib3
      requests
  ]);
  pyqt6StubsSrc = pkgs.fetchFromGitHub {
    owner = "TilmanK";
    repo = "PyQt6-stubs";
    rev = "86d119ed202c1f9f86923563c2754cf93c1ec303";
    sha256 = "0yg7bj969i83zac450bc09m8qf8jkpq4i0yzwlablzrjq3wz4xpv";
  };
  pyqt6Stubs = pkgs.python3.pkgs.buildPythonPackage rec {
    pname = "pyqt6-stubs-custom";
    version = "6.2.3"; 
    src = pyqt6StubsSrc;

    doCheck = false; 
  };
in 

mkShell {
  name = "Pukalendar Shell";
  description = "NixEnvironment to use with the Pukalendar project";
  buildInputs = [
    pythonEnv
    pyqt6Stubs
    libGL
    qt6.wrapQtAppsHook
    qt6.qtbase
  ];

    # export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
  shellHook = ''
    export QT_PLUGIN_PATH=${qt6.qtbase}/lib/qt-6/plugins
    export QT_QPA_PLATFORM_PLUGIN_PATH=${qt6.qtbase}/lib/qt-6/plugins/platforms
    export PATH=${pythonEnv}/bin/:$PATH
    export PYTHONPATH=$(realpath PyQt-Fluent-Widgets/)/:$PYTHONPATH
    export PYTHONPATH=$(realpath PyQt-Frameless-Window/)/:$PYTHONPATH
  '';
}