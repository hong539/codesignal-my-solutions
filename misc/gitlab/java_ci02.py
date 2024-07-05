import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
from tempfile import mkdtemp

def parse_pom(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Define the namespaces used in the pom.xml file
    namespaces = {
        'mvn': 'http://maven.apache.org/POM/4.0.0'
    }
    
    # Extract basic information
    group_id = root.find('mvn:groupId', namespaces)
    artifact_id = root.find('mvn:artifactId', namespaces)
    version = root.find('mvn:version', namespaces)
    
    return {
        "group_id": group_id.text if group_id is not None else "Not found",
        "artifact_id": artifact_id.text if artifact_id is not None else "Not found",
        "version": version.text if version is not None else "Not found"
    }

def run_maven_clean_package():
    # Run the Maven clean package command
    result = subprocess.run(['mvn', 'clean', 'package'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Maven build failed")
        print(result.stderr.decode())
        return False
    else:
        print("Maven build succeeded")
        print(result.stdout.decode())
        return True

def find_jar_files(directory):
    jar_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.jar'):
                jar_files.append(os.path.join(root, file))
    return jar_files

def move_files_to_tmp(jar_files):
    tmp_dir = mkdtemp()
    for jar_file in jar_files:
        shutil.move(jar_file, tmp_dir)
    return tmp_dir

def build_docker_image(tmp_dir):
    dockerfile_content = f"""
    FROM openjdk:8-jdk-alpine
    COPY {tmp_dir}/*.jar /app/
    WORKDIR /app
    # Example of running one jar file
    CMD ["java", "-jar", "{os.listdir(tmp_dir)[0]}"]
    """
    
    dockerfile_path = os.path.join(tmp_dir, 'Dockerfile')
    with open(dockerfile_path, 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

    # Run docker build
    result = subprocess.run(['docker', 'build', '-t', 'my-java-app', tmp_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("Docker build failed")
        print(result.stderr.decode())
    else:
        print("Docker build succeeded")
        print(result.stdout.decode())

def main():
    pom_file_path = 'path/to/your/pom.xml'
    target_directory = 'target'

    # Step 1: Parse the pom.xml file
    pom_info = parse_pom(pom_file_path)
    print("POM Info:", pom_info)
    
    # Step 2: Run mvn clean package
    if not run_maven_clean_package():
        return
    
    # Step 3: Find all jar files under the target directory
    jar_files = find_jar_files(target_directory)
    print("Found JAR files:", jar_files)
    
    # Step 4: Move jar files to a temporary directory
    tmp_dir = move_files_to_tmp(jar_files)
    print("JAR files moved to temporary directory:", tmp_dir)
    
    # Step 5: Build Docker image with JAR files
    build_docker_image(tmp_dir)

if __name__ == "__main__":
    main()