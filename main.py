from streamlit.web import cli as st_cli
from python.runfiles import runfiles


def main() -> None:
    app = runfiles.Create().Rlocation("analytics_tools/user_interface/app.py")
    st_cli.main_run([app, "--server.address=0.0.0.0"])


if __name__ == "__main__":
    main()
