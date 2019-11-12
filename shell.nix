with import <nixpkgs> {};

let
  finalfusion = pkgs.callPackage (fetchFromGitHub {
    owner = "finalfusion";
    repo = "nix-packages";
    rev = "94177ce11423a608af6969fcfafba323d89de16a";
    sha256 = "1znhb79wj6ibrwa63nd3mm33k8s0a5s0ampcmfj8pajj41cfxdas";
  }) {};
in mkShell {
  nativeBuildInputs = [
    gnome3.glade
    latest.rustChannels.stable.rust
  ];

  buildInputs = [
    gnome3.gtk3
  ];
}
