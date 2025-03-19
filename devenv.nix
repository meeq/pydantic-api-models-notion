{ pkgs, lib, config, inputs, ... }:

{
  packages = [ pkgs.git ];

  languages.python.enable = true;
  languages.python.poetry.enable = true;
  languages.python.poetry.activate.enable = true;
  languages.python.version = "3.12";

  scripts.check-types.exec = ''
    poetry \
      run mypy \
        --explicit-package-bases "$DEVENV_ROOT/pydantic_api/notion/models/"
  '';
}
