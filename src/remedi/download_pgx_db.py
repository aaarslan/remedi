import json
import os
import subprocess


def download_pgx_db():
    # Define the directory where you want to save the files
    directory = "data"
    pharma_dir = os.path.join(directory, "pharmacogenomics")

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Prepare the wget command with the directory prefix
    if not os.path.exists(pharma_dir):
        command = f"wget --recursive --no-parent --no-host-directories --cut-dirs 8 -P {directory} ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/24.03/output/etl/json/pharmacogenomics"
        process = subprocess.Popen(command, shell=True)
        process.wait()

        if process.returncode != 0:
            print(f"Command failed with exit code {process.returncode}")
        else:
            print("Download completed successfully.")
            # Proceed to check success and potentially combine JSON files
    if os.path.exists(pharma_dir):
        check_success_and_combine_jsons(pharma_dir)


def check_success_and_combine_jsons(directory):
    # Check for the _SUCCESS file
    if "_SUCCESS" in os.listdir(directory):
        # Combine JSON files
        combine_json_files(directory)
    else:
        print("Download was not successful. _SUCCESS file not found.")


def combine_json_files(directory):
    json_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.startswith("part-") and f.endswith(".json")
    ]
    data_list = []

    for file_name in json_files:
        with open(file_name, "r") as file:
            for line in file:
                try:
                    data = json.loads(line.strip())
                    data_list.append(data)  # Append each JSON object to the list
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {file_name}: {e}")

    combined_file_path = os.path.join(directory, "combined.json")
    with open(combined_file_path, "w") as outfile:
        json.dump(data_list, outfile)

    print(f"All JSON files have been combined into {combined_file_path}")


if __name__ == "__main__":
    download_pgx_db()
