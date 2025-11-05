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
in 

mkShell {
  name = "Pukalendar Shell";
  description = "NixEnvironment to use with the Pukalendar project";
  buildInputs = [
    pythonEnv
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