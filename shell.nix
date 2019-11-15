with import <nixpkgs> {};

let
  finalfusion = pkgs.callPackage (fetchFromGitHub {
    owner = "finalfusion";
    repo = "nix-packages";
    rev = "a7fc91ec0336c04b0b51ba9c8c0a806427f96a42";
    sha256 = "02dc1qz1zppi224jh0xlhc3k3qy3cpxcksp36c4cchcgfr0yz532";
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
