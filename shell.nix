let
  unstable = import (fetchTarball "https://channels.nixos.org/nixos-unstable/nixexprs.tar.xz") { };
in
with (import <nixpkgs> {});
let
  python-packages = ps:
    with ps; [
      numpy
      networkx
      pytest
    ];
in
  mkShellNoCC {
    packages = with unstable; [
      poetry
      ((python3.withPackages python-packages).override (args: {ignoreCollisions = true;}))
    ];

    LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  }
