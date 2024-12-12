{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:albe2669/poetry2nix/ruff-0.7.2";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = inputs @ { self, nixpkgs, flake-utils, ... }: 
    flake-utils.lib.eachDefaultSystem (system:
      let

        pkgs = nixpkgs.legacyPackages.${system};
        poetry2nix = inputs.poetry2nix.lib.mkPoetry2Nix { inherit pkgs; };
      in
      {
        packages = {
          yourPackage = poetry2nix.mkPoetryApplication {
            projectDir = self;

            # set this to true to use premade wheels rather than the source
            preferWheels = true;
            overrides = poetry2nix.overrides.withDefaults (final: prev: {
                pyright = prev.pyright.overridePythonAttrs
                (
                  old: {
                    buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
                  }
                );
                ruff = prev.ruff.overridePythonAttrs
                (
                  old: {
                    buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
                  }
                );
              });
          };
          default = self.packages.${system}.yourPackage;
        };

        # Shell for app dependencies.
        #
        #     nix develop
        #
        # Use this shell for developing your app.
        devShells.default = pkgs.mkShellNoCC {
          inputsFrom = [ self.packages.${system}.yourPackage ];
          package = with pkgs; [
            # any development dependencies that you might have in nixpkgs
            poetry
            ruff
            pyright
          ];

          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
        };
      }
    );
}
