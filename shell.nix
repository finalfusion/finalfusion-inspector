with import <nixpkgs> {};

let
  finalfusion = pkgs.callPackage (fetchFromGitHub {
    owner = "finalfusion";
    repo = "nix-packages";
    rev = "94177ce11423a608af6969fcfafba323d89de16a";
    sha256 = "1znhb79wj6ibrwa63nd3mm33k8s0a5s0ampcmfj8pajj41cfxdas";
  }) {};
in mkShell {
  nativeBuildInputs = [ qt5.qttools.dev python3Packages.autopep8 python3Packages.flake8 ];

  propagatedBuildInputs = [
    finalfusion.python3Packages.finalfusion
    python3Packages.pyqt5
    python3Packages.setuptools
    python3Packages.toml
  ];

  # Normally set by the wrapper, but we can't use it in nix-shell (?).
  QT_QPA_PLATFORM_PLUGIN_PATH="${qt5.qtbase.bin}/lib/qt-${qt5.qtbase.version}/plugins";
}
