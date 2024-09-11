#!/usr/bin/env python3

import subprocess
import argparse

# A function to run shell commands with real-time output
def run_command(command):
    """Run a shell command and stream the output in real-time."""
    try:
        print(f"Running command: {command}")
        # Use subprocess.Popen for real-time streaming of stdout and stderr
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Stream output line by line
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Capture and print any errors that occurred
        stderr = process.communicate()[1]
        if stderr:
            print(f"Error: {stderr.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr}")

# Base function to handle Docker build
def build_docker(image_tag="latest"):
    """Build the Docker image."""
    run_command(f"docker build -t my_docker_image:{image_tag} .")

# Function to run Docker Compose up
def docker_compose_up(detached=False):
    """Run docker compose up."""
    cmd = "docker compose up"
    if detached:
        cmd += " -d"
    run_command(cmd)

# Function to clean orphan containers
def clean_orphans():
    """Remove orphan containers."""
    run_command("docker-compose up --remove-orphans")

# Easily extensible with additional commands
def some_other_command():
    """Placeholder for another generic command."""
    run_command("echo 'This is another command!'")

# Main function to parse arguments and run appropriate commands
def main():
    parser = argparse.ArgumentParser(description="Buildy - A wrapper to run various commands")
    
    # Define subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommand: build
    build_parser = subparsers.add_parser("build", help="Build the Docker image")
    build_parser.add_argument("--tag", type=str, default="latest", help="Tag for the Docker image (default: latest)")

    # Subcommand: up
    up_parser = subparsers.add_parser("up", help="Run docker-compose up")
    up_parser.add_argument("-d", "--detached", action="store_true", help="Run containers in detached mode")

    # Subcommand: clean
    clean_parser = subparsers.add_parser("clean", help="Clean orphan containers")

    # Subcommand: other
    other_parser = subparsers.add_parser("other", help="Run some other command")

    # Parse the arguments
    args = parser.parse_args()

    # Execute appropriate command
    if args.command == "build":
        build_docker(args.tag)
    elif args.command == "up":
        docker_compose_up(args.detached)
    elif args.command == "clean":
        clean_orphans()
    elif args.command == "other":
        some_other_command()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
