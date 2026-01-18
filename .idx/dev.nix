# To learn more about how to use Nix to configure your environment
# see: https://firebase.google.com/docs/studio/customize-workspace
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.ffmpeg # deepface dependency
    pkgs.tk # deepface dependency
    pkgs.python311Packages.flask
    pkgs.python311Packages.flask-login
    pkgs.python311Packages.flask-bcrypt
    pkgs.python311Packages.flask-cors
    pkgs.python311Packages.deepface
    pkgs.python311Packages.vadersentiment
    pkgs.python311Packages.gunicorn
    pkgs.git
    pkgs.python311Packages.numpy
  ];

  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "ms-python.python"
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["python3", "server/app.py"];
          manager = "web";
        };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # install-deps = "pip install -r requirements.txt";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # No-op, but can be used for other tasks
      };
    };
  };
}
