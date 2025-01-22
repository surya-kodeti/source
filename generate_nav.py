import os
import yaml

def generate_nav():
    docs_dir = "docs"
    nav = []

    for repo_name in sorted(os.listdir(docs_dir)):
        repo_path = os.path.join(docs_dir, repo_name)
        if not os.path.isdir(repo_path):
            continue  # Skip files, only process directories

        # Create navigation for the repo
        repo_nav = []
        for root, dirs, files in os.walk(repo_path):
            root_relative = os.path.relpath(root, docs_dir)

            # Collect Markdown files in the current directory
            items = []
            for file in sorted(files):
                if file.endswith(".md"):
                    file_path = os.path.join(root_relative, file).replace("\\", "/")
                    if os.path.isfile(file_path):  # Ensure the file exists
                        label = os.path.splitext(file)[0].capitalize()
                        items.append({label: file_path})

            # Add items for this directory
            if items:
                if root_relative != repo_name:  # Add folder structure only if it's not the root
                    folder_label = os.path.basename(root_relative).capitalize()
                    repo_nav.append({folder_label: items})
                else:
                    repo_nav.extend(items)

        # Add repo to navigation
        if repo_nav:  # Only add if there are valid files
            nav.append({repo_name.capitalize(): repo_nav})

    return nav

def update_mkdocs_config(nav):
    config_file = "mkdocs.yml"

    # Read existing mkdocs.yml
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    # Update the nav section
    config["nav"] = nav

    # Write updated mkdocs.yml
    with open(config_file, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print("Navigation updated in mkdocs.yml")

if __name__ == "__main__":
    nav = generate_nav()
    update_mkdocs_config(nav)
