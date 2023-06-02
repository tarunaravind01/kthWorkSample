import subprocess
import argparse

def configure_instance(instance_name):
    # Use subprocess to run the Ansible playbook
    subprocess.run(["ansible-playbook", "-i", "inventory.ini", "configure.yml", "-e", f"target={instance_name}"])

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="CLI app to configure online instances using Ansible")
    parser.add_argument("instances", nargs="+", help="Name(s) of the instance(s) to configure")
    args = parser.parse_args()

    # Configure each instance
    for instance_name in args.instances:
        configure_instance(instance_name)
    print("Configuration completed successfully")

if __name__ == "__main__":
    main()
