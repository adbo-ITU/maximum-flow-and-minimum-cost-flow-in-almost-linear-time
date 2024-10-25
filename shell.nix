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
    packages = with pkgs; [
      ((python3.withPackages python-packages).override (args: {ignoreCollisions = true;}))
    ];
  }
