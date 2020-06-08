with import <nixpkgs> {};

mkShell {
  nativeBuildInputs = [
    cargo
    clippy
    gnome3.glade
  ];

  buildInputs = [
    gnome3.gtk3
  ];
}
